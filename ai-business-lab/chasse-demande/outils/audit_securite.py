"""Audit de sécurité d'un site web, en français (Dig, 30/09/2026).

Deux modes :
- PASSIF (par défaut) : pour tout site, y compris un concurrent. On ne lit que ce que le site
  montre à n'importe quel visiteur : la page d'accueil (1 requête HTTPS + 1 requête HTTP pour
  la redirection), ses en-têtes, son certificat et son code HTML. Aucun test d'intrusion,
  aucune URL cachée essayée, aucun formulaire envoyé.
- PROPRIÉTAIRE (--proprietaire) : UNIQUEMENT sur nos sites ou ceux d'un client qui nous a
  donné son accord écrit. Ajoute la recherche de fichiers sensibles exposés (/.env, /.git…).
  Rappel : accéder ou se maintenir frauduleusement dans un système informatique est puni de
  3 ans d'emprisonnement et 100 000 € d'amende (Code pénal, art. 323-1, version en vigueur
  depuis le 26/01/2023, lu sur Légifrance le 30/09/2026).

Usage : python3 audit_securite.py https://exemple.fr [--proprietaire] [--json]
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

UA = 'Mozilla/5.0 (compatible; audit-dig/1.0; controle passif)'


def curl(url, tete=False, suivre=True, max_octets=3_000_000):
    """Une requête GET (ou HEAD) ; renvoie (code, en-têtes dict en minuscules, corps, url finale)."""
    cmd = ['curl', '-s', '-m', '25', '-A', UA, '-D', '-', '-o', '-', '--max-filesize', str(max_octets),
           '-w', '\n__FIN__%{http_code} %{url_effective}']
    if suivre:
        cmd.append('-L')
    if tete:
        cmd.append('-I')
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, errors='replace').stdout
    corps, _, fin = r.rpartition('\n__FIN__')
    code, _, finale = fin.partition(' ')
    # garder le dernier bloc d'en-têtes (après les redirections)
    blocs = re.split(r'\r?\n\r?\n', corps)
    entetes, reste = {}, corps
    i = 0
    while i < len(blocs) and re.match(r'HTTP/[\d.]+ \d{3}', blocs[i]):
        entetes = {}
        for ligne in blocs[i].splitlines()[1:]:
            k, _, v = ligne.partition(':')
            entetes.setdefault(k.strip().lower(), []).append(v.strip())
        i += 1
    reste = '\n\n'.join(blocs[i:])
    return int(code or 0), entetes, reste, finale.strip()


def certificat(hote):
    """Date d'expiration et émetteur du certificat HTTPS réellement présenté par le site.
    Lecture via curl (tunnel CONNECT, qui laisse passer le vrai certificat) ; une lecture directe
    peut être interceptée par un proxy local et donner un faux émetteur."""
    r = subprocess.run(['curl', '-svI', '-m', '20', f'https://{hote}'], capture_output=True, text=True).stderr
    m = re.search(r'expire date: (.+)', r)
    iss = re.search(r'issuer: .*?O=([^;]+)', r)
    if m:
        fin = datetime.strptime(m[1].strip(), '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
        return (fin - datetime.now(timezone.utc)).days, iss[1].strip() if iss else '?', None
    err = re.search(r'(SSL certificate problem[^\n]*|certificate has expired[^\n]*)', r)
    return None, None, err[1] if err else 'lecture impossible'


def audit(url, proprietaire=False):
    u = urlparse(url if '://' in url else 'https://' + url)
    hote = u.hostname
    res = []  # (gravité, contrôle, constat)

    def note(grav, controle, constat):
        res.append((grav, controle, constat))

    code, h, html, finale = curl(f'https://{hote}{u.path or "/"}')
    if not code:
        note('critique', 'Accès HTTPS', 'le site ne répond pas en HTTPS')
        return res
    get = lambda k: (h.get(k) or [''])[-1]

    # 1. HTTPS et redirection
    c80, h80, _, fin80 = curl(f'http://{hote}/', suivre=True)
    if fin80.startswith('https://'):
        note('ok', 'Redirection HTTP → HTTPS', 'oui')
    else:
        note('élevé', 'Redirection HTTP → HTTPS', "la version http:// n'est pas redirigée vers https://")
    jours, emetteur, err = certificat(hote)
    if jours is None:
        note('élevé', 'Certificat HTTPS', f'illisible ({err})')
    elif jours < 0:
        note('critique', 'Certificat HTTPS', f'EXPIRÉ depuis {-jours} jours')
    elif jours < 15:
        note('élevé', 'Certificat HTTPS', f'expire dans {jours} jours ({emetteur})')
    else:
        note('ok', 'Certificat HTTPS', f'valide encore {jours} jours ({emetteur})')

    # 2. En-têtes de sécurité
    hsts = get('strict-transport-security')
    m = re.search(r'max-age=(\d+)', hsts)
    if not hsts:
        note('moyen', 'HSTS (HTTPS imposé)', 'absent')
    elif m and int(m[1]) < 15552000:
        note('faible', 'HSTS (HTTPS imposé)', f'durée courte ({int(m[1]) // 86400} jours ; 180 jours ou plus conseillés)')
    else:
        note('ok', 'HSTS (HTTPS imposé)', hsts[:80])
    csp = get('content-security-policy')
    if not csp:
        note('moyen', 'CSP (politique de contenu)', 'absente : pas de barrière contre les scripts injectés')
    else:
        faibles = [x for x in ("'unsafe-eval'", '*', 'http:') if re.search(r"(^|[\s;])" + re.escape(x) + r"($|[\s;])", csp)]
        note('faible' if faibles else 'ok', 'CSP (politique de contenu)',
             ('présente mais permissive : ' + ', '.join(faibles)) if faibles else 'présente')
    if 'frame-ancestors' in csp or get('x-frame-options'):
        note('ok', 'Protection contre l’intégration piégée (clickjacking)', 'oui')
    else:
        note('moyen', 'Protection contre l’intégration piégée (clickjacking)', 'absente (X-Frame-Options ou frame-ancestors)')
    note('ok' if get('x-content-type-options').lower() == 'nosniff' else 'faible', 'X-Content-Type-Options',
         get('x-content-type-options') or 'absent')
    note('ok' if get('referrer-policy') else 'faible', 'Referrer-Policy', get('referrer-policy') or 'absente')
    note('ok' if get('permissions-policy') else 'faible', 'Permissions-Policy', get('permissions-policy')[:60] or 'absente')

    # 3. Informations qui aident un attaquant
    fuites = [f'{k}: {get(k)}' for k in ('server', 'x-powered-by', 'x-aspnet-version', 'x-generator')
              if get(k) and re.search(r'\d', get(k))]
    gen = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if gen and re.search(r'\d', gen[1]):
        fuites.append('meta generator : ' + gen[1])
    wpver = re.search(r'ver=(\d+\.\d+(?:\.\d+)?)', html) if 'wp-content' in html else None
    if wpver:
        fuites.append('WordPress (version visible dans les liens : ' + wpver[1] + ')')
    note('faible' if fuites else 'ok', 'Versions de logiciels affichées', '; '.join(fuites) or 'aucune')

    # 4. Cookies
    mauvais = []
    for ck in h.get('set-cookie', []):
        nom = ck.split('=', 1)[0]
        manque = [a for a in ('Secure', 'HttpOnly', 'SameSite') if a.lower() not in ck.lower()]
        if manque:
            mauvais.append(f"{nom} (manque {', '.join(manque)})")
    if h.get('set-cookie'):
        note('moyen' if mauvais else 'ok', 'Cookies', '; '.join(mauvais) or 'attributs de sécurité présents')

    # 5. Contenu de la page
    mixte = sorted(set(re.findall(r'(?:src|href|action)=["\'](http://[^"\']+)', html, re.I)))
    mixte = [x for x in mixte if not x.startswith('http://www.w3.org')]
    note('moyen' if mixte else 'ok', 'Contenu mixte (http:// dans une page https)',
         f'{len(mixte)} ressource(s), ex. {mixte[0][:70]}' if mixte else 'aucun')
    scripts_ext = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\'][^>]*>', html, re.I)
    tiers = [s for s in scripts_ext if urlparse(s).hostname and not urlparse(s).hostname.endswith(hote)]
    sans_sri = [s for s in tiers if not re.search(r'<script[^>]+src=["\']' + re.escape(s) + r'["\'][^>]*integrity=', html, re.I)]
    note('faible' if sans_sri else 'ok', 'Scripts tiers sans empreinte (SRI)',
         f'{len(sans_sri)} sur {len(tiers)} (ex. {urlparse(sans_sri[0]).hostname})' if sans_sri else f'{len(tiers)} script(s) tiers')
    formulaires = re.findall(r'<form[^>]*>', html, re.I)
    f_http = [f for f in formulaires if re.search(r'action=["\']http://', f, re.I)]
    if f_http:
        note('élevé', 'Formulaires', 'envoi en http:// non chiffré')
    elif formulaires:
        note('ok', 'Formulaires', f'{len(formulaires)} formulaire(s), envoi chiffré')
    traceurs = [t for t in ('googletagmanager', 'google-analytics', 'connect.facebook.net', 'hotjar', 'clarity.ms') if t in html]
    bandeau = re.search(r'tarteaucitron|axeptio|cookiebot|didomi|onetrust|consent', html, re.I)
    if traceurs and not bandeau:
        note('moyen', 'Traceurs et consentement (RGPD)', 'traceurs (' + ', '.join(traceurs) + ') sans outil de consentement détecté')
    elif traceurs:
        note('ok', 'Traceurs et consentement (RGPD)', 'traceurs + outil de consentement détecté')
    ml = re.search(r'mentions[\s-]*l[ée]gales', html, re.I)
    note('ok' if ml else 'moyen', 'Lien « mentions légales » (obligation légale)', 'trouvé' if ml else 'introuvable sur la page d’accueil')

    # 6. Mode propriétaire : fichiers sensibles exposés (JAMAIS sur un site tiers sans accord écrit)
    if proprietaire:
        for chemin, signe in (('/.env', r'^[A-Z_]+=.+'), ('/.git/HEAD', r'^ref: refs/'), ('/wp-config.php.bak', r'DB_PASSWORD'),
                              ('/backup.zip', None), ('/.DS_Store', None)):
            c, hh, corps, _ = curl(f'https://{hote}{chemin}', suivre=False, max_octets=200_000)
            expose = c == 200 and (re.search(signe, corps, re.M) if signe else len(corps) > 0 and 'html' not in get('content-type'))
            note('critique' if expose else 'ok', f'Fichier sensible {chemin}', 'EXPOSÉ' if expose else 'non exposé')
        c, hs, corps, _ = curl(f'https://{hote}/.well-known/security.txt', suivre=True, max_octets=50_000)
        ok = c == 200 and 'text/plain' in (hs.get('content-type') or [''])[-1] and re.search(r'^Contact:\s*\S+', corps, re.M | re.I)
        note('ok' if ok else 'faible', 'security.txt (contact sécurité)', 'présent' if ok else 'absent (recommandé)')
    return res


ORDRE = {'critique': 0, 'élevé': 1, 'moyen': 2, 'faible': 3, 'ok': 4}
POIDS = {'critique': 30, 'élevé': 15, 'moyen': 7, 'faible': 3, 'ok': 0}

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    prop = '--proprietaire' in sys.argv
    r = audit(args[0], proprietaire=prop)
    note_finale = max(0, 100 - sum(POIDS[g] for g, _, _ in r))
    if '--json' in sys.argv:
        print(json.dumps({'site': args[0], 'mode': 'propriétaire' if prop else 'passif', 'note': note_finale,
                          'controles': [dict(gravite=g, controle=c, constat=x) for g, c, x in r]}, ensure_ascii=False, indent=1))
    else:
        print(f"Audit de sécurité — {args[0]} — mode {'propriétaire' if prop else 'passif'} — {datetime.now():%d/%m/%Y %H:%M}")
        for g, c, x in sorted(r, key=lambda t: ORDRE[t[0]]):
            print(f'  [{g:^8}] {c} : {x}')
        print(f'Note : {note_finale}/100 (100 = aucun défaut détecté par ces contrôles, ce qui ne garantit pas l’absence de faille)')
