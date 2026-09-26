"""Relevé de Salesforce AppExchange (interface publique de recommandation).

La pagination de l'interface est ignorée et une requête plafonne à ~1 700
résultats : le relevé unit donc plusieurs requêtes par mot-clé. Sortie :
appexchange.csv (titre, éditeur, catégories, note, nombre d'avis)."""
import csv, json, time, urllib.parse, urllib.request

MOTS = ["", "sales", "service", "marketing", "analytics", "integration", "document", "quote", "invoice",
        "billing", "payment", "email", "sms", "calendar", "scheduling", "data", "duplicate", "import",
        "export", "report", "dashboard", "field service", "project", "time", "hr", "recruiting", "survey",
        "forms", "esignature", "cpq", "commerce", "slack", "ai", "security", "backup", "compliance",
        "telephony", "call", "chat", "maps", "territory", "lead", "nonprofit", "education", "health",
        "finance", "insurance", "real estate", "manufacturing", "partner", "portal", "knowledge", "case"]

def lire(u):
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=90))
        except Exception:
            time.sleep(5)
    return None

vus = {}
for m in MOTS:
    q = f"&keyword={urllib.parse.quote(m)}" if m else ""
    d = lire(f"https://api.appexchange.salesforce.com/recommendations/v3/listings?type=apps&page=0&pageSize=2000&language=en{q}")
    for a in (d or {}).get("listings", []):
        vus[a["oafId"]] = [a["oafId"], a["title"], a.get("publisher", ""), "|".join(a.get("listingCategories") or []),
                           a.get("averageRating", ""), a.get("reviewsAmount", 0), (a.get("description") or "")[:150].replace("\n", " ")]
    print(m or "(tout)", len(vus), flush=True)
    time.sleep(1)
w = csv.writer(open("appexchange.csv", "w", newline="", encoding="utf-8"))
w.writerow(["id", "titre", "editeur", "categories", "note", "avis", "description"])
w.writerows(vus.values())
