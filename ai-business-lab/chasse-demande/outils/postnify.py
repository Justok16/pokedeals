#!/usr/bin/env python3
"""Postnify (offre « Free Forever » : 2 réseaux, 15 publications par mois, API incluse).

Préparé le 21/10/2026 pour publier sur X et Facebook en plus de Metricool et Buffer.
Documentation officielle lue le 21/10/2026 : https://docs.postnify.com/public-api/introduction,
  …/integrations/list, …/posts/create, …/providers/facebook, …/providers/x, …/uploads/upload-from-url
  - clé : Settings > Developers > Public API, envoyée dans l'en-tête « Authorization » ;
  - 30 appels par heure, tous points confondus : regrouper plusieurs publications dans un seul appel ;
  - l'interface dit « channel », l'API dit « integration » (même chose : un compte relié).

La clé n'est JAMAIS écrite dans le dépôt ni collée dans la conversation : elle est lue dans la
variable d'environnement POSTNIFY_API_KEY (réglages de l'environnement cloud).

Usage :
  python3 outils/postnify.py canaux                      liste les comptes reliés (id, réseau, nom)
  python3 outils/postnify.py programmer fichier.json     programme les publications décrites dans le fichier
  python3 outils/postnify.py exemple                     écrit un fichier d'exemple à compléter

Format du fichier JSON (une liste) :
  [{"reseau": "x", "date": "2026-11-03T17:30:00+01:00", "texte": "…", "images": ["https://…/1.jpg"]},
   {"reseau": "facebook", "date": "2026-11-03T17:30:00+01:00", "texte": "…", "images": [], "url": "https://dig16.fr"}]
Le compteur mensuel est tenu dans .claude/hooks/quotas.json (clé « postnify ») : jamais plus de 15 par mois.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://platform.postnify.com/api/public/v1"  # docs.postnify.com/public-api/introduction, lu le 21/10/2026
QUOTAS = Path(__file__).resolve().parents[3] / ".claude" / "hooks" / "quotas.json"
LIMITE_MOIS = 15
REGLAGES = {
    "x": {"__type": "x", "who_can_reply_post": "everyone", "community": "",
          "made_with_ai": False, "paid_partnership": False},
    "facebook": {"__type": "facebook"},
    "instagram": {"__type": "instagram", "post_type": "post", "collaborators": []},
    "threads": {"__type": "threads"},
}


def cle():
    k = os.environ.get("POSTNIFY_API_KEY", "").strip()
    if not k:
        sys.exit("POSTNIFY_API_KEY absente : à ajouter dans les réglages de l'environnement (jamais dans la conversation).")
    return k


def appel(methode, chemin, corps=None):
    req = urllib.request.Request(BASE + chemin, method=methode,
                                 headers={"Authorization": cle(), "Content-Type": "application/json",
                                          "User-Agent": "DIG16-postnify/1.0 (+https://dig16.fr)"})
    data = json.dumps(corps).encode() if corps is not None else None
    try:
        with urllib.request.urlopen(req, data, timeout=30) as r:
            return json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        sys.exit(f"Postnify {e.code} sur {chemin} : {e.read().decode()[:500]}")


def canaux():
    liste = appel("GET", "/integrations")
    for c in liste if isinstance(liste, list) else liste.get("integrations", []):
        print(f"{c.get('id')}  {c.get('identifier')}  {c.get('name')}"
              f"{'  (déconnecté)' if c.get('disabled') else ''}")
    return liste


def compteur(mois, ajout=0):
    q = json.loads(QUOTAS.read_text()) if QUOTAS.exists() else {}
    p = q.setdefault("postnify", {"limite": LIMITE_MOIS,
                                  "source": "postnify.com/pricing, lu le 21/10/2026 : Free Forever, 2 réseaux, 15 publications par mois, API incluse ; docs.postnify.com : 30 appels par heure",
                                  "mois": {}})
    deja = p["mois"].get(mois, 0)
    if ajout:
        p["mois"][mois] = deja + ajout
        QUOTAS.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n")
    return deja


def programmer(fichier):
    pubs = json.loads(Path(fichier).read_text(encoding="utf-8"))
    if not pubs:
        sys.exit("fichier vide")
    mois = pubs[0]["date"][:7]
    deja = compteur(mois)
    if deja + len(pubs) > LIMITE_MOIS:
        sys.exit(f"Quota Postnify : {deja} déjà programmées en {mois}, +{len(pubs)} dépasserait {LIMITE_MOIS}. Rien envoyé.")
    comptes = canaux()
    comptes = comptes if isinstance(comptes, list) else comptes.get("integrations", [])
    par_reseau = {c.get("identifier"): c["id"] for c in comptes}
    posts = []
    for p in pubs:
        if p["reseau"] not in par_reseau:
            sys.exit(f"réseau {p['reseau']} non relié dans Postnify (reliés : {', '.join(par_reseau)})")
        if p["reseau"] == "x" and len(p["texte"]) > 280:
            sys.exit(f"texte X de {len(p['texte'])} caractères (280 max) : {p['texte'][:60]}…")
        reglages = dict(REGLAGES[p["reseau"]])
        if p["reseau"] == "facebook" and p.get("url"):
            reglages["url"] = p["url"]
        # chaque image est d'abord importée chez Postnify (doc « Upload from URL ») : réponse {id, name, path}
        images = []
        for u in p.get("images", []):
            r = appel("POST", "/upload-from-url", {"url": u})
            images.append({"id": r["id"], "path": r["path"]})
        posts.append({"integration": {"id": par_reseau[p["reseau"]]},
                      "value": [{"content": p["texte"], "image": images}],
                      "settings": reglages})
    # un seul appel pour toutes les publications d'une même date ; dates différentes = appels séparés
    envoyes = 0
    for date in sorted({p["date"] for p in pubs}):
        lot = [posts[i] for i, p in enumerate(pubs) if p["date"] == date]
        d = datetime.fromisoformat(date).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        rep = appel("POST", "/posts", {"type": "schedule", "date": d, "shortLink": False, "tags": [], "posts": lot})
        print(date, "→", json.dumps(rep, ensure_ascii=False)[:300])
        envoyes += len(lot)
    compteur(mois, envoyes)
    print(f"{envoyes} publication(s) programmée(s) ; total {mois} : {compteur(mois)}/{LIMITE_MOIS}")


def exemple():
    ex = [{"reseau": "x", "date": "2026-11-03T17:30:00+01:00",
           "texte": "Un site qui se lit bien sur téléphone, au nom de l'artisan. Démo gratuite : https://dig16.fr/x #Charente #artisan",
           "images": ["https://dig16.fr/img/reseaux/pub/EXEMPLE-1.jpg"]},
          {"reseau": "facebook", "date": "2026-11-03T17:30:00+01:00", "texte": "…", "images": [], "url": "https://dig16.fr"}]
    Path("postnify-exemple.json").write_text(json.dumps(ex, ensure_ascii=False, indent=2), encoding="utf-8")
    print("postnify-exemple.json écrit")


if __name__ == "__main__":
    a = sys.argv[1:] or ["aide"]
    {"canaux": canaux, "exemple": exemple}.get(a[0], lambda: programmer(a[1]) if a[0] == "programmer" and len(a) > 1 else print(__doc__))()
