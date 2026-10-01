"""Résume une vidéo ou un reel Facebook public sans compte (constaté le 01/10/2026) :
lien de partage (facebook.com/share/r/...) -> redirection vers /reel/<id> (en-tête Location, robot
« facebookexternalhit ») -> lecteur intégrable public /plugins/video.php (champs sd_src / hd_src) ->
fichier vidéo -> même chaîne que les reels Instagram (vidéo réduite, Gemini via /api/avis).
Usage : python3 resumer_reel_facebook.py <lien> <dossier_sortie> [cookies.txt]"""
import sys, re, os, html, json, subprocess, urllib.parse
from resumer_reel_instagram import resumer_fichier

UA_ROBOT = 'facebookexternalhit/1.1'   # robot d'aperçu de liens de Facebook : reçoit la redirection publique


def main(lien, dossier, cookies='/tmp/cj.txt'):
    os.makedirs(dossier, exist_ok=True)
    m = re.search(r'/(?:reel|videos)/(\d{8,})', lien)
    if not m:
        if not re.match(r'https://(www\.|m\.)?facebook\.com/share/[rv]/[A-Za-z0-9]+/?', lien):
            sys.exit('lien Facebook non reconnu')
        tetes = subprocess.run(['curl', '-s', '-m', '30', '-D', '-', '-o', '/dev/null', '-A', UA_ROBOT, lien],
                               capture_output=True, text=True).stdout
        m = re.search(r'(?im)^location:.*?/(?:reel|videos)/(\d{8,})', tetes)
        if not m:
            sys.exit('redirection introuvable (vidéo privée ou supprimée ?)')
    vid = m[1]
    cible = urllib.parse.quote(f'https://www.facebook.com/reel/{vid}', safe='')
    page = subprocess.run(['curl', '-s', '-m', '30', '-A', UA_ROBOT, '-H', 'Accept-Language: fr-FR',
                           f'https://www.facebook.com/plugins/video.php?href={cible}&show_text=true'],
                          capture_output=True, text=True).stdout
    u = re.search(r'"sd_src":"([^"]+)"', page) or re.search(r'"hd_src":"([^"]+)"', page)
    if not u:
        sys.exit(f'{vid} : fichier vidéo introuvable dans le lecteur public')
    url = json.loads(f'"{u[1]}"')   # décode les \/ et %
    if urllib.parse.urlparse(url).hostname is None or not urllib.parse.urlparse(url).hostname.endswith('.fbcdn.net'):
        sys.exit('adresse vidéo inattendue (hors fbcdn.net) : arrêt par prudence')
    leg = re.search(r'<div[^>]*data-testid="post_message"[^>]*>(.*?)</div>', page, re.S) or \
        re.search(r'<meta property="og:description" content="([^"]*)"', page)
    legende = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', leg[1]))).strip() if leg else ''
    brut = f'/tmp/reel-fb{vid}.mp4'
    subprocess.run(['curl', '-s', '-f', '-m', '180', '-o', brut, url], check=True)
    return resumer_fichier(brut, f'fb-{vid}', legende, dossier, cookies, 'vidéo Facebook')


if __name__ == '__main__':
    main(*sys.argv[1:4])
