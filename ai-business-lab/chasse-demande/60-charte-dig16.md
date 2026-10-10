# Charte graphique DIG16 (08/10/2026)

Demande de l'utilisateur : « ça fait cheap… je veux que ça fasse premium, haute qualité » (couleurs et polices).
S'applique au site dig16.fr (toutes les pages) et à la vidéo de présentation. Les démos clients gardent leur propre identité.

## Couleurs (un seul accent)

| Rôle | Valeur |
|---|---|
| Fond principal (encre chaude) | `#0f0e0c` |
| Surfaces sombres | `#181613` (cartes : dégradé `#1b1915` → `#151310`) |
| Texte sur fond sombre (ivoire) | `#efe9df` ; texte secondaire `#a8a093` |
| Sections claires (ivoire) | `#f3eee5` ; cartes `#fbf8f2` ; texte `#1a1814` ; secondaire `#655e54` |
| **Accent laiton** (boutons, chiffres, filets) | `#c8a46e` ; survol `#d9bb8a` ; texte posé dessus `#14110d` |
| Accent sur fond clair (texte, icônes) | `#7a5a2c` (contraste suffisant sur ivoire) |

Interdits : dégradés orange-violet, bleu nuit, deuxième couleur d'accent.

## Typographies (Google Fonts, gratuites)

- Titres : **Instrument Serif** (poids 400, italique pour l'emphase), interlettrage serré.
- Texte : **Geist** (300 à 600).
- Petites étiquettes : **Geist Mono**, capitales, interlettrage large.

## Détails

- Logo : monogramme « D » en Instrument Serif, laiton, dans un carré filet laiton ; « DIG16 » en Geist 600 espacé.
- Boutons en pilule ; principal laiton sur texte encre ; secondaire filet ivoire translucide.
- Grain très léger sur toute la page (bruit SVG, opacité 5 %).
- Icône d'onglet : monogramme laiton sur encre.

## Documents imprimés (08/10/2026)

- Même rendu sur tous les documents : `outils/marque/charte_documents.py` (polices, couleurs, couverture sombre
  avec signature et emblème).
- Générateurs passés à la charte : `outils/documents_commerciaux.py` (CGV, devis, facture), `outils/plan_complet.py`,
  `outils/campagne_pdf.py`, `outils/marque/flyer.py`.
- Supports écrits à la main : `python3 outils/marque/restyler_supports.py` puis `python3 outils/marque/pdf_supports.py`
  (antisèche, guide de prospection, questionnaires, audit, guides Jarvis et MiniMax, visuel de lancement).
