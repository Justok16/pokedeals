"""
Normalisation de texte + filtre de pertinence des annonces pour PokeDeals.

Extrait de main.py le 16/08/2026 (premier module du decoupage progressif
de main.py, cf. SESSION_NOTES.md) : fonctions PURES, sans etat partage ni
appel reseau, centrees sur annonce_pertinente() -- le filtre qui decide si
une annonce eBay/Vinted/Leboncoin correspond bien a la carte recherchee
(bon Pokemon, bon numero, bonne langue, pas un lot/objet derive/carte
gradee...).

_nom_neutre_entre_langues() reste dans main.py : elle depend de
CT_NOMS_EN, defini bien plus loin dans main.py (table de correspondance
FR->EN utilisee par le moteur de cote), une dependance vers l'avant qui
sort du perimetre "texte pur" de ce module.
"""
from __future__ import annotations

import re
import unicodedata


# ------------------- Normalisation de texte -------------------

def normaliser(texte: str) -> str:
    """minuscules + sans accents + sans tirets (méga-dracaufeu -> mega dracaufeu)."""
    t = unicodedata.normalize("NFD", (texte or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.replace("-", " ").replace("_", " ").replace(".", " ")


# ------------------- Filtres de pertinence -------------------

RE_NUMERO = re.compile(r"(\d{1,3})\s*/\s*(\d{2,3})")
# V38 : certains vendeurs écrivent le numéro avec un tiret ou une espace
# au lieu du slash ("199-165", "199 165"). Sans ce filtre de secours, ces
# annonces étaient systématiquement rejetées ("aucun numéro dans le
# titre"), même quand tout le reste du titre était correct. On ne
# l'utilise qu'en repli, après avoir essayé le slash — le slash reste
# prioritaire pour éviter de capturer par erreur une date ou une
# référence interne au vendeur (ex. "025-09").
RE_NUMERO_SEPARATEUR = re.compile(r"\b(\d{1,3})[-\s](\d{2,3})\b")

# 1) L'annonce doit contenir AU MOINS UN de ces indices de "vraie carte"
INDICES_CARTE = [
    "carte", "card", "carta", "karte",       # carte en FR/EN/IT-ES/DE
    "tcg", "holo", "reverse", "full art", "fa ",
    "promo", "alt ", "alternative", "secrete", "secret",
    " ar", "ar ", "sar", "sir", "mhr", "chr",
    " ex", "ex ", " gx", "gx ", "vstar", "vmax", " nm", "nm ",
    "near mint", "mint", "psa", "pca",       # (psa/pca restent exclus ensuite,
]                                             #  mais prouvent que c'est une carte)

# 2) Mots qui signalent que ce N'EST PAS une carte à l'unité non gradée
EXCLUSIONS = [
    # Lots & produits scellés
    "lot de", "lot ", " lots", "x5", "x10", "x20", "x50", "x100",
    "display", "booster", "coffret", "etb", "elite trainer", "tin ",
    "blister", "tripack", "bundle", "collection complete", "set complet",
    "classeur", "album", "a choisir", "au choix",
    # Contrefaçons & produits dérivés de cartes
    "proxy", "proxies", "fake", "replique", "custom", "metal", "jumbo",
    "oversize", "gold plated", "plastifiee", "sticker", "autocollant",
    # Cartes gradées
    "psa", "pca", "bgs", "cgc", "gradee", "graded", "grade 8", "grade 9", "grade 10",
    # Cartes abîmées (fausseraient la cote vers le bas)
    "abim", "damaged", "played", "poor", "endommag",
    # Vêtements & accessoires
    "t shirt", "tee shirt", "tshirt", "pull", "sweat", "hoodie", "veste",
    "casquette", "bonnet", "pyjama", "chaussette", "chausson", "basket",
    "deguisement", "costume", "sac ", "sacoche", "cartable", "trousse",
    # Jouets & objets
    "peluche", "figurine", "funko", "pop!", "jouet", "lego", "puzzle",
    "piece", "medaille", "mug", "tasse", "gourde", "porte cle", "porte cles",
    "coque", "poster", "tapis", "protege", "sleeve", "toploader",
    # V17 : accessoires de protection/présentation (pas la carte elle-même)
    "vitrine", "affichage", "protection", "presentoir", "support",
    "boitier", "boite de protection", "etui", "pochette", "cadre",
    "magnetique", "acrylique", "screwdown", "top loader", "porte carte",
    "jeu video", "nintendo switch", "game boy", "ds ", "3ds",
    "livre", "manga", "dvd", "blu ray",
]

# Petits mots à ignorer quand on extrait le nom du Pokémon
MOTS_VIDES = {"carte", "pokemon", "ex", "gx", "v", "vstar", "vmax", "de", "n",
              "la", "le", "et", "team", "jp", "fr", "sv2a",
              "sir", "sar", "ar", "mhr"}
# Noms de sets : descriptifs, souvent absents des titres -> jamais exigés
MOTS_SETS = {"heros", "transcendants", "flammes", "fantasmagoriques",
             "equilibre", "parfait", "chaos", "ascendant", "nuit", "noire",
             "serie", "151",
             # V16.1 : descriptifs de rareté/produit (jamais exigés dans un titre)
             "trainer", "gallery", "promo", "alternative", "ultra", "rare",
             "celeste", "prismatiques", "mascarade", "crepusculaire",
             "aventures", "ensemble", "stars", "etincelantes", "de", "lilie"}

# V16 : gestion des langues.
# - Suffixe ajouté aux requêtes eBay/Vinted/Leboncoin selon la langue.
SUFFIXES_LANGUE = {"jp": " japonaise", "en": " anglaise",
                   "kr": " coréenne", "cn": " chinoise"}
# - Marqueurs devant figurer dans le TITRE pour valider la langue.
#   Les marqueurs courts (<= 3 lettres) sont comparés mot à mot pour
#   éviter les faux positifs ("kr" à l'intérieur d'un autre mot, etc.).
MARQUEURS_LANGUE = {
    # NB : les codes de SET (sv2a, m2a...) ne sont PAS des marqueurs de
    # langue — une carte 151 coréenne ou chinoise porte aussi "sv2a". La
    # langue se prouve par un mot de langue, des caractères, ou la
    # localisation eBay, jamais par le code de set.
    "jp": ["japonaise", "japonais", "japanese", "japon", "jpn", "jap", "jp",
           # V30 : formes ITALIENNE, ESPAGNOLE, ALLEMANDE et NÉERLANDAISE.
           # Cas vécu : une annonce Vinted titrée « Pokémon Pikachu AR
           # 173/165 – Giapponese – Art Rare » (vendeur italien, carte
           # japonaise) a franchi le filtre FR et failli être comparée à
           # la cote française de 114,42€. Le mot était dans le titre, en
           # clair — on ne le connaissait simplement pas.
           "giapponese", "giapponesi", "giappone",
           "japones", "japonesa", "japonesas",
           "japanisch", "japanische", "japans"],
    "en": ["anglaise", "anglais", "english", "eng",
           "inglese", "ingles", "englisch"],
    "kr": ["coreenne", "coreen", "korean", "korea", "kor", "kr",
           "coreano", "coreana", "koreanisch", "koreaans"],
    "cn": ["chinoise", "chinois", "chinese", "china", "zh", "cn",
           "cinese", "cinesi", "chino", "chinesisch"],
    # V20 : langues EUROPÉENNES non désirées. Une carte italienne/allemande/
    # espagnole au même numéro qu'une française vaut souvent moins et créait
    # de faux deals. On les détecte par le mot de langue explicite ET par des
    # mots très caractéristiques présents dans les annonces ou sur la carte.
    "it": ["italienne", "italien", "italian", "italiano", "italia",
           "condizioni", "come da foto", "carta", "fase",
           # V22.8 : mots relevés dans de vraies annonces Vinted italiennes
           # qui avaient un titre parfaitement « neutre » (le piège : seule
           # la description trahissait la langue).
           "comprare", "spedisco", "spedizione", "chiedere", "informazioni",
           "lingua", "espansione", "numero della", "nome della", "carte da",
           "perfette", "ottime", "buone condizioni", "regalo", "prezzo",
           "disponibile", "vendo", "scambio", "grazie", "salve", "ciao"],
    "de": ["allemande", "allemand", "german", "deutsch", "zustand", "karte", "sammlung"],
    "es": ["espagnole", "espagnol", "spanish", "espanol", "espana", "estado", "carta espanola"],
    "pt": ["portugaise", "portugais", "portuguese", "portugues"],
    "nl": ["nederlands", "kaart"],
}
# Langues à REJETER pour une carte française (tout sauf le français).
LANGUES_NON_FR = ("jp", "en", "kr", "cn", "it", "de", "es", "pt", "nl")

# V22.8 : formules signalant une ENCHÈRE DÉGUISÉE. Le vendeur affiche un
# prix dérisoire (1€) et invite à surenchérir en commentaire — le prix
# affiché n'a alors aucun rapport avec le prix de vente réel.
SIGNAUX_ENCHERE = (
    "non comprare", "ne pas acheter", "n achetez pas", "nachetez pas",
    "do not buy", "dont buy", "enchere", "encheres", "asta", "offerta",
    "faire offre", "meilleure offre", "au plus offrant", "plus offrant",
    "chiedere per informazioni", "mp pour prix", "prix en mp",
    "commentaire pour prix", "spedisco energia", "spedisco solo energia",
)
TOUS_MARQUEURS = [m for lst in MARQUEURS_LANGUE.values() for m in lst]


def _marqueur_present(marqueur: str, texte_norm: str, jetons: list[str]) -> bool:
    if len(marqueur) <= 3:
        return marqueur in jetons
    return marqueur in texte_norm


# =====================================================================
# V28 : CODES DE SET JAPONAIS = PREUVE QUE LA CARTE N'EST PAS FRANÇAISE
# ---------------------------------------------------------------------
# Cas vécu (fausse alerte Telegram) : une annonce Vinted titrée
# « Pikachu AR sv2a 173/165 — État parfait », photo d'une carte
# CORÉENNE, comparée à la cote FRANÇAISE de 114,42€ -> faux profit
# annoncé de +84,91€.
#
# Pourquoi tous les filtres l'ont laissée passer :
#   - aucun caractère coréen dans le TITRE (seulement sur la photo)
#   - aucun mot de langue ("coréenne", "korean"...)
#   - bon Pokémon, bon numéro 173/165
#   - et le filtre "preuve de français" a trouvé « état » et
#     « parfait »... qui prouvent seulement que le VENDEUR est
#     français, pas que la CARTE l'est. Un vendeur français vend
#     très bien une carte coréenne.
#
# Le vrai signal : « sv2a » est le code de set JAPONAIS de la série
# 151, porté par les versions JP et KR. La version FRANÇAISE ne le
# porte JAMAIS (elle affiche EV3.5, 151, Écarlate & Violet).
# Ce code ne dit pas LAQUELLE des langues asiatiques (JP et KR le
# partagent), mais il exclut le français avec certitude.
#
# Effet double : supprime ces fausses alertes ET nettoie les cotes FR,
# qui absorbaient des cartes japonaises au même numéro (constaté :
# « Bulbizarre AR SFG 9.5 – SV2a 151 (166/165) » à 70€ comptée dans
# le bas-marché de la cote française).
# =====================================================================
SETS_ASIATIQUES = {
    # Écarlate & Violet japonais (sv...)
    "sv1", "sv1a", "sv1s", "sv1v", "sv2", "sv2a", "sv2d", "sv2p",
    "sv3", "sv3a", "sv4", "sv4a", "sv4k", "sv4m", "sv5a", "sv5k", "sv5m",
    "sv6", "sv6a", "sv7", "sv7a", "sv8", "sv8a", "sv9", "sv9a",
    "sv10", "sv11b", "sv11w",
    # Épée & Bouclier japonais (s...)
    "s8b", "s9a", "s10a", "s11", "s12", "s12a",
    # Méga-Évolution japonais (m...)
    "m1l", "m1s", "m2", "m2a", "m3", "m4", "m5", "mc",
    # Promos japonaises
    "s-p",
}


def code_set_asiatique(jetons: list[str]) -> str | None:
    """Renvoie le code de set japonais trouvé dans les jetons, sinon None.

    Comparaison mot à mot : « sv2a » doit être un jeton isolé, pour ne
    pas confondre avec un fragment d'un autre mot.
    """
    for jeton in jetons:
        if jeton in SETS_ASIATIQUES:
            return jeton
    return None


# V18 : détection de caractères asiatiques dans le titre ORIGINAL (avant
# normalisation, qui les supprimerait). Une annonce contenant フシギダネ,
# ピカチュウ, 리자몽, 妙蛙种子... est forcément une carte étrangère, même si
# le reste du titre est en français.
# V19 : on distingue MAINTENANT la langue asiatique (jp / kr / cn), car une
# carte japonaise et sa version coréenne partagent le MÊME numéro. Sans
# cette distinction, une annonce coréenne (moins chère) polluerait la cote
# japonaise et inversement — le même piège que FR/JP.


def _script_asiatique(texte: str) -> str | None:
    """Renvoie 'jp', 'kr' ou 'cn' selon les caractères présents, sinon None.
    - Hangul (한글)            -> 'kr' (sans ambiguïté)
    - Hiragana/Katakana (かな) -> 'jp' (sans ambiguïté)
    - Idéogrammes seuls        -> 'cn' (Hanzi ; les kanji japonais isolés sont
      rares dans les titres d'annonces, qui contiennent presque toujours des
      kana ; on tranche donc côté chinois par défaut, la localisation eBay
      restant le signal prioritaire pour lever un éventuel doute).
    """
    a_hangul = a_kana = a_ideo = False
    for ch in texte or "":
        code = ord(ch)
        if 0xAC00 <= code <= 0xD7A3:            # hangul
            a_hangul = True
        elif 0x3040 <= code <= 0x30FF:          # hiragana + katakana
            a_kana = True
        elif (0x4E00 <= code <= 0x9FFF
              or 0x3400 <= code <= 0x4DBF):     # idéogrammes CJK
            a_ideo = True
    if a_hangul:
        return "kr"
    if a_kana:
        return "jp"
    if a_ideo:
        return "cn"
    return None


def extraire_numero(texte: str) -> str | None:
    m = RE_NUMERO.search(texte or "")
    return f"{int(m.group(1))}/{int(m.group(2))}" if m else None


def extraire_numero_annonce(titre: str) -> str | None:
    """Comme extraire_numero, mais avec un repli tiret/espace ('199-165',
    '199 165'). Réservé aux TITRES D'ANNONCES (eBay/Vinted) : le nom de la
    carte dans config.yaml doit rester sur le format strict X/Y, sinon un
    tiret dans "Méga-Dracaufeu" pourrait être pris à tort pour un numéro.
    """
    direct = extraire_numero(titre)
    if direct:
        return direct
    m = RE_NUMERO_SEPARATEUR.search(titre or "")
    return f"{int(m.group(1))}/{int(m.group(2))}" if m else None


# V17.4 : les cartes Nuit Noire françaises (set PBL) ont un numéro SANS
# dénominateur ("116", "120"...) au lieu du format "X/Y". Sans traitement
# spécial, "Darkrai ex 116" et "Darkrai ex 120" deviennent indiscernables
# (même Pokémon, filtre incapable de distinguer 116 de 120). On extrait donc
# ce numéro nu du NOM de carte, et on l'exige comme un token isolé dans le
# titre, en rejetant tout autre numéro nu du même Pokémon.
RE_NUMERO_NU = re.compile(r"\b(\d{2,3})\b")


def numero_nu_voulu(nom_carte: str) -> str | None:
    """Renvoie le numéro nu (ex '116') si le nom en contient un ET n'a pas
    de numéro au format X/Y. Sinon None."""
    if extraire_numero(nom_carte):
        return None  # déjà un numéro X/Y : géré par la voie normale
    m = RE_NUMERO_NU.search(nom_carte or "")
    return m.group(1) if m else None


def numeros_nus_titre(titre: str) -> list[str]:
    """Tous les numéros nus (2-3 chiffres) présents dans un titre normalisé,
    en excluant ceux qui font partie d'un format X/Y (déjà gérés ailleurs)."""
    t = titre or ""
    # On retire d'abord les 'X/Y' pour ne pas capturer leurs composantes.
    sans_fraction = RE_NUMERO.sub(" ", t)
    return RE_NUMERO_NU.findall(sans_fraction)


def mots_requis(nom_carte: str) -> list[str]:
    """Mots distinctifs de la carte, TOUS exigés dans le titre.
    'Méga-Dracolosse ex 290/217' -> ['mega', 'dracolosse']
    'Zoroark de N ex héros transcendants' -> ['zoroark']
    """
    return [mot for mot in normaliser(nom_carte).split()
            if len(mot) >= 3 and mot not in MOTS_VIDES and mot not in MOTS_SETS
            and not any(c.isdigit() for c in mot)]


# V16.1 : pour une carte SANS numéro (promo, Trainer Gallery), le type de
# carte (vmax / vstar / v / gx / ex) DOIT rester distinctif, sinon une V
# et une VMAX du même Pokémon deviennent indiscernables. On garde donc ces
# marqueurs de rareté que mots_requis() écarte normalement.
TYPES_CARTE = {"vmax", "vstar", "gx", "ex", "v"}


def mots_requis_stricts(nom_carte: str) -> list[str]:
    base = mots_requis(nom_carte)
    for mot in normaliser(nom_carte).split():
        if mot in TYPES_CARTE and mot not in base:
            base.append(mot)
    return base


# =====================================================================
# V26 : PREUVE POSITIVE DE FRANÇAIS (annonces Vinted uniquement)
# ---------------------------------------------------------------------
# Sur eBay, _localisation_incoherente écarte déjà TOUTE annonce non
# localisée en France quand la carte recherchée est française —
# italiennes comprises. Rien à ajouter de ce côté.
#
# Vinted, lui, ne fournit aucun pays exploitable. Le filtre habituel
# exige le nom FRANÇAIS du Pokémon, ce qui suffit pour Dracaufeu : un
# vendeur italien n'écrit jamais « Dracaufeu ». Mais le nom ne prouve
# RIEN pour les Pokémon qui s'écrivent pareil dans toutes les langues :
# Mew, Pikachu, Mewtwo, Lucario, Gardevoir, Darkrai, Morpeko, Latias,
# Lugia, Zoroark. Un titre « Mew ex 205/165 » est compatible avec les
# versions FR, JP, KR, IT, EN, DE et ES à la fois — elles portent toutes
# le même numéro. C'est exactement là que les italiennes passaient.
#
# Le danger n'est PAS d'alerter sur une carte qui n'existe pas en
# français : c'est de comparer une italienne à 40€ à la COTE FRANÇAISE
# de 40€, alors que l'italienne en vaut 25.
# =====================================================================
MARQUEURS_FRANCAIS = (
    "francaise", "francais", "france",
    # V39 : retrait de "etat", "envoi", "envoie", "livraison", "expedition",
    # "merci", "bonjour", "rapide", "soignee", "jouee" et des formules de
    # prix ("prix ferme", "port compris"...). Même raisonnement que pour
    # "vf"/"parfait" retirés à la session précédente : ces mots prouvent
    # que le VENDEUR écrit en français, pas que la CARTE l'est. Un vendeur
    # français vend très bien une carte japonaise ou coréenne en écrivant
    # "état parfait, envoi rapide, merci". Ne restent que les mots qui
    # décrivent explicitement la nationalité de la carte elle-même.
    "neuve", "neuf",
)


def preuve_francais(texte: str) -> bool:
    """Un mot typiquement français figure-t-il dans l'annonce ?"""
    t = normaliser(texte)
    jetons = t.split()
    return any(_marqueur_present(m, t, jetons) for m in MARQUEURS_FRANCAIS)


def _pays_ebay(plateforme: str) -> str | None:
    """Extrait le code pays d'une plateforme 'eBay (JP)' -> 'jp'. None sinon."""
    p = str(plateforme or "")
    if p.startswith("eBay (") and p.endswith(")"):
        code = p[6:-1].strip().lower()
        return code or None
    return None


# Correspondance pays eBay -> langue de la carte
_PAYS_VERS_LANGUE = {"jp": "jp", "kr": "kr", "cn": "cn"}


def annonce_pertinente(titre: str, nom_carte: str, langue: str = "fr", alias: str = "",
                       plateforme: str = "") -> tuple[bool, str]:
    """Filtre strict : (pertinent, raison).

    V18 : `plateforme` permet d'utiliser la localisation eBay comme signal
    de langue. Une annonce "eBay (JP)" au titre 100% français est bien une
    carte japonaise (localisée au Japon) : elle doit être routée vers
    l'entrée japonaise, pas vers l'entrée française.
    """
    t = normaliser(titre)
    # V39 : neutraliser "non gradée" / "ungraded" AVANT le test des mots
    # exclus. La correction faite dans _etat_ok() ne suffisait pas : cette
    # fonction-ci a sa PROPRE liste (EXCLUSIONS, qui contient aussi "gradee"
    # et "graded") et elle est testée plus tôt dans le pipeline. Une annonce
    # « Dracaufeu ex 199/165 non gradée » était donc encore rejetée ici,
    # avant même d'atteindre le correctif de la session précédente.
    for negation in ("non gradee", "non-gradee", "pas gradee",
                     "ungraded", "not graded", "no grading", "sans grading"):
        t = t.replace(negation, "")
    if not t.strip():
        return False, "titre vide"

    # 1) Exclusions d'abord (vêtements, lots, scellé, gradées, objets...)
    for mot in EXCLUSIONS:
        if mot in t:
            return False, f"exclue ('{mot.strip()}')"

    # 2) Doit ressembler à une carte
    if not any(ind in f" {t} " for ind in INDICES_CARTE):
        return False, "pas une carte (aucun indice carte/holo/promo...)"

    # 2bis) Cohérence de LANGUE. Une carte coréenne vaut souvent moins que
    #    sa jumelle japonaise (même numéro !) : les mélanger fausserait les
    #    cotes. V19 : on distingue finement jp / kr / cn.
    #    Signaux de langue, par ordre de fiabilité :
    #      1. script du titre (hangul=kr, kana=jp, idéogrammes=cn)
    #      2. localisation eBay (JP/KR/CN)
    #      3. marqueurs texte ("korean", "japonaise"...)
    script = _script_asiatique(titre)              # 'jp'/'kr'/'cn'/None
    pays = _pays_ebay(plateforme)
    langue_du_pays = _PAYS_VERS_LANGUE.get(pays) if pays else None
    titre_a_des_caracteres_asiatiques = script is not None
    origine_asiatique = titre_a_des_caracteres_asiatiques or bool(langue_du_pays)
    jetons_langue = t.split()

    # Quelle(s) langue(s) asiatique(s) l'annonce revendique-t-elle par son texte ?
    langues_marquees = {lg for lg, mots in MARQUEURS_LANGUE.items()
                        if any(_marqueur_present(mm, t, jetons_langue) for mm in mots)}

    if langue in (None, "", "fr"):
        if origine_asiatique or langues_marquees:
            return False, "carte étrangère (caractères/origine) hors recherche FR"
        # V28 : un code de set JAPONAIS (sv2a, m2a, s8b...) dans le titre
        # prouve que la carte n'est pas française — même si le vendeur, lui,
        # écrit en français. Signal factuel, pas du vocabulaire.
        code_jp = code_set_asiatique(jetons_langue)
        if code_jp:
            return False, (f"carte étrangère : code de set japonais "
                           f"'{code_jp}' (une carte FR n'en porte jamais)")
    else:
        # Carte asiatique (jp/kr/cn). Elle doit correspondre à SA langue et
        # rejeter les signaux d'une AUTRE langue asiatique.
        autres = {"jp", "kr", "cn"} - {langue}
        # Signal contradictoire = l'annonce pointe clairement vers une autre langue
        if script in autres:
            return False, f"script {script} ≠ langue {langue}"
        if langue_du_pays in autres:
            return False, f"localisation {langue_du_pays} ≠ langue {langue}"
        if langues_marquees and langue not in langues_marquees and not (script == langue or langue_du_pays == langue):
            return False, f"marqueur {langues_marquees} ≠ langue {langue}"
        # Signal POSITIF requis : au moins un indice confirme la bonne langue
        confirme = (script == langue
                    or langue_du_pays == langue
                    or langue in langues_marquees)
        if not confirme:
            return False, f"langue '{langue}' non confirmée dans le titre"

    # 3) Cohérence Méga : une carte Méga ne pollue pas une recherche non-Méga
    #    et inversement. ATTENTION : "méga" peut aussi venir du NOM DU SET
    #    "Méga-Évolution" (ex. un Bulbizarre de ce set n'est PAS une carte
    #    Méga). On ne compte donc "méga" comme marqueur de carte Méga que
    #    s'il n'est pas immédiatement suivi de "évolution"/"evolution".
    requis = mots_requis(nom_carte)
    jetons = t.split()
    titre_mega = False
    for i, jet in enumerate(jetons):
        if jet in ("mega", "m"):
            suivant = jetons[i + 1] if i + 1 < len(jetons) else ""
            if suivant not in ("evolution", "evolutions"):
                titre_mega = True
                break
    carte_mega = "mega" in requis
    if titre_mega and not carte_mega:
        return False, "carte Méga hors recherche"
    if carte_mega and not titre_mega:
        return False, "'mega' absent du titre"

    # 4) Le nom du Pokémon (mot distinctif principal) doit être présent.
    #    V16 : un alias (ex. Tortank pour Blastoise) est aussi accepté,
    #    car les vendeurs français titrent souvent les cartes étrangères
    #    avec le nom français du Pokémon.
    pokemon = next((m for m in requis if m != "mega"), None)
    noms_acceptes = [pokemon] if pokemon else []
    if alias:
        noms_acceptes += [m for m in normaliser(alias).split() if len(m) >= 3]
    if noms_acceptes and not any(n in t for n in noms_acceptes):
        return False, f"'{pokemon}' (ou alias) absent du titre"

    # 5) Le NUMÉRO de carte est la preuve la plus fiable.
    #    V15 : si la carte recherchée porte un numéro, il est OBLIGATOIRE
    #    dans le titre de l'annonce.
    #    Pourquoi ? Un "Dracaufeu" à 5€ et un "Dracaufeu ex 199/165" à
    #    200€ portent le même nom : sans numéro, impossible de trancher.
    #    Une annonce sans numéro est donc écartée des cotes ET des alertes.
    #    On rate quelques annonces, mais on élimine les fausses cotes —
    #    et une cote fausse coûte bien plus cher qu'une annonce ratée.
    numero_voulu = extraire_numero(nom_carte)
    numero_annonce = extraire_numero_annonce(titre)
    if numero_voulu:
        if not numero_annonce:
            return False, "aucun numéro dans le titre (exigé depuis V15)"
        if numero_annonce != numero_voulu:
            return False, f"mauvais numéro ({numero_annonce} != {numero_voulu})"
        # bon numéro + bon pokémon : suffisant, on s'arrête là
    else:
        # Le nom recherché n'a pas de numéro X/Y (ex. versions SIR, promos,
        # TG, ou cartes PBL Nuit Noire à numéro nu). On exige tous les mots
        # distinctifs, EN CONSERVANT le type de carte (vmax/v/ex...) pour ne
        # pas confondre une V et une VMAX du même Pokémon. Le nom principal
        # peut être couvert par l'alias.
        jetons_titre = t.split()
        for mot in mots_requis_stricts(nom_carte):
            if mot == "mega":
                continue
            if mot == pokemon and alias and any(
                    n in t for n in normaliser(alias).split() if len(n) >= 3):
                continue  # nom principal couvert par l'alias
            # Les types de carte se comparent mot à mot ("v" ne doit pas
            # matcher le "v" de "vmax"). Le nom PRINCIPAL du Pokémon aussi :
            # sans ça, "mew" est considéré présent dans "mewtwo" (sous-
            # chaîne), et une carte sans numéro pourrait valider une
            # annonce d'un AUTRE Pokémon au nom proche. Les autres mots
            # (noms de sets composés, etc.) restent en sous-chaîne, plus
            # tolérants et sans ce risque de confusion entre Pokémon.
            if mot in TYPES_CARTE or mot == pokemon:
                if mot not in jetons_titre:
                    return False, f"'{mot}' absent du titre (mot entier requis)"
            elif mot not in t:
                return False, f"'{mot}' absent du titre"

        # V17.4 : cartes PBL à numéro nu (Nuit Noire FR : "116", "120"...).
        # Le numéro voulu DOIT figurer dans le titre, et aucun AUTRE numéro
        # nu ne doit y figurer (sinon "Darkrai ex 120" matcherait la 116).
        num_nu = numero_nu_voulu(nom_carte)
        if num_nu:
            nus = numeros_nus_titre(titre)
            if num_nu not in nus:
                return False, f"numéro {num_nu} absent du titre"
            autres = [n for n in nus if n != num_nu]
            if autres:
                return False, f"autre numéro présent ({autres[0]} ≠ {num_nu})"
            # Numéro nu exigé et présent : on NE rejette PAS sur numero_annonce
            # (le titre peut aussi contenir un X/Y, ex '116/086' — cohérent).
            return True, "ok"

        # ... et refuser une annonce qui, elle, porte un numéro X/Y : une carte
        # sans numéro (SIR non numérotée) n'est pas une carte numérotée.
        if numero_annonce:
            return False, "annonce numérotée ≠ version sans numéro (SIR)"

    return True, "ok"
