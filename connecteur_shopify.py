"""
Connecteur generique Shopify pour PokeDeals.

Interroge l'endpoint public /products.json expose par toute boutique Shopify
(pas besoin de cle API ni d'authentification) pour recuperer le catalogue et
rechercher des produits par critere (nom, numero), dans le meme esprit que
les connecteurs existants (eBay, Vinted, Cardtrader).

Reutilisable tel quel sur les ~40 boutiques Shopify identifiees lors de
l'audit (voir audit_boutiques.py) : il suffit de changer le nom de domaine.
"""

import re
import sys
import time
from dataclasses import dataclass

import requests

# Evite les UnicodeEncodeError sur la console Windows (cp1252) face a des
# caracteres speciaux presents dans certains titres de produits.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

TIMEOUT = 15
DELAY_BETWEEN_PAGES = 0.5
PRODUITS_PAR_PAGE = 250
MAX_PAGES = 20  # limite de securite -> 5000 produits max

# Mots-cles (FR + EN) utilises pour deviner la langue d'un produit a partir
# de son titre. Volontairement minimal : si rien ne matche, on retourne None
# (indetermine) plutot que de deviner.
# Inclut aussi des langues HORS watchlist (chinois, anglais, indonesien...)
# afin de pouvoir exclure ces variantes d'un rapprochement de cote errone
# (ex: carte "Chinois Traditionnel" comparee par erreur a une cote FR) --
# cf. bonne_affaire_shopify.py qui rejette tout langue_detectee != carte.langue.
LANGUE_MOTS_CLES = {
    "fr": ["français", "francais", "french"],
    "jp": ["japonais", "japanese"],
    "kr": ["coréen", "coreen", "korean"],
    "cn": ["chinois", "chinese"],
    "en": ["anglais", "english"],
    "id": ["indonésien", "indonesien", "indonesian"],
}


@dataclass
class CritereRecherche:
    """Un critere de recherche issu de la watchlist config.yaml.

    numero peut valoir None (pas de numero exploitable, ex: "Evoli Trainer
    Gallery"), contenir un denominateur ("199/165") ou non ("SWSH087", "117").
    """
    nom: str
    numero: str | None = None


@dataclass
class ResultatRecherche:
    boutique: str
    titre: str
    prix: float
    en_stock: bool
    url_produit: str
    variante_titre: str
    image_url: str | None
    langue_detectee: str | None
    # "forte" = matche sur nom ET numero (fiable, exploitable pour une alerte
    # automatique). "faible" = repli nom seul, faute de numero exploitable
    # dans la watchlist -> a verifier manuellement avant d'alerter.
    confiance: str = "forte"
    necessite_verification_manuelle: bool = False


def detecter_langue(titre: str) -> str | None:
    """Devine la langue d'un produit a partir des mentions dans son titre.

    Retourne None si aucune mention n'est trouvee (indetermine), plutot que
    de deviner a partir d'autres indices (nom de domaine, etc.).
    """
    titre_lower = titre.lower()
    for langue, mots in LANGUE_MOTS_CLES.items():
        if any(mot in titre_lower for mot in mots):
            return langue
    return None


def _regex_numero_sans_denominateur(numero: str) -> re.Pattern:
    """Construit une regex tolerante au padding de zeros pour un numero SANS
    denominateur (ex: "087" doit aussi matcher "87", "SWSH087" doit aussi
    matcher "SWSH87"). Bornee par des lookarounds anti-chiffre pour eviter
    qu'un numero court ("87") ne matche a l'interieur d'un plus grand
    ("1087")."""
    def remplacer_digits(m: re.Match) -> str:
        digits = m.group(0)
        sans_zeros = digits.lstrip("0") or "0"
        return r"0*" + re.escape(sans_zeros)

    corps = re.sub(r"\d+", remplacer_digits, re.escape(numero))
    return re.compile(r"(?<!\d)" + corps + r"(?!\d)", re.IGNORECASE)


def _titre_correspond(titre: str, critere: CritereRecherche) -> bool:
    """Applique les regles de matching nom/numero decrites dans la doc de
    rechercher_par_mots_cles."""
    titre_lower = titre.lower()

    if critere.nom.lower() not in titre_lower:
        return False

    if critere.numero is None:
        # Pas de numero exploitable -> repli sur le nom seul (comme pour eBay,
        # cf. config.yaml lignes 201-206).
        return True

    if "/" in critere.numero:
        # Numero avec denominateur -> substring exact obligatoire.
        return critere.numero.lower() in titre_lower

    # Numero sans denominateur -> le nom seul ne suffit jamais : on exige en
    # plus une correspondance (tolerante au padding de zeros) du numero.
    return bool(_regex_numero_sans_denominateur(critere.numero).search(titre))


class ConnecteurShopify:
    """Connecteur generique pour une boutique Shopify, identifiee par son domaine."""

    def __init__(self, domaine: str, nom_affiche: str | None = None):
        self.domaine = domaine.strip().rstrip("/")
        self.nom_affiche = nom_affiche or domaine
        self.base_url = f"https://{self.domaine}"
        self.session = requests.Session()

    def recuperer_tout_le_catalogue(self) -> list[dict]:
        """Pagine sur /products.json jusqu'a epuisement du catalogue (ou limite de securite)."""
        produits: list[dict] = []

        for page in range(1, MAX_PAGES + 1):
            url = f"{self.base_url}/products.json?limit={PRODUITS_PAR_PAGE}&page={page}"
            try:
                r = self.session.get(url, headers=HEADERS, timeout=TIMEOUT)
                r.raise_for_status()
                data = r.json()
            except (requests.exceptions.RequestException, ValueError):
                # Page en echec (reseau, timeout, JSON invalide) -> on s'arrete proprement
                break

            page_produits = data.get("products", [])
            if not page_produits:
                break

            produits.extend(page_produits)

            if page < MAX_PAGES:
                time.sleep(DELAY_BETWEEN_PAGES)

        return produits

    def rechercher_dans_catalogue(
        self, catalogue: list[dict], criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        """Recherche des cartes par critere (nom, numero) issu de config.yaml,
        dans un catalogue DEJA RECUPERE (aucun appel reseau ici).

        A utiliser quand le meme catalogue doit servir a plusieurs logiques
        (ex: detection "bonne affaire" ET detection "retour en stock") pour
        eviter de refaire un appel /products.json par logique.

        Regles de matching (nom ET numero obligatoires des qu'un numero existe) :
          - numero avec denominateur ("199/165")       -> nom (substring) ET
            numero (substring exact)
          - numero sans denominateur ("SWSH087", "117") -> nom (substring) ET
            numero (regex tolerante au padding de zeros). Le numero seul ne
            suffit jamais : trop de faux positifs sur les numeros courts.
          - pas de numero (None)                        -> repli sur le nom
            seul, comme le fait deja le bot pour eBay.

        Retourne un dict {(nom, numero): [resultats]} pour que l'appelant
        puisse voir, critere par critere, ce qui a ete trouve ou non.
        """
        resultats_par_critere: dict[tuple[str, str | None], list[ResultatRecherche]] = {
            (nom, numero): [] for nom, numero in criteres
        }

        for nom, numero in criteres:
            critere = CritereRecherche(nom=nom, numero=numero)
            # Sans numero exploitable, on ne fait que du matching nom seul :
            # confiance faible, a ne jamais traiter comme une alerte fiable.
            confiance = "forte" if numero is not None else "faible"
            necessite_verification = numero is None

            for produit in catalogue:
                titre = produit.get("title", "")
                if not _titre_correspond(titre, critere):
                    continue

                handle = produit.get("handle", "")
                url_produit = f"{self.base_url}/products/{handle}"
                image_url = None
                images = produit.get("images") or []
                if images:
                    image_url = images[0].get("src")
                langue_detectee = detecter_langue(titre)

                for variant in produit.get("variants", []):
                    try:
                        prix = float(variant.get("price"))
                    except (TypeError, ValueError):
                        continue

                    resultats_par_critere[(nom, numero)].append(ResultatRecherche(
                        boutique=self.nom_affiche,
                        titre=titre,
                        prix=prix,
                        en_stock=bool(variant.get("available")),
                        url_produit=url_produit,
                        variante_titre=variant.get("title", ""),
                        image_url=image_url,
                        langue_detectee=langue_detectee,
                        confiance=confiance,
                        necessite_verification_manuelle=necessite_verification,
                    ))

        return resultats_par_critere

    def rechercher_par_mots_cles(
        self, criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        """Raccourci pour un usage standalone : recupere le catalogue PUIS
        cherche dedans (1 appel reseau, comme avant). Quand le meme catalogue
        doit servir a plusieurs logiques d'analyse dans le meme cycle de scan
        (bonne affaire + retour en stock...), preferer recuperer_tout_le_catalogue()
        une seule fois et appeler rechercher_dans_catalogue() sur le resultat
        partage, pour ne pas refaire l'appel /products.json a chaque fois."""
        catalogue = self.recuperer_tout_le_catalogue()
        return self.rechercher_dans_catalogue(catalogue, criteres)


if __name__ == "__main__":
    # Echantillon de 10 entrees REELLES de config.yaml (watchlist PokeDeals),
    # melangeant les 3 formats rencontres :
    #   - standard avec denominateur (X/Y)
    #   - JP/KR avec code de set abrege (numero garde le denominateur, le
    #     code de set genre "sv2a"/"mC" n'est pas utilise comme numero)
    #   - promo/Trainer Gallery sans denominateur, voire sans numero du tout
    echantillon_config: list[tuple[str, str | None]] = [
        ("Dracaufeu", "199/165"),          # standard FR, denominateur
        ("Pikachu", "173/165"),            # standard FR, denominateur
        ("Mew", "193/165"),                # standard FR, denominateur
        ("Charizard", "201/165"),          # JP (sv2a) — denominateur conserve
        ("Méga-Dracaufeu Y", "294/217"),   # standard FR, denominateur
        ("Evoli", "SWSH087"),              # promo FR, sans denominateur
        ("Morpeko", "117"),                # promo FR, sans denominateur
        ("Poissirene", "087"),             # promo FR, sans denominateur (test padding)
        ("Pikachu", "764"),                # JP (mC), sans denominateur
        ("Evoli", None),                   # Trainer Gallery, pas de numero exploitable
    ]

    boutiques = ["questcorner.fr", "kyoriyu.fr"]

    for domaine in boutiques:
        print(f"\n{'=' * 70}")
        print(f"Boutique : {domaine}")
        print("=" * 70)

        connecteur = ConnecteurShopify(domaine)
        resultats_par_critere = connecteur.rechercher_par_mots_cles(echantillon_config)

        for (nom, numero), resultats in resultats_par_critere.items():
            libelle = f"{nom} {numero}" if numero else f"{nom} (sans numero)"
            print(f"\n--- {libelle} ---")

            if not resultats:
                print("  Non trouve.")
                continue

            resultats.sort(key=lambda r: r.prix)
            for r in resultats:
                statut = "EN STOCK" if r.en_stock else "RUPTURE "
                langue = r.langue_detectee or "?"
                marque_confiance = "⚠ A VERIFIER" if r.necessite_verification_manuelle else "confiance forte"
                print(f"  [{statut}] ({langue}) [{marque_confiance}] {r.titre} — {r.prix:.2f}€ — {r.url_produit}")
