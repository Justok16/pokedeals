"""Sentinelle DIG16 (13/10/2026) : surveillance indépendante de la conversation Claude, lancée toutes les 3 heures
par GitHub Actions (.github/workflows/sentinelle_dig16.yml). Sans aucun secret.
Vérifie : pages principales du site (code 200 et nom DIG16), certificat HTTPS (plus de 20 jours), nom de domaine
(expiration lue sur rdap.nic.fr, plus de 45 jours), messagerie (MX de dig16.fr présent), fichiers publics utiles
(robots.txt, sitemap.xml, llms.txt). Écrit le rapport dans sentinelle.md et sort avec le nombre d'alertes."""

import datetime
import socket
import ssl
import sys

import requests

DOMAINE = "dig16.fr"
PAGES = ["/", "/prestige", "/mentions-legales", "/robots.txt", "/sitemap.xml", "/llms.txt"]
UA = {"User-Agent": "sentinelle-dig16 (surveillance du site, GitHub Actions)"}
res = []


def note(nom, bon, detail):
    res.append((nom, bool(bon), detail))


def pages():
    for p in PAGES:
        url = f"https://{DOMAINE}{p}"
        try:
            r = requests.get(url, headers=UA, timeout=30)
            bon = r.status_code == 200 and (p != "/" or "DIG16" in r.text)
            note(f"page {p}", bon, f"code {r.status_code}")
        except requests.RequestException as e:
            note(f"page {p}", False, str(e)[:120])


def certificat():
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((DOMAINE, 443), timeout=20) as s:
            with ctx.wrap_socket(s, server_hostname=DOMAINE) as t:
                fin = datetime.datetime.fromtimestamp(
                    ssl.cert_time_to_seconds(t.getpeercert()["notAfter"]), datetime.timezone.utc
                )
        jours = (fin - datetime.datetime.now(datetime.timezone.utc)).days
        note("certificat HTTPS", jours > 20, f"expire dans {jours} jours ({fin:%d/%m/%Y})")
    except (OSError, ssl.SSLError, KeyError) as e:
        note("certificat HTTPS", False, str(e)[:120])


def domaine():
    try:
        d = requests.get(f"https://rdap.nic.fr/domain/{DOMAINE}", headers=UA, timeout=30).json()
        fin = next(e["eventDate"] for e in d.get("events", []) if e.get("eventAction") == "expiration")
        fin = datetime.datetime.fromisoformat(fin.replace("Z", "+00:00"))
        jours = (fin - datetime.datetime.now(datetime.timezone.utc)).days
        note("nom de domaine", jours > 45, f"expire dans {jours} jours ({fin:%d/%m/%Y}), à renouveler chez OVH")
    except (requests.RequestException, ValueError, StopIteration) as e:
        note("nom de domaine", False, f"expiration illisible : {str(e)[:100]}")


def messagerie():
    try:
        d = requests.get(
            "https://dns.google/resolve", params={"name": DOMAINE, "type": "MX"}, headers=UA, timeout=20
        ).json()
        mx = [a["data"] for a in d.get("Answer", []) if a.get("type") == 15]
        note("messagerie (MX)", bool(mx), ", ".join(mx) or "aucun enregistrement MX")
    except (requests.RequestException, ValueError) as e:
        note("messagerie (MX)", False, str(e)[:120])


pages()
certificat()
domaine()
messagerie()

alertes = [r for r in res if not r[1]]
lignes = [f"Sentinelle DIG16 du {datetime.datetime.now(datetime.timezone.utc):%d/%m/%Y %H:%M} UTC", ""]
lignes += [f"- {'OK' if b else '**ALERTE**'} {n} : {d}" for n, b, d in res]
with open("sentinelle.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lignes) + "\n")
print("\n".join(lignes))
sys.exit(len(alertes))
