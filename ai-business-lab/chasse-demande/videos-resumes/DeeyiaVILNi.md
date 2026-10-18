Reel Instagram DeeyiaVILNi (damien.mapt, 47 s, résumé le 18/10/2026)
« Instagram Agent Skill » : 13 skills gratuits pour que Claude prépare le travail d'un community manager Instagram
(posts, commentaires, réponses, profil, planning, recherche des reels qui marchent). « Rien n'est publié sans toi :
l'outil prépare, tu valides. » Le guide de l'auteur s'obtient en commentant « INSTA » (inutile : le dépôt est public).

## Vérifié à la source (18/10/2026)

- Dépôt : https://github.com/Jakeschincariol/instagram-agent-skill — licence **MIT**, auteur Jake Schincariol,
  dernier commit du 13/09/2026 (d03c56b). Lu en entier : 13 `SKILL.md`, 5 petits scripts Python **sans aucun accès
  réseau** ni dépendance. 13 skills et 26 formules d'accroche : **confirmés** (`hooks.json`).
- Le README dit lui-même ses limites : il **ne publie rien** (publier automatiquement viole les conditions d'Instagram) ;
  le score d'accroche repère les accroches faibles mais **ne prédit pas les succès** (test de l'auteur : AUC 0,56, « à
  peine mieux qu'une pièce »). Les vues affichées dans la vidéo (1,2 M, 860 k, 2,4 M) sont des exemples d'écran.
- Plafond de **5 hashtags** par publication depuis le **18/12/2025** : annonce du compte officiel @creators reprise par
  Social Media Today et Reddit ; la page Instagram elle-même n'est pas lisible depuis le conteneur.
- Tout est en anglais (listes de mots, appels à l'action).

| Élément | Pour DIG16 |
|---|---|
| `ig-caption` + `caption.py` (fenêtre de 125 caractères avant « … plus », hashtags ≤ 5, liens morts) | ✅ **Appliqué** : installé dans `.claude/skills/ig-caption/` ; les 5 légendes de la série « Le conseil DIG16 » passées au contrôle : accroche entière dans la fenêtre, 3 hashtags. **Défaut trouvé et corrigé** : l'adresse du guide était écrite dans la légende Instagram, où elle n'est pas cliquable → « sur dig16.fr (lien dans la bio) » ; Facebook garde le lien complet ; TikTok sans « lien dans la bio » tant que sa bio n'a pas de lien |
| `ig-profile` + grille de 100 points | ✅ **Appliqué** : installé ; champ « Nom » Instagram vérifié (« DIG16 · Sites internet Charente », posé le 11/10 : déjà conforme) et 3 publications épinglées proposées dans `67` § 4 ; la grille servira dès la capture du profil |
| `ig-reel` (hookscore, beats), `ig-viral`, `ig-plan`, `ig-carousel`, `ig-story`, `ig-comment`, `ig-reply`, `ig-dm`, `ig-repurpose`, `ig-audit` | 📦 Réserve (réseaux en pause jusqu'au 1er client payant) : à ressortir à la reprise des réseaux ; listes de mots anglaises, à adapter au français |
| `ig-human` (humanize.py) | 📦 Réserve **avec mise en garde** : il remplace l'apostrophe ’ et supprime les espaces insécables, ce qui casse la typographie française ; ne jamais l'appliquer à un texte DIG16 sans retirer ces deux règles |
| Guide de l'auteur (commenter « INSTA ») | Inutile : le dépôt public suffit |
