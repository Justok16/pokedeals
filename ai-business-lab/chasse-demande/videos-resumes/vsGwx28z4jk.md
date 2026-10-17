# Vidéo https://youtu.be/vsGwx28z4jk

> Résumé produit par Gemini (via le relais Vercel) le 25/09/2026. Les chiffres de revenus sont **affirmés par l’auteur de la vidéo, non vérifiés**.

Cette vidéo présente des astuces pour optimiser l'utilisation de Claude Opus 5.5, le nouveau modèle d'Anthropic, dans un contexte de développement d'agents IA et de prompt engineering. L'objectif principal est d'obtenir des résultats plus rapides et de réduire les coûts d'utilisation des systèmes basés sur Claude Code.

### Idée principale

La vidéo détaille 12 astuces, basées sur la documentation officielle d'Anthropic, pour mieux prompté Claude Opus 5.5. Ces astuces visent à rendre vos configurations plus rapides et vos systèmes moins coûteux, en adaptant les méthodes de travail aux spécificités de ce nouveau modèle.

### Outils, sites, ou dépôts GitHub cités

*   **platform.claude.com/docs** : Site officiel de la documentation d'Anthropic sur Claude (Gratuit).
*   **CLAUDO.md** : Fichier d'instructions pour les agents, utilisé par Claude Code (Gratuit, fait partie de l'écosystème Claude).
*   **AGENTS.md** : Fichier d'instructions pour les agents, utilisé par des outils comme Codex et Cursor. Maintenant compatible avec Claude Code (Gratuit, fait partie de l'écosystème Claude/Codex/Cursor).
*   **Codex** : Un outil d'agent de codage mentionné, qui utilise AGENTS.md (Non précisé s'il est payant ou gratuit).
*   **Cursor** : Un outil d'agent de codage mentionné, qui utilise AGENTS.md (Non précisé s'il est payant ou gratuit).
*   **PIL (Python Imaging Library)** : Bibliothèque Python pour le traitement d'images (recadrage, zoom) (Gratuit).
*   **OpenCV** : Bibliothèque Python pour la vision par ordinateur (recadrage, zoom) (Gratuit).
*   **RoboNuggets Guide (PDF)** : Un guide PDF récapitulatif de toutes les astuces et prompts présentés dans la vidéo (Gratuit, lien fourni dans la description de la vidéo).

### Astuces concrètes et réutilisables

1.  **Commencer à "medium effort" (effort moyen) :** Le réglage par défaut recommandé pour Claude Opus 5.5 est désormais "medium". Il offre le meilleur équilibre entre performance et rapidité. Il est conseillé de commencer par ce réglage, puis d'augmenter si la performance est insuffisante.
2.  **Tester vos niveaux d'effort sur votre propre travail :** Plutôt que d'utiliser des paramètres généraux, demandez à Claude de tester une tâche réelle que vous effectuez régulièrement à différents niveaux d'effort (low, medium, high, extra high, max) et de comparer les résultats pour identifier le réglage optimal pour *vos* besoins spécifiques.
3.  **Utiliser `AGENTS.md` dans Claude Code :** La dernière version de Claude Code (2.1.277) prend en charge le fichier `AGENTS.md`. Si votre dossier ne contient pas de `CLAUDE.md`, Claude Code utilisera `AGENTS.md` à la place. Cela permet de maintenir un seul fichier d'instructions si vous utilisez plusieurs agents de codage (comme Claude Code, Codex et Cursor), évitant ainsi la synchronisation entre plusieurs fichiers.
4.  **Changer l'effort en cours de chat sans vider le cache :** Claude Opus 5.5 introduit une fonction (en bêta) qui permet de modifier le niveau d'effort au milieu d'une conversation ("per-message effort change") sans invalider le cache du modèle. Cela signifie que Claude n'a pas à relire toute la conversation, ce qui économise des tokens.
5.  **Utiliser les "banked usage resets" (réinitialisations d'utilisation en banque) :** Claude met en banque des réinitialisations d'utilisation. Si vous atteignez vos limites hebdomadaires, vous pouvez aller dans "Settings → Usage" et cliquer sur "Reset for free" pour réinitialiser vos limites immédiatement. Veillez à vérifier la date d'expiration de ces réinitialisations (celle du lancement d'Opus 5.5 expire le 23 octobre).
6.  **Ne pas demander à Claude de "montrer son raisonnement" :** Les requêtes demandant à Claude de reproduire son raisonnement interne avant de répondre sont désormais signalées sous la catégorie `reasoning_extraction` et peuvent être refusées. Cette fonctionnalité est désactivée dans Opus 5.5, vraisemblablement pour empêcher la "distillation" du modèle par d'autres entreprises.
7.  **Indiquer que les réponses précédentes sont "réglées" :** Dans les chats longs, Claude Opus 5.5 peut parfois revenir sur des réponses précédentes, ce qui peut être inefficace. Pour éviter cela, ajoutez la phrase suivante à la fin de votre prompt système (ou via une "skill" à activer à la demande) : "Once you have answered something, treat that answer as done. On later turns, focus your thinking on what the user is asking now, and don't go back over an earlier answer unless the user asks about it or points out a problem with it."
8.  **Maintenir une liste de tâches (checklist) :** Pour les tâches complexes et longues, Claude 5.5 peut parfois s'arrêter avant la complétion totale. Pour garantir que le travail est entièrement terminé, demandez à Claude de maintenir une checklist des étapes à suivre. Il cochera les éléments au fur et à mesure, assurant une meilleure complétion.
9.  **Définir un budget temps :** Claude Opus 5.5 est capable de faire attention au temps écoulé par tâche. Si vous avez une contrainte de temps, donnez-lui un budget temps explicite (par exemple, "Termine cette tâche en trois minutes."). Il ajustera son rythme pour respecter cette limite.
10. **Utiliser "Time matters" (Le temps compte) :** Si vous ne pouvez pas estimer un budget temps précis, l'ajout des mots "Time matters" à votre prompt peut améliorer la vitesse de complétion de la tâche par Opus 5.5. Les tests d'Anthropic ont montré que les équipes d'agents finissent plus vite si cette instruction est présente.
11. **Fournir un système de conception pour le travail de design :** Sans direction de design, Claude 5.5 a des "défauts de conception" qui donnent un look générique (ex: arrière-plans crème, mots en italique). Pour un résultat plus proche de votre marque, donnez-lui un système de conception (couleurs, polices, composants) ou listez explicitement les styles que vous *ne voulez pas*.
12. **Donner à Claude des outils de recadrage et de zoom pour les images :** Claude Opus 5.5 lit déjà très bien les graphiques et captures d'écran. Cependant, pour des images très denses comme les dessins techniques, il est utile de lui donner accès à des outils de traitement d'image comme les bibliothèques Python PIL et OpenCV. Cela lui permet de zoomer sur les détails pertinents, de se concentrer sur ce qui importe et de réduire l'utilisation de tokens en ne traitant que des crops plus petits de l'image haute résolution.

### Chiffres de revenus annoncés

Aucun chiffre de revenu n'est annoncé par l'auteur dans la vidéo. Le contenu se concentre sur l'optimisation des performances et la réduction des coûts d'utilisation de Claude Opus 5.5.
