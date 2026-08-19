"""
Watchlist et logique de detection pour le radar de PRECOMMANDES (produits
scelles a venir, pas des cartes a l'unite) -- fonctionnalite INDEPENDANTE
des deux systemes d'alerte existants (bonne_affaire_shopify.py = seuil de
prix sur des cartes deja catalogues, alerte_stock.py = retour en stock d'un
produit deja catalogue). Ici on detecte l'APPARITION d'un produit qui
n'existait pas avant sur une boutique -- la precommande elle-meme, en stock
ou non.

La date d'ouverture de precommande de chaque produit est PAR DEFINITION
inconnue (c'est ce que ce radar sert a decouvrir) -- pas de fenetre de scan
calculee, le scan tourne au meme rythme que le cycle existant de chaque
plateforme, jusqu'a la date de sortie du produit (au-dela, le produit
bascule en vente normale, plus interessant pour CE radar specifique).

Pour ajouter un futur produit a surveiller : ajouter une entree a
PRODUITS_SURVEILLES ci-dessous (voir la docstring de ProduitSurveille).
Aucune autre modification de code necessaire.
"""

import re
import unicodedata
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ProduitSurveille:
    """Un produit scelle a venir a detecter des sa mise en precommande.

    nom : identifiant lisible (utilise dans les alertes et la memoire).
    mots_cles_edition : au moins UN de ces termes doit apparaitre dans le
        texte du produit (titre + description si disponible) -- identifie
        l'EDITION/COFFRET (ex: "30e anniversaire", "règne delta").
    mots_cles_type : au moins UN de ces termes doit AUSSI apparaitre --
        identifie le TYPE de produit ou le personnage (ex: "ETB",
        "mentali"). Les deux groupes sont requis ENSEMBLE (comme le
        matching nom+numero deja utilise pour les cartes a l'unite) pour
        eviter les faux positifs sur un simple "anniversaire" isole.
    date_sortie : date de sortie officielle FR -- sert à CONFIRMER un match
        trouve (si une date est detectable sur la page) et a desactiver
        automatiquement la detection une fois passee.
    prioritaire : marque un produit auquel Justok tient particulierement --
        purement cosmetique (ajoute un ⭐ dans l'alerte Telegram, cf.
        alerte_precommande._texte_precommande), n'affecte AUCUNE logique de
        detection/suppression d'alerte. Ajoute le 18/08/2026 pour l'UPC
        Noctali, a la demande explicite de Justok.
    """
    nom: str
    mots_cles_edition: frozenset[str]
    mots_cles_type: frozenset[str]
    date_sortie: date
    prioritaire: bool = False


PRODUITS_SURVEILLES: list[ProduitSurveille] = [
    ProduitSurveille(
        nom="Coffret Dresseur d'Élite — 30e Anniversaire (30th Celebration) FR",
        mots_cles_edition=frozenset({
            # PAS de "celebration"/"célébration" seul : matche a tort
            # l'ANCIEN coffret "Celebrations"/"Célébrations" (25e
            # anniversaire, EB7.5, 2021), toujours en vente/revente --
            # faux positif reel constate lors du test sur echantillon
            # (lemantcg.fr, hikarudistribution.com, poke-geek.fr,
            # hamacards.com). "30th celebration" (l'expression complete,
            # nom officiel EN du set 2026) reste sans ambiguite.
            "30e anniversaire", "30eme anniversaire", "30th anniversary",
            "30th celebration",
        }),
        mots_cles_type=frozenset({
            "dresseur d'elite", "dresseur elite", "etb", "elite trainer box",
        }),
        date_sortie=date(2026, 9, 16),
    ),
    ProduitSurveille(
        nom="Coffret Dresseur d'Élite — ME06 Règne Delta FR",
        mots_cles_edition=frozenset({
            "regne delta", "delta reign", "me06",
        }),
        mots_cles_type=frozenset({
            "dresseur d'elite", "dresseur elite", "etb", "elite trainer box",
        }),
        date_sortie=date(2026, 11, 6),
    ),
    # V55 (18/08/2026) : precedemment UNE seule entree "Journee et Soiree
    # (Mentali/Noctali)" avec les mots-cles type des DEUX personnages --
    # signale par Justok : UPC Mentali et UPC Noctali sont deux produits
    # DISTINCTS (fiches produit separees, precommandes potentiellement
    # ouvertes a des moments differents), pas un seul produit a 2 variantes.
    # Bug reel identifie avant qu'il ne se manifeste (verifie en creusant
    # la memoire du 18/08 : aucune boutique n'avait encore les DEUX
    # fiches a la fois) : _candidat() (radar_precommandes.py) utilise
    # `produit.nom` comme cle de memoire (`domaine|nom_produit`, cf.
    # alerte_precommande._cle_memoire) -- avec un seul ProduitSurveille
    # couvrant les deux personnages, les 2 fiches d'une meme boutique
    # auraient partage la MEME cle memoire, et detecter_nouvelles_precommandes()
    # aurait alors traite la 2e fiche scannee comme "deja connue" (ou pire,
    # ecrase silencieusement les infos de la 1ere) -- une des deux
    # precommandes aurait ete perdue sans jamais alerter. Scinde en 2
    # entrees separees, memes mots-cles edition et date_sortie, mots-cles
    # type isoles par personnage.
    ProduitSurveille(
        nom="Collection Ultra-Premium — Espeon (Mentali) 30e Anniversaire FR",
        mots_cles_edition=frozenset({
            # PAS de "ultra premium" seul : c'est aussi un adjectif
            # marketing generique ("carte ultra premium issue de
            # l'extension...") utilise sur des cartes a l'unite SANS
            # RAPPORT -- faux positif reel constate lors du test sur
            # echantillon (questcorner.fr, un simple Noctali-VMAX EVS).
            # La phrase complete "collection ultra premium" (dans
            # n'importe quel ordre de mots) est specifique au produit.
            "collection ultra premium", "ultra premium collection", "upc",
            "journee et soiree", "day and night",
        }),
        mots_cles_type=frozenset({
            "mentali", "espeon",
        }),
        date_sortie=date(2026, 11, 6),
    ),
    ProduitSurveille(
        nom="Collection Ultra-Premium — Umbreon (Noctali) 30e Anniversaire FR",
        mots_cles_edition=frozenset({
            "collection ultra premium", "ultra premium collection", "upc",
            "journee et soiree", "day and night",
        }),
        mots_cles_type=frozenset({
            "noctali", "umbreon",
        }),
        date_sortie=date(2026, 11, 6),
        prioritaire=True,  # celle qui interesse le plus Justok (18/08/2026)
    ),
]


def _normaliser_accents_casse(texte: str) -> str:
    """Minuscule, accents retires -- SANS toucher a la ponctuation (utilise
    pour l'extraction de dates, ou "/" et "-" sont significatifs : "16/09/2026")."""
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("ascii")
    return sans_accents.lower()


def _normaliser(texte: str) -> str:
    """Minuscule, accents retires, ponctuation (tirets, apostrophes...)
    reduite a un espace -- pour comparer un texte de page (accents, casse,
    typographie variables : "Ultra-Premium" / "Ultra Premium", "d'Élite" /
    "d Elite") aux mots-cles de PRODUITS_SURVEILLES (deja ecrits sans
    accents ci-dessus, cf. "regne" pas "règne"). Meme principe que
    _normaliser_texte dans connecteur_prestashop_sitemap.py.

    NE PAS utiliser pour l'extraction de dates (cf. _normaliser_accents_casse)
    -- "/" et "-" y sont significatifs ("16/09/2026"), les ecraser en
    espace romprait le format numerique JJ/MM/AAAA."""
    return re.sub(r"[^a-z0-9]+", " ", _normaliser_accents_casse(texte))


def produits_actifs(aujourdhui: date | None = None) -> list[ProduitSurveille]:
    """Produits dont la date de sortie n'est pas encore passee -- arret
    automatique de la detection au-dela (cf. docstring du module)."""
    aujourdhui = aujourdhui or date.today()
    return [p for p in PRODUITS_SURVEILLES if p.date_sortie >= aujourdhui]


# --- Detection de mots-cles ---

def titre_correspond_produit(texte: str, produit: ProduitSurveille) -> bool:
    """Le double groupe (edition ET type) doit matcher -- meme principe que
    nom+numero pour les cartes a l'unite, evite qu'un simple "anniversaire"
    ou "ETB" isole (tres frequent, n'importe quel set a un ETB) declenche
    un faux positif.

    Les mots-cles eux-memes sont normalises AVANT la comparaison (pas
    seulement le texte de la page) : "dresseur d'elite" (avec apostrophe,
    tel qu'ecrit dans PRODUITS_SURVEILLES) ne matcherait sinon JAMAIS un
    texte normalise (ponctuation ecrasee, donc sans apostrophe) -- bug reel
    constate lors du re-test sur echantillon (poke-geek.fr, faux rejet
    d'un match legitime)."""
    texte_norm = _normaliser(texte)
    a_edition = any(_normaliser(mot) in texte_norm for mot in produit.mots_cles_edition)
    a_type = any(_normaliser(mot) in texte_norm for mot in produit.mots_cles_type)
    return a_edition and a_type


# --- Extraction et validation de date sur la page produit ---

MOIS_FR = {
    "janvier": 1, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "decembre": 12,
}
MOIS_EN = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12,
}

# Formats numeriques : "16/09/2026", "16-09-2026", "2026-09-16" (ISO).
_RE_DATE_JJ_MM_AAAA = re.compile(r"\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})\b")
_RE_DATE_ISO = re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b")
# Formats textuels FR/EN : "16 septembre 2026", "September 16, 2026" / "16 September 2026".
_RE_DATE_TEXTE_JJ_MOIS_AAAA = re.compile(
    r"\b(\d{1,2})(?:er)?\s+([a-z]+)\s+(\d{4})\b"
)
_RE_DATE_TEXTE_MOIS_JJ_AAAA = re.compile(
    r"\b([a-z]+)\s+(\d{1,2}),?\s+(\d{4})\b"
)


def extraire_dates_page(texte: str) -> list[date]:
    """Extrait toutes les dates plausibles reperees dans un texte de page
    (titre + description), tous formats couverts confondus. Retourne une
    liste (potentiellement vide) -- ne leve jamais, une date invalide
    (ex: 32/13/2026) est simplement ignoree."""
    texte_norm = _normaliser_accents_casse(texte)
    dates_trouvees: list[date] = []

    for m in _RE_DATE_JJ_MM_AAAA.finditer(texte_norm):
        jour, mois, annee = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            dates_trouvees.append(date(annee, mois, jour))
        except ValueError:
            pass

    for m in _RE_DATE_ISO.finditer(texte_norm):
        annee, mois, jour = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            dates_trouvees.append(date(annee, mois, jour))
        except ValueError:
            pass

    for m in _RE_DATE_TEXTE_JJ_MOIS_AAAA.finditer(texte_norm):
        jour, nom_mois, annee = int(m.group(1)), m.group(2), int(m.group(3))
        mois = MOIS_FR.get(nom_mois) or MOIS_EN.get(nom_mois)
        if mois:
            try:
                dates_trouvees.append(date(annee, mois, jour))
            except ValueError:
                pass

    for m in _RE_DATE_TEXTE_MOIS_JJ_AAAA.finditer(texte_norm):
        nom_mois, jour, annee = m.group(1), int(m.group(2)), int(m.group(3))
        mois = MOIS_EN.get(nom_mois) or MOIS_FR.get(nom_mois)
        if mois:
            try:
                dates_trouvees.append(date(annee, mois, jour))
            except ValueError:
                pass

    return dates_trouvees


def evaluer_correspondance(
    titre: str, texte_description: str, produit: ProduitSurveille
) -> tuple[str, str] | tuple[None, str]:
    """Applique la regle complete de detection a un produit trouve sur une
    boutique. Retourne (confiance, raison) si retenu -- confiance vaut
    "forte" (date de sortie confirmee sur la page) ou "moyenne" (mots-cles
    matches, aucune date exploitable) -- ou (None, raison) si rejete.

    Regles (cf. consigne) :
      - Mots-cles (edition ET type) obligatoires -- sinon rejet immediat.
      - Si une date INCOMPATIBLE (ni le jour attendu, ni aucune date qui
        s'en approche) est trouvee sur la page -- rejet (signe frequent
        d'un faux positif : une ANCIENNE extension au nom proche, avec sa
        propre date de sortie deja passee).
      - Si la date ATTENDUE est trouvee -- confiance forte.
      - Si aucune date exploitable n'est trouvee -- confiance moyenne (la
        plupart des pages de precommande n'auront pas de date structuree
        scrapable a ce stade)."""
    texte_complet = f"{titre} {texte_description}"

    if not titre_correspond_produit(texte_complet, produit):
        return None, "mots-cles absents (edition et/ou type de produit)"

    dates_trouvees = extraire_dates_page(texte_complet)
    if not dates_trouvees:
        return "moyenne", "mots-cles presents, aucune date detectee sur la page"

    if produit.date_sortie in dates_trouvees:
        return "forte", f"date de sortie attendue ({produit.date_sortie.isoformat()}) confirmee sur la page"

    # Des dates existent mais AUCUNE ne correspond -- rejet (probable
    # homonyme : ancienne extension avec sa propre date, deja passee).
    autres = ", ".join(d.isoformat() for d in dates_trouvees)
    return None, f"date(s) incompatible(s) trouvee(s) ({autres}), aucune ne correspond a {produit.date_sortie.isoformat()}"
