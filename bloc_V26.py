# =====================================================================
#  POKÉDEALS — BLOC V26
#  Preuve positive de français sur les annonces VINTED
# =====================================================================
#
#  À QUOI ÇA SERT
#  --------------
#  Sur eBay, la fonction _localisation_incoherente écarte déjà TOUTE
#  annonce non localisée en France quand la carte recherchée est
#  française — italiennes comprises. Rien à faire de ce côté.
#
#  Vinted, lui, ne fournit aucun pays exploitable. Une annonce italienne
#  au titre neutre y est indiscernable d'une française. C'est de là que
#  viennent les alertes sur des cartes italiennes.
#
#  Ce bloc ne touche QUE le déclenchement des alertes. Les annonces
#  Vinted n'entrent jamais dans le calcul des cotes (obtenir_cote ne
#  reçoit que les annonces eBay) : aucun risque d'effet de bord.
#
#  Aucun format de données ne change -> PURGE_VERSION reste à 20.
#
#  CE QU'IL FAUT FAIRE
#  -------------------
#    PARTIE 1 : à INSÉRER dans main.py
#    PARTIE 2 : à REMPLACER dans main.py
#    PARTIE 3 : à AJOUTER (temporaire, 1 seul scan)
#
# =====================================================================


# =====================================================================
#  PARTIE 1 — À INSÉRER
# ---------------------------------------------------------------------
#  Où : juste APRÈS la fonction `mots_requis_stricts`
#       et AVANT la fonction `_pays_ebay`.
#
#  Note : ce code utilise CT_NOMS_EN, qui est défini plus BAS dans
#  main.py (section Cardtrader). C'est normal et ça fonctionne : Python
#  ne résout le nom qu'au moment de l'appel, pas à la lecture du fichier.
# =====================================================================

# V26 : PREUVE POSITIVE DE FRANÇAIS (annonces Vinted uniquement).
# Le filtre habituel exige le nom FRANÇAIS du Pokémon, ce qui suffit
# pour Dracaufeu : un vendeur italien n'écrit jamais « Dracaufeu ».
# Mais le nom ne prouve RIEN pour les Pokémon qui s'écrivent pareil dans
# toutes les langues : Mew, Pikachu, Mewtwo, Lucario, Gardevoir, Darkrai,
# Morpeko, Latias, Lugia, Zoroark. Un titre « Mew ex 205/165 » est
# compatible avec la version FR, JP, KR, IT, EN, DE et ES à la fois —
# elles portent toutes le même numéro. C'est exactement là que les
# italiennes passaient, et le danger n'est pas d'alerter sur une carte
# inexistante en français : c'est de comparer une italienne à 40€ à la
# COTE FRANÇAISE de 40€, alors que l'italienne en vaut 25.
MARQUEURS_FRANCAIS = (
    "francaise", "francais", "france", "vf",
    "neuve", "neuf", "etat", "envoi", "envoie", "livraison", "expedition",
    "vends", "vendue", "achat", "acheteur", "merci", "bonjour",
    "rapide", "soignee", "parfait", "jouee",
    "prix ferme", "port compris", "port offert", "main propre",
)


def _nom_neutre_entre_langues(nom_carte: str) -> bool:
    """Le nom du Pokémon s'écrit-il pareil en français et en anglais ?

    'Dracaufeu ex 199/165' -> False : le nom prouve à lui seul la langue
    'Mew ex 205/165'       -> True  : le nom ne prouve rien

    Un Pokémon absent de CT_NOMS_EN est traité comme NEUTRE : mieux vaut
    exiger une preuve inutile que laisser passer une italienne.
    """
    mots = [m for m in mots_requis(nom_carte) if m != "mega"]
    if not mots:
        return True
    fr = mots[0]
    en = normaliser(CT_NOMS_EN.get(fr, ""))
    if not en:
        return True
    return en == fr


def preuve_francais(texte: str) -> bool:
    """Un mot typiquement français figure-t-il dans l'annonce ?"""
    t = normaliser(texte)
    jetons = t.split()
    return any(_marqueur_present(m, t, jetons) for m in MARQUEURS_FRANCAIS)


# =====================================================================
#  PARTIE 2 — À REMPLACER
# ---------------------------------------------------------------------
#  Où : dans main(), à l'intérieur de la boucle « for annonce in
#       annonces: ».
#
#  Repère la ligne qui commence par :
#       if str(deal.get("id", "")).startswith("vinted-"):
#  et remplace TOUT ce bloc (jusqu'à son `continue` final, juste avant
#  la ligne `log.info("  ✓ DEAL : ...")`) par le code ci-dessous.
#
#  ⚠️ ATTENTION À L'INDENTATION : ce code vit à l'intérieur de deux
#  boucles imbriquées. Les lignes commencent à 12 espaces, comme dans
#  l'original. Ne pas décaler.
# =====================================================================

            if str(deal.get("id", "")).startswith("vinted-"):
                desc = vinted_description(str(deal["id"]).replace("vinted-", "", 1))
                texte_annonce = f"{deal.get('titre', '')} {desc}".strip()
                if desc:
                    ok_lg, motif = annonce_pertinente(
                        texte_annonce, carte["nom"],
                        carte.get("langue", "fr"), carte.get("alias", ""))
                    # On ne rejette QUE sur un motif de LANGUE. Les autres
                    # exclusions (lot, bundle...) ne doivent pas s'appliquer
                    # à la description : un vendeur qui écrit « merci de
                    # privilégier l'achat par lot » vend bien une carte seule,
                    # et son annonce serait écartée à tort.
                    if not ok_lg and ("étrangère" in motif or "langue" in motif):
                        log.info("  ✗ Écarté après lecture de la description : %s (%s)",
                                 deal["titre"][:50], motif)
                        marquer(vues, deal["id"])
                        continue

                # V26 : preuve positive de français. Cartes FR uniquement —
                # les cartes JP/KR/CN gardent leur filtre habituel.
                if carte.get("langue", "fr") in (None, "", "fr"):
                    neutre = _nom_neutre_entre_langues(carte["nom"])
                    t_norm = normaliser(texte_annonce)
                    mots_fr = [m for m in mots_requis(carte["nom"]) if m != "mega"]
                    nom_fr = mots_fr[0] if mots_fr else ""

                    # (a) Le nom FRANÇAIS doit figurer en toutes lettres.
                    #     Un titre bilingue « Dracaufeu / Charizard » le
                    #     contient : il PASSE — c'est même une preuve de
                    #     français, un vendeur italien n'écrit jamais
                    #     « Dracaufeu ». Ce qu'on écarte ici, c'est
                    #     uniquement l'annonce qui n'a passé le filtre que
                    #     par son ALIAS anglais, sans jamais nommer la
                    #     carte en français.
                    if not neutre and nom_fr and nom_fr not in t_norm:
                        log.info("  ✗ Écarté : nom français '%s' absent de l'annonce "
                                 "(reconnue via l'alias seul) — %s",
                                 nom_fr, deal["titre"][:50])
                        marquer(vues, deal["id"])
                        continue

                    # (b) Nom neutre (Mew, Pikachu, Lucario...) : le nom ne
                    #     prouve rien, on exige un mot français — MAIS
                    #     seulement si on a pu LIRE la description. Une
                    #     description absente (429, session expirée, fiche
                    #     supprimée) est un incident réseau, pas une preuve
                    #     d'annonce étrangère : sans le `desc and`, on
                    #     écarterait de vraies annonces françaises pour une
                    #     panne, et en les marquant vues, définitivement.
                    if neutre and desc and not preuve_francais(texte_annonce):
                        log.info("  ✗ Écarté : nom de Pokémon identique dans toutes "
                                 "les langues et aucun mot français dans l'annonce "
                                 "— %s", deal["titre"][:50])
                        marquer(vues, deal["id"])
                        continue


# =====================================================================
#  PARTIE 3 — À AJOUTER (TEMPORAIRE : 1 SEUL SCAN, PUIS RETIRER)
# ---------------------------------------------------------------------
#  Où : dans la fonction `vinted_description`.
#
#  Cette fonction récupère déjà la fiche complète de l'annonce Vinted et
#  n'en extrait qu'un seul champ. Cette fiche contient peut-être le pays
#  ou la locale du vendeur. Si c'est le cas, on obtient sur Vinted le
#  même signal factuel que sur eBay — et toute la liste MARQUEURS_FRANCAIS
#  ci-dessus devient inutile, remplacée par un vrai filtre de pays.
#
#  Remplace :
#       item = (r.json() or {}).get("item") or {}
#       return str(item.get("description") or "")
#
#  par les 3 lignes ci-dessous, lance UN scan, puis envoie-moi la ligne
#  « [Vinted debug] champs disponibles : ... » du log.
# =====================================================================

        item = (r.json() or {}).get("item") or {}
        log.info("    [Vinted debug] champs disponibles : %s", sorted(item.keys()))
        return str(item.get("description") or "")


# =====================================================================
#  RÉSULTAT ATTENDU (annonces Vinted, cartes françaises)
# ---------------------------------------------------------------------
#   « Dracaufeu / Charizard ex 199/165 »          -> ALERTE (bilingue OK)
#   « Dracaufeu ex 199/165 NM »                   -> ALERTE
#   « Charizard ex 199/165 » seul (via alias)     -> silence
#   « Mew ex 205/165 » + description lue, 0 mot FR-> silence
#   « Mew ex 205/165 » + « état neuf, envoi »     -> ALERTE
#   « Mew ex 205/165 » + description illisible    -> ALERTE (pas de panne
#                                                    = pas de preuve)
#
#   Cartes JP / KR / CN : comportement totalement inchangé.
# =====================================================================
