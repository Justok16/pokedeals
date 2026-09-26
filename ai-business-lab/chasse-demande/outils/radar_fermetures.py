"""Radar des fermetures annoncées (API, intégrations, fonctions) chez les
grandes plateformes. Lit les journaux officiels des développeurs, garde les
phrases qui annoncent un retrait daté dans le futur. Sortie : radar.md.

Leçon d'Invoice Stack (voir 20-hubspot-comptabilite-grille.md) : l'argent B2B
va à celui qui est prêt AVANT la date de fermeture.
"""
import html, re, urllib.request
from datetime import date

SOURCES = {
    "Shopify": "https://shopify.dev/changelog/feed.xml",
    "HubSpot": "https://developers.hubspot.com/changelog/rss.xml",
    "Xero": "https://developer.xero.com/changelog",
    "Intuit QuickBooks": "https://developer.intuit.com/app/developer/qbo/docs/release-notes",
    "Zoom": "https://developers.zoom.us/changelog/",
    "Slack": "https://docs.slack.dev/changelog/tags/deprecation/",
    "Meta Graph API": "https://developers.facebook.com/docs/graph-api/changelog/",
    "Google Workspace": "https://developers.google.com/workspace/release-notes",
    "Square": "https://developer.squareup.com/docs/changelog/connect",
    "Stripe": "https://stripe.com/docs/changelog",
    "eBay": "https://developer.ebay.com/develop/apis/api-deprecation-status",
    "Atlassian": "https://developer.atlassian.com/changelog/",
    "Google Ads": "https://developers.google.com/google-ads/api/docs/sunset-dates",
    "Amazon SP-API": "https://developer-docs.amazon.com/sp-api/changelog",
    "Mailchimp": "https://mailchimp.com/developer/release-notes/",
    "Klaviyo": "https://developers.klaviyo.com/en/docs/changelog_",
    "Notion": "https://developers.notion.com/page/changelog",
    "Airtable": "https://airtable.com/developers/web/api/changelog",
    "Zendesk": "https://developer.zendesk.com/api-reference/changelog/changelog/",
    "Miro": "https://developers.miro.com/changelog",
    "Pipedrive": "https://developers.pipedrive.com/changelog",
    "monday.com": "https://developer.monday.com/api-reference/changelog",
    "Webflow": "https://developers.webflow.com/data/changelog",
    "Asana": "https://developers.asana.com/docs/change-log",
    "Trello": "https://developer.atlassian.com/cloud/trello/changelog/",
    "Intercom": "https://developers.intercom.com/docs/build-an-integration/learn-more/rest-apis/api-changelog",
    "GitHub": "https://docs.github.com/en/rest/about-the-rest-api/breaking-changes",
    "Dropbox": "https://developer.dropbox.com/changelog",
    "Calendly": "https://developer.calendly.com/changelog",
    "Microsoft (fin de support 2027)": "https://learn.microsoft.com/en-us/lifecycle/end-of-support/end-of-support-2027",
}
MOTS = re.compile(r"deprecat|sunset|retir|end[- ]of[- ]life|decommission|no longer (be )?(available|supported)|will be removed|shut ?down", re.I)
MOIS = "January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
DATE = re.compile(rf"(({MOIS})\.? \d{{1,2}},? (20\d\d))|((20\d\d)-(\d\d)-(\d\d))|(({MOIS}) (20\d\d))|(Q[1-4] (20\d\d))", re.I)

def texte(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    s = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    s = re.sub(r"<(script|style)\b.*?</\1\s*>", " ", s, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))

def annee(m):
    return int(next(g for g in (m.group(3), m.group(5), m.group(10), m.group(12)) if g))

def main():
    auj = date.today().year
    lignes = [f"# Radar des fermetures — relevé du {date.today().isoformat()}\n"]
    for nom, url in SOURCES.items():
        try:
            t = texte(url)
        except Exception as e:
            lignes.append(f"\n## {nom}\n\n- (source illisible : {e})\n")
            continue
        vus = set()
        trouves = []
        for phrase in re.split(r"(?<=[.!?])\s+", t):
            if len(phrase) > 400 or not MOTS.search(phrase):
                continue
            dates = list(DATE.finditer(phrase))
            if not dates or max(annee(d) for d in dates) < auj:
                continue
            cle = phrase[:120]
            if cle not in vus:
                vus.add(cle)
                # [clients] : pas de jargon de développeur, donc peut toucher des
                # utilisateurs non techniques (le cas qui a fait Invoice Stack).
                dev = re.search(r"\b(API|SDK|endpoint|scope|CLI|webhook|v\d+(\.\d+)?)\b", phrase)
                trouves.append(("" if dev else "[clients] ") + phrase.strip())
        lignes.append(f"\n## {nom} ({len(trouves)})\n\nSource : {url}\n")
        lignes += [f"- {p}" for p in trouves[:25]]
    open("radar.md", "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes)[:200])

if __name__ == "__main__":
    main()
