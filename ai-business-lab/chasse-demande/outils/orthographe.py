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
MOTS_OK = {'Dig', 'EI', 'Charente', 'Claude', 'Gemini', 'Cloudflare', 'RGE', 'Qualibat', 'SIRET', 'SIREN', 'BODACC',
           'CNIL', 'noindex', 'Mappy', 'PagesJaunes'}
def texte(f):
    s = open(f, encoding='utf-8', errors='ignore').read()
    if f.endswith(('.html', '.htm')):
        s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S | re.I)
        s = re.sub(r'<(br|p|div|li|h\d|tr|td|th)\b[^>]*>', '\n', s, flags=re.I)
        s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    return re.sub(r'[ \t  ]+', ' ', s)
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
        garde = [l for l in lignes if l.split('\t')[0] not in IGNORER and l.split('\t')[1].strip() not in MOTS_OK]
        total += len(garde)
        print(f'== {f} : {len(garde)} remarque(s)')
        for l in garde: print('  ' + l)
    return 1 if total else 0
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
