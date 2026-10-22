# Vidéo YouTube dl78bCncIe0 : « Une équipe de 4 IA qui se contrôlent (OpenCode) » (envoyée le 21/10/2026)

Source : https://youtu.be/dl78bCncIe0, transcription vidIQ lue en entier le 21/10/2026.

Idée centrale : 4 agents (architecte, développeur, relecteur, testeur) + un chef ; **seul le développeur peut modifier**
le travail ; le relecteur et le testeur n'ont **pas le droit d'écrire** : ils doivent décrire le problème (quel fichier,
quel défaut, quel résultat attendu) et le développeur corrige ; passage de relais par fichiers écrits ; 3 allers-retours
au plus, puis le chef rend la main à l'humain avec la liste de ce qui n'a pas pu être vérifié.

| Conseil | Décision DIG16 |
|---|---|
| Relecteur **sans droit de modifier** (sinon il corrige en silence et personne ne voit le défaut) | ✅ **Appliqué le 21/10** dans `44-controle-qualite.md` : relecture finale par un agent en lecture seule (type « Explore ») qui rend un verdict « validé / à refaire » avec la liste des défauts |
| Testeur « client difficile » : cas normal, entrées vides, pannes | ✅ Déjà dans `44` et `test_pages.py` ; skill `break-ui` disponible |
| 3 allers-retours maximum puis l'humain tranche | ✅ Repris dans `44` |
| OpenCode (outil) | 📦 Réserve : Claude Code fait déjà ce travail avec ses sous-agents |
