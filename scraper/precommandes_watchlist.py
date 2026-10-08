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
        automatiquement la detection une fois passee. None = date inconnue
        ou reportee : aucune validation de date (une page n'est jamais
        rejetee pour sa date), match toujours a confiance "moyenne".
    surveiller_jusqu_au : fin de la fenetre de detection si differente de
        date_sortie (defaut : date_sortie). Permet de continuer a detecter
        les RESTOCKS apres la sortie, sans toucher a la date servant a
        valider les pages (ex: ETB sorti le 16/09 mais suivi jusqu'a fin
        d'annee). Si date_sortie ET surveiller_jusqu_au sont None, le
        produit reste actif indefiniment.
    mots_cles_supplementaires : groupes de mots-cles ADDITIONNELS, dont
        chacun doit aussi avoir au moins un terme present (en plus des
        groupes edition et type) -- sert a distinguer un coffret d'une
        carte a l'unite du meme personnage (ex: tin Nymphali vs carte
        Nymphali ex isolee de la meme extension).
    alerte_disponibilite : suivi de DISPONIBILITE demande explicitement
        par Justok (04/10/2026, produits des 30 ans). Trois effets :
        (1) alerte des qu'une page devient commandable (rupture ->
        stock) OU apparait deja commandable sur une boutique deja
        balayee au moins une fois pour ce produit (premier balayage d'une
        boutique = reference silencieuse, cf. alerte_precommande) ;
        (2) message "Disponible" au lieu de "Precommande detectee" ;
        (3) alerte Telegram envoyee MEME si l'interrupteur global
        notifications.telegram (config.yaml) est coupe -- cet interrupteur
        reste actif pour tout le reste (cf. scan_precommandes.py).
    prioritaire : marque un produit auquel Justok tient particulierement --
        purement cosmetique (ajoute un ⭐ dans l'alerte Telegram, cf.
        alerte_precommande._texte_precommande), n'affecte AUCUNE logique de
        detection/suppression d'alerte. Ajoute le 18/08/2026 pour l'UPC
        Noctali, a la demande explicite de Justok.
    """
    nom: str
    mots_cles_edition: frozenset[str]
    mots_cles_type: frozenset[str]
    date_sortie: date | None
    prioritaire: bool = False
    surveiller_jusqu_au: date | None = None
    mots_cles_supplementaires: tuple[frozenset[str], ...] = ()
    alerte_disponibilite: bool = False
    # Mots (mots ENTIERS, accents/casse/ponctuation ignores) dont la presence
    # dans le TITRE rejette la page, et dans le TITRE OU la description pour
    # `mots_exclus_texte` -- cf. EXCLUSIONS_LOTS_ET_IMPORTS.
    mots_exclus_titre: frozenset[str] = frozenset()
    mots_exclus_texte: frozenset[str] = frozenset()
    # Mots (ENTIERS) d'un produit CONCURRENT : un titre qui en contient un
    # sans contenir aucun mot de `mots_cles_supplementaires` est rejete
    # (ex. Pokebox Amphinobi-ex vs Pokebox Nymphali-ex, 08/10/2026).
    concurrents_titre: frozenset[str] = frozenset()
    # True : au moins un mot-cle TYPE doit figurer dans le TITRE (pas seulement
    # dans la description) -- un "Pack coffret 30 ans" de revendeur dont la
    # description enumere ETB/bundle/mini tin ne doit pas matcher chacun de
    # ces produits.
    type_dans_titre: bool = False
    # True : uniquement la VERSION FRANCAISE (demande de Justok, 04/10/2026 :
    # "aucune autre langue") -- cf. langue_non_francaise().
    francais_uniquement: bool = False


# 04/10/2026, faux positifs reels recus sur Telegram (kwilytcg.com, nin-nin-game.com) :
#   - "Lot/bundle 30 ans", "Lot duopack 30 ans" : lots de revendeur melangeant
#     plusieurs produits (poster collection, tripack, ETB d'une autre extension,
#     "mini tin Illumis"...) -- la description contient "bundle"/"mini tin"/"ETB"
#     sans que la page vende le produit suivi ;
#   - "30th Anniversary Mini Tin Case Collection Vol.1 (10 Pack Box) [Ensky]" :
#     produit derive japonais (edition originale japonaise), pas le Mini Tin TCG FR.
# Un vrai produit suivi n'est jamais un "lot" dans son titre, ni une edition
# japonaise/importee (les produits suivis sont les produits FRANCAIS).
MOTS_LOTS_TITRE = frozenset({"lot", "lots", "duopack", "tripack", "duo pack", "tri pack"})
# Lots de revendeur "produit Pokemon + produit d'un AUTRE jeu" (snooop.gg,
# 05/10/2026 : "Bundle | Pokémon 30E Anniversaire Mini Tin | Rise 3 Boosters
# Prestige 2025") : ce ne sont pas les produits officiels suivis.
MOTS_AUTRES_JEUX_TITRE = frozenset({
    "lorcana", "rise", "riftbound", "one piece", "yu-gi-oh", "yugioh", "magic", "mtg",
    "dragon ball", "digimon", "flesh and blood", "star wars unlimited", "naruto", "union arena",
})
MOTS_IMPORTS_TEXTE = frozenset({
    "ensky", "case collection", "10 pack box", "japonaise", "japonais", "japanese",
    "edition japonaise", "japan version",
})
# --- Langue : uniquement le FRANCAIS (Justok, 04/10/2026) ---
# Une page est rejetee si son titre porte un marqueur de langue non francaise
# explicite, OU si ni son titre ni sa description ne contiennent aucun indice
# de francais (preuve POSITIVE exigee : un titre sans marqueur de langue,
# ex. "30th Celebration Booster Bundle", n'est pas assez pour affirmer FR).
# Limite assumee : une fiche FR au titre 100% anglais et sans le moindre mot
# francais dans le titre/la description serait ratee.
_RE_CODE_LANGUE_PONCTUE = re.compile(
    r"[-–—|(\[/]\s*(?:en|eng|jp|jap|kr|de|it|es|pt|cn|zh|th|ru|pl|nl)\s*(?:[)\]|/]|$)", re.IGNORECASE)
_RE_CODE_LANGUE_FIN_MAJ = re.compile(r"\s(?:EN|ENG|JP|KR|DE|IT|ES|PT|CN|TH)$")
MOTS_LANGUES_TITRE = frozenset({
    "english", "anglais", "anglaise", "japanese", "japonais", "japonaise", "korean", "coreen", "coreenne",
    "chinese", "chinois", "chinoise", "german", "allemand", "allemande", "deutsch", "italian", "italien",
    "italienne", "spanish", "espagnol", "espagnole", "portuguese", "portugais", "thai", "thailandais",
    "international version", "us version", "uk version", "english version", "version anglaise",
    "version japonaise", "version allemande",
})
MOTS_INDICE_FRANCAIS = frozenset({
    "fr", "francais", "francaise", "anniversaire", "coffret", "dresseur", "paquet", "boite", "precommande",
    "nymphali", "mentali", "noctali", "pokebox",
})


def langue_non_francaise(titre: str, description: str) -> str | None:
    """Raison du rejet si la page n'est pas clairement francaise, sinon None."""
    if _RE_CODE_LANGUE_PONCTUE.search(titre) or _RE_CODE_LANGUE_FIN_MAJ.search(titre):
        return "code de langue non francais dans le titre"
    mot = _mot_exclu(titre, MOTS_LANGUES_TITRE)
    if mot:
        return f"langue non francaise dans le titre ('{mot}')"
    if not _mot_exclu(f"{titre} {description}", MOTS_INDICE_FRANCAIS):
        return "aucun indice de francais (titre/description)"
    return None


# Suite du meme jour : "Pack coffret 30 ans" et "Gros pack 30ans + ME03/04"
# (kwilytcg.com) matchaient encore ETB, Bundle, Mini Tin et Pokebox via leur
# description -> le type de produit doit etre dans le TITRE.
EXCLUSIONS_LOTS_ET_IMPORTS = {
    "mots_exclus_titre": MOTS_LOTS_TITRE | MOTS_AUTRES_JEUX_TITRE | {"pack", "gros pack", "pack coffret"},
    "mots_exclus_texte": MOTS_IMPORTS_TEXTE,
    "type_dans_titre": True,
    "francais_uniquement": True,
}


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
            "coffret ultra premium",  # 08/10/2026 : "Coffret Ultra Premium Mentali ex" non reconnu
        }),
        mots_cles_type=frozenset({
            "mentali", "espeon",
        }),
        date_sortie=date(2026, 11, 6),
        surveiller_jusqu_au=date(2026, 12, 31),
        alerte_disponibilite=True,
        **EXCLUSIONS_LOTS_ET_IMPORTS,
    ),
    ProduitSurveille(
        nom="Collection Ultra-Premium — Umbreon (Noctali) 30e Anniversaire FR",
        mots_cles_edition=frozenset({
            "collection ultra premium", "ultra premium collection", "upc",
            "journee et soiree", "day and night",
            "coffret ultra premium",  # 08/10/2026 : "Coffret Ultra Premium Mentali ex" non reconnu
        }),
        mots_cles_type=frozenset({
            "noctali", "umbreon",
        }),
        date_sortie=date(2026, 11, 6),
        prioritaire=True,  # celle qui interesse le plus Justok (18/08/2026)
        surveiller_jusqu_au=date(2026, 12, 31),
        alerte_disponibilite=True,
        **EXCLUSIONS_LOTS_ET_IMPORTS,
    ),
    # --- Suivi de DISPONIBILITE des produits des 30 ans (demande de Justok,
    # 04/10/2026 : "prevenez-moi des qu'il y aura du restock" / "des qu'il
    # sera possible de precommander et/ou du stock"). L'entree ETB
    # d'origine (ci-dessus, sortie 16/09) a expire automatiquement : cette
    # nouvelle entree la remplace pour le SUIVI DES RESTOCKS. Le nom
    # differe VOLONTAIREMENT de l'ancienne (cle memoire = domaine|nom) :
    # les anciens etats memorises (periode precommande, alertes jamais
    # envoyees pendant la coupure Telegram du 19/09) auraient sinon
    # declenche une rafale d'alertes "stock" pour des ETB en vente depuis
    # des semaines. Fenetre : fin 2026 (a rallonger si les restocks
    # continuent).
    ProduitSurveille(
        nom="Coffret Dresseur d'Élite — 30e Anniversaire FR (suivi restock)",
        mots_cles_edition=frozenset({
            # Meme liste que l'entree d'origine (cf. son commentaire sur
            # "celebration" seul -- ne PAS ajouter "30 ans" ici : texte
            # marketing generique present sur d'autres ETB de 2026, ex.
            # ME06 Regne Delta, ce serait un faux positif).
            "30e anniversaire", "30eme anniversaire", "30th anniversary",
            "30th celebration",
            # Code d'extension (08/10/2026) : E.Leclerc nomme ses produits par code
            # ("Pokemon ME04 : coffret Dresseur d'Elite"), et la serie des 30 ans
            # est vendue sous "ME05.5" (dracaugames, tradingcardsxxx).
            "me05.5", "me 05.5", "me5.5",
            # E.Leclerc nomme la serie "Pokemon 30A" ("Pokemon 30A : Mini Tin
            # (modele aleatoire)", fiche verifiee le 08/10/2026).
            "pokemon 30a",
        }),
        mots_cles_type=frozenset({
            "dresseur d'elite", "dresseur elite", "etb", "elite trainer box",
        }),
        date_sortie=date(2026, 9, 16),
        surveiller_jusqu_au=date(2026, 12, 31),
        alerte_disponibilite=True,
        **EXCLUSIONS_LOTS_ET_IMPORTS,
    ),
    # Booster Bundle et Mini Tin : sortie initialement prevue le 02/10/2026
    # puis REPORTEE par les distributeurs (date non confirmee au
    # 04/10/2026) -> date_sortie=None, aucune validation de date (une page
    # affichant la nouvelle date ne doit pas etre rejetee).
    ProduitSurveille(
        nom="Booster Bundle — 30e Anniversaire (30th Celebration) FR",
        mots_cles_edition=frozenset({
            "30e anniversaire", "30eme anniversaire", "30th anniversary",
            "30th celebration",
            # Code d'extension (08/10/2026) : E.Leclerc nomme ses produits par code
            # ("Pokemon ME04 : coffret Dresseur d'Elite"), et la serie des 30 ans
            # est vendue sous "ME05.5" (dracaugames, tradingcardsxxx).
            "me05.5", "me 05.5", "me5.5",
            # E.Leclerc nomme la serie "Pokemon 30A" ("Pokemon 30A : Mini Tin
            # (modele aleatoire)", fiche verifiee le 08/10/2026).
            "pokemon 30a",
        }),
        mots_cles_type=frozenset({
            "booster bundle", "bundle", "paquet de boosters", "paquet de booster",
            # Nom FRANCAIS officiel sur la boite (photo envoyee par Justok le
            # 08/10/2026) : "30e Anniversaire -- Lot de boosters".
            "lot de boosters", "lot de booster",
            # Fiche reelle manquee (dracaugames.com, 08/10/2026) : "Pokemon -
            # Bundle / Lot de 6 boosters ME05.5 : 30e Anniversaire".
            "lot de 6 boosters",
        }),
        date_sortie=None,
        surveiller_jusqu_au=date(2026, 12, 31),
        alerte_disponibilite=True,
        **EXCLUSIONS_LOTS_ET_IMPORTS,
    ),
    ProduitSurveille(
        nom="Mini Tin — 30e Anniversaire (30th Celebration) FR",
        mots_cles_edition=frozenset({
            "30e anniversaire", "30eme anniversaire", "30th anniversary",
            "30th celebration",
            # Code d'extension (08/10/2026) : E.Leclerc nomme ses produits par code
            # ("Pokemon ME04 : coffret Dresseur d'Elite"), et la serie des 30 ans
            # est vendue sous "ME05.5" (dracaugames, tradingcardsxxx).
            "me05.5", "me 05.5", "me5.5",
            # E.Leclerc nomme la serie "Pokemon 30A" ("Pokemon 30A : Mini Tin
            # (modele aleatoire)", fiche verifiee le 08/10/2026).
            "pokemon 30a",
        }),
        mots_cles_type=frozenset({
            "mini tin", "mini boite", "mini coffret metal",
        }),
        date_sortie=None,
        surveiller_jusqu_au=date(2026, 12, 31),
        alerte_disponibilite=True,
        **EXCLUSIONS_LOTS_ET_IMPORTS,
    ),
    # Pokebox / Tin 30e Anniversaire Nymphali-ex (Sylveon ex Tin, 4
    # boosters + promo + carte oversize) : sortie annoncee le 04/12/2026
    # cote US, date FR non confirmee -> date_sortie=None. Mots-cles
    # volontairement stricts (pas de "tin" seul : sous-chaine de "destinees",
    # "tintin"...) pour ne PAS matcher les cartes Nymphali ex a l'unite de la
    # meme extension (faux positifs en rafale sur les boutiques de
    # singles) : le groupe supplementaire impose le personnage, le groupe
    # type impose un format coffret/boite.
    ProduitSurveille(
        nom="Pokébox / Tin — Nymphali ex (Sylveon ex Tin) 30e Anniversaire FR",
        mots_cles_edition=frozenset({
            "30e anniversaire", "30eme anniversaire", "30th anniversary",
            "30th celebration", "30 ans",
            "pokemon 30a",   # nom E.Leclerc de la serie (cf. ETB)
        }),
        mots_cles_type=frozenset({
            "pokebox", "poke box", "ex tin", "tin nymphali", "tin sylveon",
            "ex box", "pokemon ex box", "coffret pokemon ex",
            # 08/10/2026 (visuel envoye par Justok : une boite metal) : titres
            # reels du type "Tin Pokemon Nymphali-ex 30e Anniversaire" ou
            # "Boite metal Nymphali-ex" n'etaient pas reconnus. Jamais "tin"
            # seul (correspondance par sous-chaine : "martin", "mini tin").
            "tin pokemon", "pokemon tin", "tin 30", "boite metal", "boite en metal",
        }),
        mots_cles_supplementaires=(frozenset({"nymphali", "sylveon"}),),
        date_sortie=None,
        surveiller_jusqu_au=date(2027, 1, 31),
        alerte_disponibilite=True,
        **{**EXCLUSIONS_LOTS_ET_IMPORTS,
           # "Mini Tin 30e Anniversaire" (autre produit suivi) ne doit pas
           # passer pour la Pokebox via "tin pokemon"/"tin 30".
           "mots_exclus_titre": EXCLUSIONS_LOTS_ET_IMPORTS["mots_exclus_titre"] | {"mini"}},
        # 08/10/2026 : la Pokebox SOEUR "Amphinobi-ex" 30e Anniversaire
        # (plazatcg.com, pokemagic.fr) matchait via "nymphali" ailleurs sur la
        # page. Rejetee si son TITRE nomme Amphinobi sans nommer Nymphali ;
        # "Pokebox Nymphali ex et Amphinobi ex" (modele au choix) reste gardee.
        concurrents_titre=frozenset({"amphinobi", "greninja"}),
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
    """Produits dont la fenetre de surveillance n'est pas terminee (fin =
    surveiller_jusqu_au, a defaut date_sortie ; aucune des deux = actif
    sans limite) -- arret automatique de la detection au-dela (cf.
    docstring du module)."""
    aujourdhui = aujourdhui or date.today()
    actifs = []
    for p in PRODUITS_SURVEILLES:
        fin = p.surveiller_jusqu_au or p.date_sortie
        if fin is None or fin >= aujourdhui:
            actifs.append(p)
    return actifs


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
    a_supplementaires = all(
        any(_normaliser(mot) in texte_norm for mot in groupe)
        for groupe in produit.mots_cles_supplementaires
    )
    return a_edition and a_type and a_supplementaires


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


def _mot_exclu(texte: str, mots: frozenset[str]) -> str | None:
    """Premier mot/expression de `mots` present en MOT ENTIER dans `texte`
    (normalise) -- "lot" ne matche pas "pilote" ni "ballotin"."""
    if not mots:
        return None
    norm = f" {_normaliser(texte)} "
    for mot in sorted(mots):
        if f" {_normaliser(mot).strip()} " in norm:
            return mot
    return None


def _titre_sans_nom_officiel(titre: str, produit: ProduitSurveille) -> str:
    """Titre normalise, prive des noms officiels du produit qui contiennent
    eux-memes un mot exclu (08/10/2026, signale par Justok) : le Booster
    Bundle s'appelle officiellement "Lot de boosters" en francais, et "lot"
    (exclusion des lots de revendeur) rejetait donc la fiche officielle.
    Un vrai lot ("Lot de 3 lots de boosters...") garde un "lot" en dehors du
    nom officiel et reste exclu."""
    norm = f" {_normaliser(titre)} "
    for mot in sorted(produit.mots_cles_type, key=len, reverse=True):
        if _mot_exclu(mot, produit.mots_exclus_titre):
            norm = norm.replace(f" {_normaliser(mot).strip()} ", " ")
    return norm


def evaluer_correspondance(
    titre: str, texte_description: str, produit: ProduitSurveille,
    texte_exclusions: str | None = None,
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
        scrapable a ce stade).

    `texte_exclusions` : texte PROPRE au produit (description JSON-LD de la
    fiche) sur lequel chercher les mots exclus, quand `texte_description`
    est la page entiere. Bug reel du 08/10/2026 : les fiches 30e
    Anniversaire FR de missplaybros.com etaient rejetees ("japonais") a
    cause des AUTRES produits affiches sur la page (suggestions, derniers
    articles). None = page entiere (comportement d'origine)."""
    texte_complet = f"{titre} {texte_description}"
    texte_exclu = texte_complet if texte_exclusions is None else f"{titre} {texte_exclusions}"

    exclu = (_mot_exclu(_titre_sans_nom_officiel(titre, produit), produit.mots_exclus_titre)
             or _mot_exclu(texte_exclu, produit.mots_exclus_texte))
    if exclu:
        return None, f"exclu : lot ou edition importee ('{exclu}')"

    concurrent = _mot_exclu(titre, produit.concurrents_titre)
    if concurrent and not any(_mot_exclu(titre, groupe) for groupe in produit.mots_cles_supplementaires):
        return None, f"autre produit dans le titre ('{concurrent}')"

    if not titre_correspond_produit(texte_complet, produit):
        return None, "mots-cles absents (edition et/ou type de produit)"

    if produit.francais_uniquement:
        raison_langue = langue_non_francaise(titre, texte_description)
        if raison_langue:
            return None, f"version non francaise : {raison_langue}"

    if produit.type_dans_titre:
        titre_norm = _normaliser(titre)
        if not any(_normaliser(mot) in titre_norm for mot in produit.mots_cles_type):
            return None, "type de produit absent du titre (page generique ou lot)"

    if produit.date_sortie is None:
        return "moyenne", "mots-cles presents (date de sortie inconnue ou reportee : pas de validation de date)"

    dates_trouvees = extraire_dates_page(texte_complet)
    if not dates_trouvees:
        return "moyenne", "mots-cles presents, aucune date detectee sur la page"

    if produit.date_sortie in dates_trouvees:
        return "forte", f"date de sortie attendue ({produit.date_sortie.isoformat()}) confirmee sur la page"

    # Des dates existent mais AUCUNE ne correspond -- rejet (probable
    # homonyme : ancienne extension avec sa propre date, deja passee).
    autres = ", ".join(d.isoformat() for d in dates_trouvees)
    return None, f"date(s) incompatible(s) trouvee(s) ({autres}), aucune ne correspond a {produit.date_sortie.isoformat()}"
