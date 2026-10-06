"""Contrôle de santé du projet en une commande (06/10/2026) : python3 outils/controle_global.py [--json]
Vérifie en moins d'une minute, sans aucun secret : site dig16.fr (pages, en-têtes, adresse officielle), DNSSEC et
messagerie du domaine (DNS en HTTPS), certificat, relais Vercel (cookie), file des résumés. Sortie : une ligne par
contrôle, « OK » ou « ALERTE », et le code de sortie vaut le nombre d'alertes (0 = tout va bien).
Le point automatique de 07:34 et 19:34 UTC le lance et ne signale à l'utilisateur QUE les alertes."""

import json
import os
import ssl
import socket
import subprocess
import sys
import datetime
import requests

SITE = "https://dig16.fr"
PAGES = {
    "/": "https://dig16.fr/",
    "/prestige": "https://dig16.fr/prestige",
    "/mentions-legales": "https://dig16.fr/mentions-legales",
}
ENTETES = [
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
]
res = []


def ok(nom, bon, detail="", info=False):
    res.append((nom, True if info else bool(bon), detail))


def doh(nom, type_):
    try:
        return requests.get(
            "https://dns.google/resolve",
            params={"name": nom, "type": type_},
            timeout=20,
        ).json()
    except Exception as e:
        return {"erreur": str(e)}


for chemin, canon in PAGES.items():
    try:
        r = requests.get(SITE + chemin, timeout=25)
        ok(
            f"page {chemin}",
            r.status_code == 200 and f'rel="canonical" href="{canon}"' in r.text,
            f"HTTP {r.status_code}",
        )
        if chemin == "/":
            manque = [h for h in ENTETES if h not in {k.lower() for k in r.headers}]
            ok("en-têtes de sécurité", not manque, ", ".join(manque) or "5/5")
            ok(
                "bandeau « ouverture prochaine »",
                "avis-ouverture" in r.text,
                "à retirer le jour du SIREN seulement",
            )
    except Exception as e:
        ok(f"page {chemin}", False, str(e)[:80])
try:
    ok(
        "www.dig16.fr",
        requests.get("https://www.dig16.fr", timeout=25).status_code == 200,
    )
except Exception as e:
    ok("www.dig16.fr", False, str(e)[:80])
ds = doh("dig16.fr", "DS")
a = doh("dig16.fr", "A")
ok(
    "DNSSEC (enregistrement DS)",
    bool(ds.get("Answer")),
    "présent" if ds.get("Answer") else "absent",
)
ok("DNSSEC validé (AD)", a.get("AD") is True, f"AD={a.get('AD')}")
mx = doh("dig16.fr", "MX")
ok(
    "messagerie (3 serveurs MX)",
    len(mx.get("Answer", [])) == 3,
    f"{len(mx.get('Answer', []))} serveurs",
)
txt = doh("dig16.fr", "TXT")
ok("SPF présent", any("v=spf1" in x.get("data", "") for x in txt.get("Answer", [])))
dm = doh("_dmarc.dig16.fr", "TXT")
ok("DMARC présent", any("v=DMARC1" in x.get("data", "") for x in dm.get("Answer", [])))
try:
    with (
        socket.create_connection(("dig16.fr", 443), timeout=15) as s,
        ssl.create_default_context().wrap_socket(s, server_hostname="dig16.fr") as t,
    ):
        fin = datetime.datetime.strptime(
            t.getpeercert()["notAfter"], "%b %d %H:%M:%S %Y %Z"
        )
        jours = (fin - datetime.datetime.utcnow()).days
        ok("certificat HTTPS", jours > 14, f"expire dans {jours} jours")
except Exception as e:
    ok("certificat HTTPS", False, str(e)[:80])
try:
    cj = "/tmp/cj.txt"
    age = (
        (datetime.datetime.now().timestamp() - os.path.getmtime(cj)) / 3600
        if os.path.exists(cj)
        else 999
    )
    code = subprocess.run(
        [
            "curl",
            "-s",
            "-o",
            "/dev/null",
            "-m",
            "30",
            "-w",
            "%{http_code}",
            "-b",
            cj,
            "https://relais-dig-justok1.vercel.app/api/video?liste=1",
        ],
        capture_output=True,
        text=True,
    ).stdout
    ok(
        "relais Vercel (cookie)",
        code == "200" and age < 23,
        f"HTTP {code}, cookie vieux de {age:.0f} h (à renouveler au-delà de 22 h)",
    )
except Exception as e:
    ok("relais Vercel (cookie)", False, str(e)[:80])
n = subprocess.run(
    "ps -eo args | grep -c '[r]esumer_chaine'",
    shell=True,
    capture_output=True,
    text=True,
).stdout.strip()
ok(
    "file des résumés finance",
    True,
    f"{n} processus (0 : quota gratuit du jour épuisé ou file finie ; le point relance finance.sh)",
    info=True,
)

alertes = [r for r in res if not r[1]]
if "--json" in sys.argv:
    print(
        json.dumps(
            [{"controle": a, "ok": b, "detail": c} for a, b, c in res],
            ensure_ascii=False,
            indent=1,
        )
    )
else:
    for nom, bon, detail in res:
        print(
            ("OK     " if bon else "ALERTE ") + nom + (f" : {detail}" if detail else "")
        )
    print(f"\n{len(res) - len(alertes)}/{len(res)} contrôles OK")
sys.exit(len(alertes))
