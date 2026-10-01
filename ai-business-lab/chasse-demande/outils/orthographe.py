"""Contrôle orthographe et grammaire (LanguageTool, hors ligne) du texte visible de fichiers HTML ou Markdown.
Usage : python3 orthographe.py fichier.html [...]   (installation : sh outils/orthographe/installer.sh)
Affiche chaque remarque : règle, mot, suggestions, contexte. Code de sortie 1 s'il y a des remarques.
Ignorées : règles typographiques déjà traitées par typo_fr.py et faux positifs connus (voir IGNORER)."""
import sys, os, re, html, subprocess, tempfile
ICI = os.path.dirname(os.path.abspath(__file__))
IGNORER = {'WHITESPACE_RULE', 'FRENCH_WHITESPACE', 'COMMA_PARENTHESIS_WHITESPACE', 'UPPERCASE_SENTENCE_START',
           'APOS_TYP', 'FRENCH_WORD_REPEAT_RULE', 'DOUBLE_PUNCTUATION', 'TIRET', 'ESPACE_UNITES',
           # Conseils de style (chiffres en lettres) et effets du texte extrait sans ponctuation entre blocs (testé le 01/10)
           'NOMBRES_EN_LETTRES', 'NOMBRES_EN_LETTRES_2', 'NOMBRES_EN_LETTRES_2_IMPROVED', 'PRONOMS_PERSONNELS_MINUSCULE',
           'POINT', 'JOURS', 'VIRGULE_DEBUT_DE_PHRASE', 'VIRG_NON_TROUVEE', 'PLACE_DE_LA_VIRGULE', 'FR_REPEATEDWORDS', 'REP_CONTENT'}
MOTS_OK = {'Truc', 'Dig', 'EI', 'Charente', 'Claude', 'Gemini', 'Cloudflare', 'RGE', 'Qualibat', 'SIRET', 'SIREN', 'BODACC',
           'CNIL', 'noindex', 'Mappy', 'PagesJaunes'}
def texte(f):
    s = open(f, encoding='utf-8', errors='ignore').read()
    if f.endswith(('.html', '.htm')):
        # Texte tel que le navigateur l'affiche (innerText respecte le CSS : blocs séparés, mots non coupés
        # par une balise) ; code et commandes exclus. Repli sur l'extraction simple si Chromium manque.
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                nav = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
                pg = nav.new_page(); pg.goto('file://' + os.path.abspath(f)); pg.wait_for_timeout(300)
                s = pg.evaluate("() => { document.querySelectorAll('code,kbd,pre').forEach(e => e.replaceWith('Truc'));"
                                " document.querySelectorAll('script,style').forEach(e => e.remove());"
                                " document.querySelectorAll('body *').forEach(e => { const d = getComputedStyle(e.parentElement).display;"
                                " if (/flex|grid/.test(d)) e.append(' '); });"
                                " return document.body.innerText; }")
                nav.close()
        except Exception:
            s = re.sub(r'<(script|style|code|kbd|pre)\b.*?</\1>', ' ', s, flags=re.S | re.I)
            s = re.sub(r'<(br|p|div|li|h\d|tr|td|th)\b[^>]*>', '\n', s, flags=re.I)
            s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    else:  # Markdown : blocs et fragments de code
        s = re.sub(r'```.*?```', ' ', s, flags=re.S)
        s = re.sub(r'`[^`\n]+`', ' ', s)
    s = re.sub(r'https?://\S+|\b[\w.-]+\.(?:fr|com|io|ai|app|dev|org|net)\b\S*', 'Truc', s)  # adresses web (mot neutre : évite « avec , format »)
    return re.sub(r'[ \t  ]+', ' ', s)
def nom_propre(regle, mot):
    """Mot inconnu commençant par une majuscule, ou avec chiffre, _ ou majuscule interne : nom de marque,
    de personne ou terme technique (Pinokio, Wan2GP, ElevenLabs). Pas des fautes de français : les vérifier
    à la source. Option --noms pour les afficher quand même."""
    return regle in ('FR_SPELLING_RULE', 'NUMBERS_IN_WORDS') and bool(re.search(r'^[A-ZÉ]|\d|_|[a-z][A-Z]', mot))
def main(fichiers):
    if not os.path.isdir('/tmp/lt/lib'):
        subprocess.run(['sh', os.path.join(ICI, 'orthographe', 'installer.sh')], check=True)
    total = 0
    for f in fichiers:
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as t:
            t.write(texte(f))
        r = subprocess.run(['java', '-cp', '/tmp/lt/lib/*', os.path.join(ICI, 'orthographe', 'Verif.java'), t.name],
                           capture_output=True, text=True)
        os.unlink(t.name)
        lignes = [l for l in r.stdout.splitlines() if l.count('\t') >= 3]
        garde = [l for l in lignes if l.split('\t')[0] not in IGNORER and l.split('\t')[1].strip() not in MOTS_OK
                 and (NOMS or not nom_propre(l.split('\t')[0], l.split('\t')[1].strip()))]
        total += len(garde)
        print(f'== {f} : {len(garde)} remarque(s)')
        for l in garde: print('  ' + l)
    return 1 if total else 0
NOMS = '--noms' in sys.argv
if __name__ == '__main__':
    sys.exit(main([a for a in sys.argv[1:] if a != '--noms']))
