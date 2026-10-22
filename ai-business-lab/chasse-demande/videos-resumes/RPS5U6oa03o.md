# Vidéo YouTube RPS5U6oa03o : « Comment le top 1 % utilise Claude Code » (envoyée le 21/10/2026)

Source : https://youtu.be/RPS5U6oa03o, transcription vidIQ lue en entier le 21/10/2026 (5 crédits). Vidéo d'un
créateur francophone ; passage sponsorisé (proxys résidentiels Data Impulse) ; liens vers ses propres skills (mlv.sh).

| # | Conseil de la vidéo | Ce que DIG16 fait / décision |
|---|---|---|
| 1 | Plus besoin du « mode plan » : donner la tâche, des garde-fous et « quand c'est fini » | ✅ Déjà la façon de travailler (consigne « le meilleur, jusqu'au bout ») |
| 2 | Ne pas changer de modèle à tout bout de champ | ✅ Rien à faire (modèle géré par la session) |
| 3 | **Faire vérifier le travail par l'agent dans un navigateur, en boucle** | ✅ Déjà en place (Playwright, `test_pages.py`, contrôle 44) ; ⛔ **pas** de session navigateur connectée aux comptes de l'utilisateur (règle de sécurité : jamais se connecter à ses comptes personnels) |
| 4 | Fichier de consignes (CLAUDE.md) le plus court possible (≤ 200 lignes) | 🟡 Le nôtre fait 233 lignes / 27 ko : allègement **proposé à l'utilisateur** (déplacer les détails techniques dans des fiches, sans retirer une seule de ses règles) |
| 5 | Supprimer les skills inutiles (commande `/skill-doctor`) | 🟡 À faire avec l'utilisateur : `/skill-doctor` est une commande à taper dans l'interface ; Claude ne peut pas la lancer lui-même |
| 6 | **Remplacer une règle écrite par un blocage automatique (crochet)** | ✅ **Appliqué le 21/10** : crochet `Stop` `.claude/hooks/interdit_sans_reponse.py` qui bloque toute fin de tour du type « pas de réponse » (erreur répétée 4 fois le 20/10) |
| 7 | Préférer l'outil en ligne de commande officiel aux connecteurs | 📦 En réserve : nos connecteurs (Gmail, Drive, Metricool…) marchent ; à ressortir si l'un d'eux casse |
| 8 | Faire travailler l'agent en arrière-plan (tâches programmées) | ✅ Déjà en place (rappels et routines programmés) |
| — | Data Impulse (proxys résidentiels, 1 $/Go, sponsor) | 📦 En réserve, payant : seulement si un scraping légal est bloqué un jour |
| — | Skills de l'auteur (mlv.sh/fc, mlv.sh/fx) | 📦 En réserve, non lus : à lire en entier avant tout usage |
