"""Espaces insécables de la typographie française dans un fichier HTML (texte seulement, hors <script>/<style>).
Usage : python3 typo_fr.py fichier.html [...]"""
import re,sys
R=[('« ','« '),(' »',' »'),(' :',' :'),(' ;',' ;'),(' ?',' ?'),(' !',' !')]
def fix_text(t):
    for a,b in R: t=t.replace(a,b)
    t=re.sub(r"(?<=\w)'(?=\w)",'\u2019',t)  # apostrophe typographique
    t=re.sub(r'(\d) (?=(?:€|%|h\b|min\b|minutes|mois|jours?|ans?|km|semaines?|questions|réponses|prospects|salariés|pages|€/mois|x\b))','\\1\u00a0',t)
    return t
def fix(h):
    out=[];pos=0
    for m in re.finditer(r'<(script|style)\b.*?</\1>',h,re.S|re.I):
        out.append(re.sub(r'>([^<]+)<',lambda x:'>'+fix_text(x.group(1))+'<',h[pos:m.start()]));out.append(m.group(0));pos=m.end()
    out.append(re.sub(r'>([^<]+)<',lambda x:'>'+fix_text(x.group(1))+'<',h[pos:]))
    return ''.join(out)
if __name__=="__main__":
  for f in sys.argv[1:]:
      s=open(f).read();n=fix(s)
      if n!=s: open(f,"w").write(n);print("corrigé",f)
