"""
Moteur de cote de PokéDeals : calcule la "cote" (juste prix de référence)
d'une carte à partir des annonces eBay, la lisse dans le temps, puis
évalue chaque annonce individuelle contre cette cote pour décider si
c'est un deal.

Extrait de main.py le 17/08/2026 (septième module du découpage progressif,
cf. SESSION_NOTES.md) — extraction la plus étendue et la plus risquée du
découpage à ce jour : recolle QUATRE blocs non contigus de main.py
(contre deux pour connecteur_leboncoin.py), tous liés au calcul/à
l'évaluation de la cote mais historiquement dispersés entre d'autres
sections (fetch eBay, cotes Cardmarket/TCGdex, fetch Vinted, stats/CSV) :

1. Suivi de l'ancienneté des annonces (V44) : `anciennete()`,
   `jours_en_ligne()`... -- sert UNIQUEMENT à `calculer_cote()` (exclusion
   des annonces "stagnantes" du panier bas-marché), déplacé ici plutôt
   que laissé dans main.py pour rester à côté de son unique consommateur.
2. `_localisation_incoherente()` + `calculer_cote()` -- le calcul du
   prix de référence lui-même (médiane eBay nettoyée des valeurs
   aberrantes, ou moyenne du bas de marché selon `cfg.cote.methode`).
3. Persistance de l'historique des cotes (`historique()`,
   `sauvegarder_historique()`...) + `cle_cote()`/`cote_lissee()`/
   `enregistrer_cote()`/`obtenir_cote()` (choix de la cote à utiliser :
   manuelle > lissée > instantanée) + `_etat_ok()` + `evaluate()`
   (décision DEAL/pas-DEAL sur une annonce précise).
4. `calculer_tendance_cote()` -- petit utilitaire d'affichage (flèche
   hausse/baisse pour le CSV), qui lit le même historique.

Tout le reste (fetch eBay/Vinted/Leboncoin, notifications, stats,
détection d'anomalies, suivi de fiabilité...) reste dans main.py, qui
réimporte les noms publics de ce module comme pour les connecteurs
précédents. `detecter_anomalies()` et `verifier_cotes_manuelles_perimees()`
restent volontairement dans main.py bien qu'elles lisent `historique()` :
ce sont des générateurs d'ALERTES Telegram couplés à `anti_spam()`/`vues`
(état du système de dédup, pas du moteur de cote), même logique que
`verifier_fiabilite_plateformes()` restée dans main.py malgré l'extraction
de `_stats_fiabilite`.

Aucun état partagé mutable n'est réassigné en bloc ici (`_historique` et
`_anciennete` sont mutés via leurs accesseurs `historique()`/`anciennete()`,
jamais réassignés depuis l'extérieur de ce module) : main.py ne réimporte
que des FONCTIONS, jamais ces variables de cache directement, donc pas de
piège de liaison figée comme `_ct_cache` (connecteur_cardtrader.py).
"""
from __future__ import annotations

import json
import logging
import os
import statistics
import time

from filtre_annonces import annonce_pertinente, normaliser, SIGNAUX_ENCHERE
from json_utils import ecrire_json_atomique

log = logging.getLogger("pokedeals.moteur_cote")
RACINE = os.path.dirname(os.path.abspath(__file__))


# =====================================================================
# V44 : SUIVI DE L'ANCIENNETÉ DES ANNONCES (pour repérer les prix qui
# ne se vendent jamais).
# ---------------------------------------------------------------------
# seen.json ne suffit pas pour ça : il ne mémorise QUE les annonces qui
# ont failli devenir un deal. Or le problème vient justement des annonces
# qui composent le calcul de la cote SANS jamais devenir un deal — une
# annonce à 300€ qui traîne sans se vendre gonfle la cote, mais n'est
# jamais "vue" au sens actuel du programme.
# On crée donc un suivi séparé : première date à laquelle chaque
# annonce a été VUE dans le calcul de cote (pas seulement testée pour
# une alerte). Une annonce qui reste identique sur plusieurs jours
# n'est probablement jamais vendue à ce prix.
# =====================================================================
FICHIER_ANCIENNETE = os.path.join(RACINE, "data", "anciennete_annonces.json")
ANCIENNETE_RETENTION_JOURS = 45  # un peu plus que seen.json, pour garder assez d'historique

_anciennete: dict | None = None


def _charger_anciennete() -> dict:
    if not os.path.exists(FICHIER_ANCIENNETE):
        return {}
    try:
        with open(FICHIER_ANCIENNETE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def anciennete() -> dict:
    global _anciennete
    if _anciennete is None:
        _anciennete = _charger_anciennete()
    return _anciennete


def donnees_anciennete_a_sauvegarder() -> dict:
    """Dict pret a etre persiste (retention deja appliquee) -- utilise par
    sauvegarder_anciennete() (fichier local) et par main.py pour le chemin
    Supabase (migration du 25/08/2026, cf. memoire_supabase.py)."""
    donnees = anciennete()
    limite = time.time() - ANCIENNETE_RETENTION_JOURS * 86400
    return {k: v for k, v in donnees.items() if v.get("premiere_vue", 0) > limite}


def sauvegarder_anciennete() -> None:
    ecrire_json_atomique(FICHIER_ANCIENNETE, donnees_anciennete_a_sauvegarder(), ensure_ascii=False, indent=1)


def initialiser_anciennete(donnees: dict) -> None:
    """Amorce le cache module (anciennete) depuis des donnees deja chargees
    en amont (Supabase) -- alternative a _charger_anciennete() (fichier
    local), utilisee par main.py quand SUPABASE_URL/SERVICE_ROLE_KEY sont
    configures."""
    global _anciennete
    _anciennete = donnees if isinstance(donnees, dict) else {}


def jours_en_ligne(annonce_id: str) -> float:
    """Nombre de jours depuis la première fois que cette annonce a été vue
    dans un calcul de cote. Enregistre aussi la première apparition si
    c'est la première fois qu'on la voit. Retourne 0.0 pour une annonce
    toute nouvelle (aucun signal d'ancienneté, ni bon ni mauvais)."""
    donnees = anciennete()
    maintenant = time.time()
    entree = donnees.get(annonce_id)
    if entree is None:
        donnees[annonce_id] = {"premiere_vue": maintenant}
        return 0.0
    return (maintenant - entree["premiere_vue"]) / 86400


def _localisation_incoherente(annonce: dict, langue: str) -> bool:
    """V18 : True si l'annonce vient d'un pays incompatible avec la langue
    recherchée. Une carte FRANÇAISE ne se vend pas depuis le Japon : les
    annonces "eBay (JP)", "eBay (KR)", "eBay (CN)" doivent être écartées de
    la cote ET des deals d'une carte FR (sinon la cote est gonflée par des
    cartes japonaises au même numéro, cf. Pikachu 173/165 et Bulbizarre
    166/165 vendus en version JP à des prix bien plus élevés).
    """
    if langue not in (None, "", "fr"):
        return False  # pour une carte JP/KR/CN, l'origine étrangère est normale
    plateforme = str(annonce.get("plateforme", ""))
    # "eBay (JP)", "eBay (DE)"... : tout ce qui n'est pas FR est suspect pour
    # une carte française d'un set (151, Méga) qui existe aussi en asiatique.
    if plateforme.startswith("eBay (") and not plateforme.startswith("eBay (FR"):
        return True
    return False


def calculer_cote(annonces: list[dict], cfg_cote: dict, nom_carte: str = "",
                  langue: str = "fr", alias: str = "") -> tuple[float | None, int]:
    """Cote = médiane des prix des annonces PERTINENTES × coefficient.

    V15 : le filtre `annonce_pertinente` exige le numéro exact de la carte.
    V16 : il vérifie aussi la langue (texte). V18 : on écarte en plus les
    annonces localisées à l'étranger pour une carte FR (eBay JP/KR/CN), qui
    gonflaient la cote avec des versions asiatiques au même numéro.
    Retourne (cote, nb_annonces_utilisées).
    """
    if nom_carte:
        # V20 diagnostic : on garde (prix, titre, plateforme) des annonces
        # retenues pour pouvoir les afficher dans les logs et repérer ce qui
        # gonfle une cote. V44 : on garde aussi l'id, pour le suivi
        # d'ancienneté (annonces qui traînent sans se vendre).
        retenues = [(a["prix"], a.get("titre", "")[:70], a.get("plateforme", ""), a.get("id", ""))
                    for a in annonces
                    if a["prix"] > 0
                    and not _localisation_incoherente(a, langue)
                    and annonce_pertinente(a.get("titre", ""), nom_carte, langue, alias, a.get("plateforme", ""))[0]]
        retenues.sort()
        prix = [p for p, _, _, _ in retenues]
    else:
        retenues = []
        prix = sorted(a["prix"] for a in annonces if a["prix"] > 0)

    if len(prix) < int(cfg_cote.get("minimum_annonces", 8)):
        return None, len(prix)

    # Élimination des valeurs aberrantes (IQR) : vendeurs fantaisistes, erreurs de prix
    if len(prix) >= 4:
        q = statistics.quantiles(prix, n=4)
        iqr = q[2] - q[0]
        bas, haut = q[0] - 1.5 * iqr, q[2] + 1.5 * iqr
        nettoyes = [p for p in prix if bas <= p <= haut] or prix
    else:
        nettoyes = prix

    # V17 : cote = MÉDIANE des prix nettoyés (après filtrage IQR).
    reference = statistics.median(nettoyes)
    coef = float(cfg_cote.get("coefficient_marche", 1.0))
    cote = round(reference * coef, 2)

    # V23 : MÉTHODE ALTERNATIVE — moyenne des N annonces les moins chères.
    # Motif : les prix eBay sont des prix DEMANDÉS. La médiane capture le
    # milieu des espoirs de vendeurs, pas le prix auquel une carte part
    # réellement. Mesuré sur 3 cartes vérifiées à la main contre Cardmarket,
    # la médiane eBay dépasse la tendance Cardmarket d'un facteur 1,8 à 2,5.
    # La moyenne du bas de marché (même méthode que pour Cardtrader) s'en
    # approche nettement mieux — et se réajuste seule quand le marché bouge.
    nb_bas = int(cfg_cote.get("nb_prix_bas", 5))
    seuil_jours = float(cfg_cote.get("seuil_jours_stagnant", 10))
    if nom_carte and retenues:
        # V44 : une annonce en ligne depuis plus de `seuil_jours_stagnant`
        # jours ne se vend probablement pas à ce prix — elle gonfle le
        # panier bas-marché sans refléter un vrai prix de vente. On
        # l'écarte du panier tant que des annonces plus fraîches
        # suffisent ; sinon on la garde (mieux qu'aucune cote).
        candidats = sorted(nettoyes)
        fraiches = [p for p, _, _, aid in retenues
                   if p in candidats and jours_en_ligne(aid) < seuil_jours]
        fraiches.sort()
        bas_marche = fraiches[:max(1, nb_bas)] if len(fraiches) >= max(1, nb_bas) else candidats[:max(1, nb_bas)]
    else:
        bas_marche = sorted(nettoyes)[:max(1, nb_bas)]
    cote_basse = round((sum(bas_marche) / len(bas_marche)) * coef, 2)

    mode_cote = str(cfg_cote.get("methode", "mediane")).lower()
    if mode_cote == "bas_marche":
        cote_retenue = cote_basse
    else:
        cote_retenue = cote

    # V20 diagnostic : détail des annonces qui composent la cote (visible dans
    # les logs GitHub). Permet de repérer une annonce anormalement chère qui
    # gonfle la médiane. À retirer une fois le diagnostic terminé.
    if nom_carte and retenues:
        rejetes_iqr = [p for p in prix if p not in nettoyes]
        log.info("    [cote %s] médiane=%.2f€ | bas-marché(%d)=%.2f€ | ×%.2f -> RETENUE %.2f€"
                 " | %d annonces%s",
                 nom_carte, reference, len(bas_marche), cote_basse / coef if coef else cote_basse,
                 coef, cote_retenue, len(nettoyes),
                 f" ({len(rejetes_iqr)} écartées IQR : {rejetes_iqr})" if rejetes_iqr else "")
        for p, titre, plat, aid in retenues:
            marque = " ← ÉCARTÉE(IQR)" if p not in nettoyes else ""
            if p in bas_marche and not marque:
                marque = " ← bas-marché"
            elif not marque and p in candidats and jours_en_ligne(aid) >= seuil_jours:
                marque = f" ← stagnante ({jours_en_ligne(aid):.0f}j, exclue du panier)"
            log.info("        %.2f€  [%s] %s%s", p, plat, titre, marque)

    return cote_retenue, len(nettoyes)


FICHIER_COTES = os.path.join(RACINE, "data", "cotes.json")
HISTORIQUE_MAX = 5          # nombre de cotes conservées par carte
VALIDITE_JOURS = 7          # une cote de plus de 7 jours est ignorée
# V17.1 : purge par VERSION plutôt que par date.
# La purge par timestamp (DEPLOIEMENT_TS) laissait survivre les cotes
# recalculées le jour même du déploiement (Dracaufeu figé à 432,50€,
# Darkrai 099 à 11,16€...). On passe à un "tag" : si le tag stocké dans
# data/cotes.json ne correspond PAS à PURGE_VERSION ci-dessous, TOUT
# l'historique est jeté au prochain scan. Pour forcer une remise à zéro
# à l'avenir, il suffit d'incrémenter ce numéro.
PURGE_VERSION = 20  # V26 : les clés d'historique intègrent la langue (fuite KR<-JP)
# Conservé pour compatibilité de lecture des anciens fichiers (non utilisé
# pour la purge elle-même).
DEPLOIEMENT_TS = 1784160000  # 16/07/2026 00:00 UTC


def _charger_historique() -> dict:
    if not os.path.exists(FICHIER_COTES):
        return {}
    try:
        with open(FICHIER_COTES, "r", encoding="utf-8") as f:
            brut = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    # Purge par version : si le fichier n'a pas le bon tag, on repart de zéro.
    if not isinstance(brut, dict) or brut.get("_purge_version") != PURGE_VERSION:
        log.info("Historique des cotes réinitialisé (purge V%s) : repart propre", PURGE_VERSION)
        return {}
    # Format valide et à jour : on retire la clé technique et on renvoie les cotes.
    return {nom: entrees for nom, entrees in brut.items() if nom != "_purge_version"}


def donnees_historique_a_sauvegarder() -> dict:
    """Dict pret a etre persiste (tag de version inclus) -- utilise par
    sauvegarder_historique() (fichier local) et par main.py pour le chemin
    Supabase (migration du 25/08/2026, cf. memoire_supabase.py)."""
    a_ecrire = {"_purge_version": PURGE_VERSION}
    a_ecrire.update(historique())
    return a_ecrire


def sauvegarder_historique() -> None:
    ecrire_json_atomique(FICHIER_COTES, donnees_historique_a_sauvegarder(), ensure_ascii=False, indent=1)


_historique = None


def historique() -> dict:
    global _historique
    if _historique is None:
        _historique = _charger_historique()
    return _historique


def initialiser_historique(brut: dict) -> None:
    """Amorce le cache module (historique) depuis des donnees deja chargees
    en amont (Supabase) -- meme logique de purge par version que
    _charger_historique() (fichier local), utilisee par main.py quand
    SUPABASE_URL/SERVICE_ROLE_KEY sont configures."""
    global _historique
    if not isinstance(brut, dict) or brut.get("_purge_version") != PURGE_VERSION:
        log.info("Historique des cotes réinitialisé (purge V%s) : repart propre", PURGE_VERSION)
        _historique = {}
    else:
        _historique = {nom: entrees for nom, entrees in brut.items() if nom != "_purge_version"}


# =====================================================================
# V26 : CLÉS D'HISTORIQUE PAR LANGUE
# ---------------------------------------------------------------------
# LE NOM SEUL NE SUFFIT PAS. Une même carte figure dans la watchlist
# sous le MÊME nom dans plusieurs langues (« Charizard ex 201/165 sv2a »
# existe en JP et en KR). Avec le nom pour seule clé, la passe KR
# relisait la cote JAPONAISE enregistrée quelques secondes plus tôt et
# l'affichait comme sa propre cote — avec 0 annonce derrière. Une
# annonce coréenne était donc comparée à un prix japonais : fausse
# alerte garantie dès qu'un écart de marché existe entre les deux
# langues (et le coréen se vend moins cher que le japonais).
# =====================================================================

def cle_cote(nom_carte: str, langue: str = "fr") -> str:
    """Clé d'historique d'une cote : nom + langue."""
    return f"{nom_carte}|{str(langue or 'fr').lower()}"


def cote_lissee(nom_carte: str, langue: str = "fr") -> float | None:
    """Médiane des cotes des 7 derniers jours (l'historique est déjà purgé
    par version au chargement, donc plus besoin de borne de déploiement)."""
    entrees = historique().get(cle_cote(nom_carte, langue), [])
    limite = time.time() - VALIDITE_JOURS * 86400
    valeurs = [e["cote"] for e in entrees if e.get("ts", 0) >= limite]
    if not valeurs:
        return None
    return round(statistics.median(valeurs), 2)


def enregistrer_cote(nom_carte: str, cote: float, langue: str = "fr",
                     nb_annonces: int | None = None) -> None:
    """Ajoute une entree a l'historique de la carte.

    `nb_annonces` (ajoute le 03/09/2026, audit) est le nombre d'annonces
    eBay PERTINENTES derriere cette cote (2e valeur retournee par
    calculer_cote()) -- purement informatif, jamais relu par la logique de
    cote elle-meme (cote_lissee()/calculer_tendance_cote() ne lisent que
    "cote"/"ts", donc l'ajout de ce champ est sans risque pour elles).
    Optionnel : None quand l'appelant n'a pas de vrai decompte a ce moment
    (ex. re-enregistrement d'une cote CORRIGEE par Cardtrader/TCGdex dans
    main.py, qui ne recompte pas les annonces eBay -- cf. son appel).
    Consomme par scoring_rarete.py via derniere_nb_annonces()."""
    h = historique()
    cle = cle_cote(nom_carte, langue)
    entrees = h.get(cle, [])
    entrees.append({"cote": cote, "ts": time.time(), "nb_annonces": nb_annonces})
    h[cle] = entrees[-HISTORIQUE_MAX:]


def derniere_nb_annonces(nom_carte: str, langue: str = "fr") -> int | None:
    """Nombre d'annonces eBay derriere la cote la plus RECENTE (par ts) de
    l'historique d'une carte -- ajoute le 03/09/2026 (audit) en meme temps
    que la persistance de "nb_annonces" par enregistrer_cote(). None si
    aucune entree, ou si l'entree la plus recente n'a pas ce champ (cote
    manuelle jamais enregistree ici, ou entree ecrite avant ce changement,
    purgee de toute facon des le prochain PURGE_VERSION)."""
    entrees = historique().get(cle_cote(nom_carte, langue), [])
    if not entrees:
        return None
    plus_recente = max(entrees, key=lambda e: e.get("ts", 0))
    return plus_recente.get("nb_annonces")


def obtenir_cote(carte: dict, annonces_ebay: list[dict], cfg: dict) -> tuple[float | None, int]:
    """Retourne (cote, confiance) où confiance = nb d'annonces eBay utilisées."""
    # 1) Cote manuelle prioritaire
    cote_manuelle = carte.get("cote")
    if cote_manuelle:
        try:
            return float(cote_manuelle), 99
        except (ValueError, TypeError):
            log.warning("Cote manuelle invalide pour %s", carte.get("nom"))

    # 2) Cote du jour depuis eBay (annonces FILTRÉES), ajoutée à l'historique
    langue = carte.get("langue", "fr")
    cote_instant, nb_pertinentes = calculer_cote(
        annonces_ebay, cfg["cote"], carte["nom"],
        langue, carte.get("alias", ""))
    if cote_instant:
        enregistrer_cote(carte["nom"], cote_instant, langue, nb_pertinentes)

    # 3) Cote lissée (médiane des derniers passages, MÊME LANGUE uniquement)
    cote = cote_lissee(carte["nom"], langue)
    if cote is None:
        cote = cote_instant
    if cote is None:
        log.info("Cote introuvable pour '%s' (%d annonce(s) pertinente(s), minimum %s requis)",
                 carte.get("nom"), nb_pertinentes, cfg["cote"].get("minimum_annonces", 8))
        return None, 0
    # V26 : dire clairement quand la cote vient de la MÉMOIRE et non du scan
    # du jour. Une cote « confiance : 0 annonces » n'est plus un mystère.
    if cote_instant is None:
        log.info("    [cote %s (%s)] aucune annonce eBay ce scan -> cote MÉMORISÉE "
                 "de %.2f€ réutilisée (moins de %s jours)",
                 carte["nom"], str(langue).upper(), cote, VALIDITE_JOURS)
    return cote, nb_pertinentes


def _etat_ok(texte: str, acceptes: list[str], refuses: list[str]) -> bool:
    t = (texte or "").lower()
    # V36 : NÉGATIONS. "Non gradée" / "ungraded" / "pas gradée" sont des
    # informations RASSURANTES (le vendeur précise que ce n'est PAS gradé),
    # mais elles contiennent littéralement le mot "gradée" — donc rejetées
    # à tort par erreur depuis le début. Cas vécu : "Non gradée Carte
    # Pokémon FR DRACAUFEU EX..." à 310€ (79€ sous la cote) écartée pour
    # "état refusé (gradée)" alors que la carte n'est justement PAS gradée.
    # On neutralise ces négations avant de chercher les mots interdits.
    for negation in ("non gradée", "non gradee", "non-gradée", "non-gradee",
                     "pas gradée", "pas gradee", "ungraded", "not graded",
                     "no grading", "sans grading"):
        t = t.replace(negation, "")
    if any(mot in t for mot in refuses):
        return False
    # V39 : nettoyage de code. etats_acceptes ne fait volontairement
    # RIEN filtrer — l'intention (documentée depuis le début) est
    # "accepter tout sauf les états explicitement refusés", beaucoup de
    # vendeurs n'indiquant pas l'état dans le titre. L'ancien code avait
    # deux branches qui renvoyaient toutes les deux True, ce qui donnait
    # l'impression trompeuse qu'un vrai filtre existait. etats_acceptes
    # dans config.yaml reste donc décoratif : garder la liste n'a pas
    # d'effet, seule etats_refuses agit.
    return True


def evaluate(annonce: dict, cote: float | None, cfg: dict, confiance: int = 0, marge_achat: float | None = None) -> tuple[dict | None, str]:
    """Évalue une annonce. Retourne (deal, status)."""
    r = cfg["regles"]

    # V45 : SEUIL DE PRIX FIXE, indépendant de la cote. Certaines cartes ont
    # un prix d'achat cible fixé à la main (ex. "je veux Plumeline à 15€ ou
    # moins, peu importe la cote calculée"). Défini par carte dans
    # config.yaml via "prix_max_fixe". Compare le PRIX SEUL (hors port),
    # comme demandé — pas le total.
    prix_fixe = annonce.get("prix_max_fixe")
    if prix_fixe:
        pertinent, raison = annonce_pertinente(
            annonce.get("titre", ""), annonce.get("carte", ""),
            annonce.get("langue", "fr"), annonce.get("alias", ""), annonce.get("plateforme", ""))
        if not pertinent:
            return None, raison
        if _localisation_incoherente(annonce, annonce.get("langue", "fr")):
            return None, "annonce localisée à l'étranger"
        if not _etat_ok(annonce.get("etat_texte", ""), cfg["etats_acceptes"], cfg["etats_refuses"]):
            return None, "état refusé (abîmée / gradée / jouée)"
        prix = float(annonce.get("prix", 0))
        if prix <= 0 or prix > float(prix_fixe):
            return None, f"prix ({prix:.2f}€) au-dessus du seuil fixe ({float(prix_fixe):.2f}€)"
        deal = {
            **annonce,
            "cote": float(prix_fixe),
            "total": round(prix + float(annonce.get("port", 0)), 2),
            "decote_pct": 0.0,
            "prix_revente_conseille": 0.0,
            "profit_net_estime": 0.0,
            "confiance": 100,  # 100 = seuil fixe manuel
        }
        return deal, "DEAL (seuil fixe)"

    if cote is None or cote <= 0:
        return None, "cote indisponible"
    if cote < r.get("cote_min", 5.0):
        return None, f"cote trop faible ({cote:.2f}€ < {r.get('cote_min', 5.0):.2f}€)"

    # Filtre anti-faux-positifs : lots, produits scellés, proxys, mauvaise version...
    # V15 : exige aussi le numéro exact de la carte dans le titre.
    # V16 : exige la cohérence de langue et accepte l'alias du Pokémon.
    pertinent, raison = annonce_pertinente(
        annonce.get("titre", ""), annonce.get("carte", ""),
        annonce.get("langue", "fr"), annonce.get("alias", ""), annonce.get("plateforme", ""))
    if not pertinent:
        return None, raison

    # V18 : une carte FRANÇAISE ne s'achète pas depuis le Japon. On rejette
    # les annonces localisées à l'étranger (eBay JP/KR/CN) qui, au même
    # numéro, sont des versions asiatiques bien plus chères et faussaient
    # les deals (cf. Pikachu 173/165 japonais à 81€ vu comme un deal).
    if _localisation_incoherente(annonce, annonce.get("langue", "fr")):
        return None, "annonce localisée à l'étranger pour une carte FR"

    prix = float(annonce.get("prix", 0))
    port = float(annonce.get("port", 0))
    total = prix + port

    prix_max = float(r.get("prix_max", 0) or 0)
    if prix_max > 0 and total > prix_max:
        return None, f"au-dessus du budget ({total:.2f}€)"
    # V36 : le plafond de port n'a plus de sens en chiffre FIXE quand la
    # watchlist va des cartes à 15€ (port à 6€ = 40% du prix, déjà limite)
    # V40 : plafond basé sur la COTE, pas sur le prix de l'annonce. Le
    # prix payé varie (c'est justement ce qu'on négocie), mais le vrai
    # risque du port reste proportionnel à la VALEUR RÉELLE de la carte.
    # V41 : passage de 5% à 7%. À 5%, une carte à ~160€ de cote (comme
    # Florizarre) plafonnait le port à 8€, alors que les ports réels
    # tournaient autour de 10-11€ sur cette gamme de prix -> 30 annonces
    # rejetées sur un seul scan pour ce seul motif.
    base_port = cote if (cote and cote > 0) else prix
    port_max = max(float(r["frais_port_max"]), base_port * 0.07)
    if str(annonce.get("plateforme", "")).startswith("eBay ("):
        port_max = max(float(r.get("frais_port_max_international", 10.0)), base_port * 0.07)
    if port > port_max:
        return None, f"port trop cher ({port:.2f}€ > {port_max:.2f}€)"
    if not _etat_ok(annonce.get("etat_texte", ""), cfg["etats_acceptes"], cfg["etats_refuses"]):
        return None, "état refusé (abîmée / gradée / jouée)"

    # --- Achat : total net au moins 10% sous la cote ---
    # Marge par carte (override), sinon marge globale
    marge = marge_achat if marge_achat is not None else r["marge_achat"]
    seuil_achat = cote * (1 - marge)
    if total > seuil_achat:
        return None, f"pas assez sous la cote ({total:.2f}€ > seuil {seuil_achat:.2f}€)"

    # V22.8 : GARDE-FOU « TROP BEAU POUR ÊTRE VRAI ».
    # Une carte à 340€ affichée 1€ n'est pas une affaire : c'est un prix
    # d'appel pour créer des enchères en commentaire (pratique courante et
    # interdite sur Vinted), un article factice, ou une erreur. Cas vécu :
    # Méga-Lucario Gold 188/132 à 1€ + port, description « Non comprare a
    # 1 € » (= « n'achetez pas à 1 € »). En dessous d'un certain pourcentage
    # de la cote, une annonce est suspecte, pas exceptionnelle.
    seuil_absurde = float(r.get("prix_plancher_ratio", 0.15))
    if cote > 0 and total < cote * seuil_absurde:
        return None, (f"prix d'appel suspect ({total:.2f}€ = {total / cote * 100:.0f}% "
                      f"de la cote {cote:.2f}€, seuil {seuil_absurde * 100:.0f}%)")
    # Signal explicite d'enchère déguisée dans le texte de l'annonce.
    texte_annonce = normaliser(str(annonce.get("titre", "")))
    if any(sig in texte_annonce for sig in SIGNAUX_ENCHERE):
        return None, "annonce d'enchère déguisée (prix d'appel)"

    # --- Revente : au moins 10% net au-dessus de la cote, frais déduits ---
    # Garde-fou : si frais_revente_estimes >= 1 (100%), le dénominateur
    # serait nul ou négatif -> on borne à 0.99 max pour éviter le crash.
    frais_revente = min(float(r["frais_revente_estimes"]), 0.99)
    prix_revente = cote * (1 + r["marge_revente"]) / (1 - frais_revente)
    profit_net = cote * (1 + r["marge_revente"]) - total
    profit_min = float(r.get("profit_min", 0) or 0)
    if profit_net < max(profit_min, 0.01):
        return None, f"profit trop faible ({profit_net:.2f}€ < {profit_min:.2f}€ minimum)"

    deal = {
        **annonce,
        "cote": round(cote, 2),
        "total": round(total, 2),
        "decote_pct": round((1 - total / cote) * 100, 1),
        "prix_revente_conseille": round(prix_revente, 2),
        "profit_net_estime": round(profit_net, 2),
        # nb d'annonces eBay derrière la cote.
        # Valeurs spéciales : 99 = cote manuelle (config.yaml),
        #                     98 = cote fournie par Cardtrader (V27).
        "confiance": confiance,
    }
    return deal, "DEAL"


def calculer_tendance_cote(nom_carte: str, langue: str = "fr") -> str:
    """Compare la cote actuelle avec celle d'hier pour déterminer la tendance."""
    h = historique()
    cle = cle_cote(nom_carte, langue)
    if cle not in h or len(h[cle]) < 2:
        return "="  # pas assez de données

    cotes = [e["cote"] for e in h[cle]]
    if len(cotes) < 2:
        return "="

    cote_aujourd = cotes[-1]
    cote_hier = cotes[0] if len(cotes) >= 2 else cote_aujourd

    if cote_aujourd > cote_hier * 1.05:  # +5% = hausse
        return "↗️"
    elif cote_aujourd < cote_hier * 0.95:  # -5% = baisse
        return "↘️"
    else:
        return "="
