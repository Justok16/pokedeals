"""Cherche des skills dans l'annuaire public skills.sh (lecture seule, rien n'est installé).
Équivalent sans installation du skill « Find Skills » de Vercel Labs (ressource envoyée le 30/09/2026).
Usage : python3 chercher_skills.py "seo local" "landing page" ...
Rappel : avant toute installation, lire le dépôt en entier (texte seul ou code relu) ; l'installation
de code externe demande l'autorisation de l'utilisateur."""
import sys, json, subprocess, urllib.parse

for q in sys.argv[1:] or ['seo']:
    r = subprocess.run(['curl', '-s', '-m', '20', 'https://skills.sh/api/search?q=' + urllib.parse.quote(q)],
                       capture_output=True, text=True).stdout
    try:
        skills = json.loads(r).get('skills', [])
    except ValueError:
        print(q, ': réponse illisible'); continue
    print(f'== {q} ({len(skills)} résultats)')
    for s in sorted(skills, key=lambda s: -s.get('installs', 0))[:8]:
        print(f"  {s.get('installs', 0):>8} installations  {s['source']}/{s['skillId']}  https://skills.sh/{s['id']}")
