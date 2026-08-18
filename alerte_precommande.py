"""
Detection d'OUVERTURE de precommande pour des produits scelles surveilles
(cf. precommandes_watchlist.py) -- systeme d'alerte INDEPENDANT de
bonne_affaire_shopify.py (seuil de prix sur cartes deja catalogues) et
alerte_stock.py (retour en stock d'un produit deja catalogue).

Contrairement a alerte_stock.py qui compare un etat "en_stock" avant/apres
pour un produit deja connu, ici on detecte l'APPARITION du produit
LUI-MEME sur une boutique (precommande qui n'existait pas avant -> existe
maintenant), en stock ou non -- la simple presence d'une page produit
correspondante suffit a declencher l'alerte (une seule fois par produit x
boutique, memorisee pour ne jamais re-alerter deux fois).
"""

from pathlib import Path

import requests

from memoire_json import charger_memoire as _charger_memoire_generique, sauvegarder_memoire as _sauvegarder_memoire_generique
from telegram_utils import echapper_html as _echapper_html, echapper_url_html as _echapper_url_html

def _cle_memoire(domaine: str, nom_produit: str) -> str:
    return f"{domaine}|{nom_produit}"


# Pas de valeur par defaut pour `chemin` : un fichier memoire PAR PLATEFORME
# existe (precommandes_anniversaire_{shopify,prestashop,woocommerce}.json),
# scan_precommandes.py passe toujours le chemin explicite -- un defaut
# generique pointerait vers un fichier qui n'existe jamais reellement
# (piege trouve a l'audit du 16/08/2026, defaut jamais utilise en pratique).
def charger_memoire(chemin: Path) -> dict:
    return _charger_memoire_generique(chemin)


def sauvegarder_memoire(memoire: dict, chemin: Path) -> None:
    _sauvegarder_memoire_generique(memoire, chemin)


def detecter_nouvelles_precommandes(
    domaine: str,
    candidats: list[dict],
    memoire: dict,
) -> list[dict]:
    """`candidats` : liste de dicts {nom_produit, confiance, raison, titre,
    url_produit, prix, en_stock} deja filtres/evalues par
    precommandes_watchlist.evaluer_correspondance (confiance != None).

    N'ALERTE JAMAIS sur la toute premiere detection d'un (domaine,
    nom_produit) A CONFIANCE "MOYENNE" -- MEME PRINCIPE que alerte_stock.py
    ("Une carte x boutique jamais vue avant est ajoutee a la memoire mais
    NE DECLENCHE PAS d'alerte, evite le spam massif au premier lancement").
    Bug reel corrige le 11/08/2026 : la version precedente alertait des la
    premiere detection, ce qui a produit une avalanche d'alertes des
    l'activation du radar pour des pages qui EXISTAIENT DEJA avant
    (annonces precoces de revendeurs, notamment japonais, souvent hors
    stock ou pas encore ouvertes a la commande) -- pas de vraie
    "apparition", juste l'effet de bord d'une memoire vide au premier
    cycle. Desormais, seules les apparitions constatees APRES un premier
    cycle de reference (qui etablit la base sans alerter) declenchent une
    alerte -- au prix d'un risque residuel documente : une precommande qui
    ouvre entre le tout premier cycle de reference et le second n'est
    detectee qu'au 2e cycle (30 min de retard max, pas un vrai raté).

    EXCEPTION ajoutee le 18/08/2026 (signale par Justok : deux boutiques,
    playshop.fr et gamesavenue.fr, avaient la precommande du Coffret 30e
    Anniversaire disponible avec DATE DE SORTIE DEJA CONFIRMEE des leur
    toute premiere verification -- jamais alertees, malgre une info
    parfaitement fiable et actionnable). Le risque de faux positif qui a
    motive la regle du 11/08 concernait des matches "moyenne" (mots-cles
    seuls, sans date -- une vieille annonce sans rapport peut matcher par
    coincidence). Un match "forte" des la premiere detection est un
    signal d'une nature differente : la date de sortie EXACTE attendue est
    deja confirmee sur la page, un faux positif par coincidence est
    quasiment exclu. Donc : premiere detection a confiance "moyenne" ->
    toujours silencieuse (memoire etablie, meme comportement qu'avant) ;
    premiere detection DIRECTEMENT a confiance "forte" -> alerte
    immediate, ne pas attendre un 2e cycle pour une info deja fiable.

    Alerte ENSUITE une seule fois par (domaine, nom_produit) -- si un
    match a confiance "moyenne" est deja memorise et qu'un match "forte"
    est trouve ensuite (date confirmee apres coup), une SECONDE alerte est
    envoyee pour signaler la confirmation -- utile (l'info "date
    confirmee" a une vraie valeur), pas juste du bruit.

    EXCEPTION ajoutee le 18/08/2026 (Justok : "les dates de precommande ne
    sont pas egales aux dates de sortie -- je veux pouvoir precommander
    des que possible pour etre SUR de pouvoir acheter"). Avant ce
    correctif, `en_stock` n'etait JAMAIS memorise -- seule `confiance`
    determinait si on re-alertait. Consequence concrete : une page qui
    apparait tot (date de sortie deja confirmee, donc alerte immediate
    grace au fix precedent) mais encore HORS STOCK (annonce/placeholder
    avant ouverture reelle des precommandes) declenchait bien une alerte
    UNE FOIS -- puis plus JAMAIS de second signal quand elle devient
    reellement commandable, puisque la confiance ne change pas entre les
    deux etats. Exactement le scenario que Justok voulait couvrir : le
    moment qui compte pour lui n'est pas l'apparition de la page, c'est le
    moment ou il peut reellement passer commande. Corrige en memorisant
    aussi `en_stock` et en declenchant une alerte des que ce champ passe a
    True alors qu'il ne l'etait pas avant (False/indetermine -> True),
    INDEPENDAMMENT du niveau de confiance -- cette transition prime sur
    toutes les autres regles de suppression ci-dessus, y compris
    `deja_confirme_mieux`. Une premiere detection (jamais vue avant)
    reste soumise aux regles habituelles ci-dessus (silencieuse si
    "moyenne", alerte immediate si "forte") : cette exception ne
    s'applique qu'a un produit DEJA connu dont le stock vient de changer.

    ECRITURE MEMOIRE DIFFEREE (V57, 18/08/2026, audit externe -- verifie
    contre le code reel avant correction) : pour un candidat qui declenche
    une alerte, `memoire[cle_mem]` n'est PLUS ecrit ici -- l'etat a
    memoriser est attache a l'evenement retourne (cles internes
    `_cle_memoire`/`_nouvel_etat`) et n'est commite qu'apres confirmation
    d'envoi Telegram reussi, par `envoyer_telegram_precommandes()`. Avant
    ce correctif, la memoire etait ecrite ICI puis sauvegardee sur disque
    AVANT meme la tentative d'envoi Telegram (cf. scan_precommandes.py) :
    un echec Telegram (timeout, 500, token invalide...) survenant APRES
    cette ecriture laissait la memoire dans l'etat "deja alerte" alors
    qu'aucune alerte n'etait jamais partie -- perte DEFINITIVE de
    l'evenement, plus aucune chance de le detecter a nouveau puisque l'etat
    memorise ne changerait plus au cycle suivant. Pour un candidat qui NE
    declenche PAS d'alerte (rien n'est du a l'utilisateur), l'ecriture
    reste immediate : aucune perte possible dans ce cas."""
    evenements = []

    for c in candidats:
        cle_mem = _cle_memoire(domaine, c["nom_produit"])
        etat_precedent = memoire.get(cle_mem)
        premiere_fois = etat_precedent is None
        # Cf. docstring V53 : seule la premiere detection a confiance
        # "moyenne" reste silencieuse -- une premiere detection deja
        # "forte" (date confirmee) est un signal trop fiable pour attendre
        # un 2e cycle.
        premiere_fois_ambigue = premiere_fois and c["confiance"] != "forte"

        deja_alerte_a_ce_niveau = (
            etat_precedent is not None
            and etat_precedent.get("confiance") == c["confiance"]
        )
        # Ne re-alerte pas si deja vu a confiance EGALE OU SUPERIEURE
        # (une fois "forte" alertee, un nouveau match "moyenne" sur la
        # meme page ne doit pas redeclencher).
        deja_confirme_mieux = (
            etat_precedent is not None
            and etat_precedent.get("confiance") == "forte"
        )
        # Cf. docstring V54 : un produit deja connu qui devient commandable
        # (stock False/indetermine -> True) alerte TOUJOURS, meme si la
        # confiance n'a pas change et meme si "forte" a deja ete confirmee.
        stock_vient_de_souvrir = (
            etat_precedent is not None
            and etat_precedent.get("en_stock") is not True
            and c.get("en_stock") is True
        )

        # Confiance MONOTONE (audit du 18/08/2026) : une fois "forte"
        # confirmee, ne redescend plus jamais a "moyenne" en memoire, meme
        # si un cycle ulterieur ne retrouve plus la date sur la page (ex.
        # boutique qui retire la mention de date apres l'annonce initiale,
        # ou texte de page legerement modifie). Sans ce plancher, un cycle
        # "forte" -> "moyenne" (silencieux, cf. deja_confirme_mieux) ecrase
        # la memoire avec "moyenne" ; un cycle SUIVANT qui retrouve "forte"
        # ne verrait alors plus deja_confirme_mieux=True et redeclencherait
        # a tort une 2e alerte de "confirmation" pour une date deja
        # confirmee une premiere fois.
        confiance_memorisee = c["confiance"]
        if etat_precedent is not None and etat_precedent.get("confiance") == "forte":
            confiance_memorisee = "forte"

        nouvel_etat = {
            "confiance": confiance_memorisee,
            "raison": c["raison"],
            "titre_produit": c["titre"],
            "url_produit": c["url_produit"],
            "derniere_verification": c.get("horodatage", ""),
            "en_stock": c.get("en_stock"),
        }

        if stock_vient_de_souvrir or (
            not premiere_fois_ambigue and not deja_alerte_a_ce_niveau and not deja_confirme_mieux
        ):
            c["_cle_memoire"] = cle_mem
            c["_nouvel_etat"] = nouvel_etat
            evenements.append(c)
        else:
            memoire[cle_mem] = nouvel_etat

    return evenements


# --- Notification Telegram (visuellement distincte des 2 autres alertes) ---
# _echapper_html/_echapper_url_html : cf. telegram_utils.py (import en tete
# de fichier).


def _texte_precommande(e: dict) -> str:
    niveau = "🟢 confirmée (date de sortie détectée)" if e["confiance"] == "forte" else "🟡 probable (mots-clés seuls)"
    # Statut de stock explicite -- evite la confusion constatee en prod
    # (alerte "précommande détectée" comprise a tort comme "achetable
    # maintenant" alors que la page peut tres bien exister hors stock ou
    # pas encore ouverte a la commande, cf. bug corrige le 11/08/2026 sur
    # le declenchement premature de l'alerte elle-meme -- ce champ ne
    # remplace pas ce fix, il rend juste chaque alerte auto-suffisante).
    if e.get("en_stock") is True:
        stock_ligne = "📦 En stock / commandable\n"
    elif e.get("en_stock") is False:
        stock_ligne = "⛔ Page trouvée mais actuellement HORS STOCK (pas encore commandable)\n"
    else:
        stock_ligne = "❓ Statut de stock indéterminé\n"
    prix_ligne = f"💰 {e['prix']:.2f}€\n" if e.get("prix") else ""
    lien_ligne = f"👉 <a href=\"{_echapper_url_html(e['url_produit'])}\">Voir le produit</a>" if e.get("url_produit") else ""
    # Marqueur purement cosmetique (V56, 18/08/2026, demande explicite de
    # Justok pour l'UPC Noctali) -- n'affecte aucune logique de detection.
    titre_ligne = f"🎁 <b>{_echapper_html(e['nom_produit'])}</b>"
    if e.get("prioritaire"):
        titre_ligne = f"⭐ {titre_ligne}"
    return (
        f"🎉 <b>Précommande détectée !</b>\n"
        f"{titre_ligne}\n"
        f"🏪 {_echapper_html(e['domaine'])}\n"
        f"🔎 Confiance : {niveau}\n"
        f"{stock_ligne}"
        f"{prix_ligne}"
        f"📝 {_echapper_html(e['titre'])}\n"
        f"{lien_ligne}"
    )


def envoyer_telegram_precommandes(evenements: list[dict], chat_id: str, token: str, memoire: dict | None = None) -> bool:
    """`memoire`, si fourni (V57, 18/08/2026) : l'etat differe de
    `detecter_nouvelles_precommandes()` (`e["_cle_memoire"]`/`e["_nouvel_etat"]`)
    n'est commite dans `memoire` QU'APRES confirmation d'envoi reussi pour
    CET evenement precis -- un echec (Telegram indisponible, token
    invalide...) laisse `memoire` intacte pour cet evenement, afin qu'il
    soit redetecte et re-tente au prochain cycle plutot que perdu
    definitivement (cf. docstring de detecter_nouvelles_precommandes)."""
    if not evenements:
        return True
    if not token or not chat_id:
        print("[alerte_precommande] Telegram non configure : alertes precommande non envoyees.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for e in evenements:
        succes = False
        try:
            r = requests.post(
                url,
                json={"chat_id": chat_id, "text": _texte_precommande(e), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code == 200:
                succes = True
            else:
                print(f"[alerte_precommande] Telegram a refuse l'alerte ({r.status_code}) : {r.text[:200]}")
        except Exception as ex:  # noqa: BLE001
            print(f"[alerte_precommande] Echec envoi Telegram : {ex}")

        if succes:
            if memoire is not None and "_cle_memoire" in e:
                memoire[e["_cle_memoire"]] = e["_nouvel_etat"]
        else:
            ok = False
    return ok
