# Comment la Chine copie Claude : 151 millions d'échanges volés

Vidéo : https://youtu.be/lKM4U-o5T6k · durée 1:54 · résumé Gemini (gemini-3.5-flash-lite, lot de 7) du 2026-10-26
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale : Expliquer la technique de la distillation utilisée par des acteurs chinois (comme Alibaba avec ses modèles Qwen) pour copier et s'entraîner à partir des modèles d'Anthropic (Claude) en analysant et en récupérant des millions d'échanges et de données textuelles.
2) Outils, sites ou dépôts GitHub cités :
   - Claude (Anthropic) : non précisé (modèle « prof » / fort).
   - Qwen (Alibaba / Tongyi Lab) : non précisé (modèle « élève »).
   - anthropic.com/threat-intelligence-report-... : URL citée, gratuite, rapport d'Anthropic.
   - mlv.sh/copie : URL citée, gratuite, pour accéder au rapport d'Anthropic décortiqué.
3) Astuces concrètes et réutilisables :
   - Utiliser la technique de la distillation : prendre un modèle fort, récupérer ses réponses, filtrer leur qualité et s'en servir pour entraîner son propre modèle.
   - Structurer le texte en tokens, multiplier les nombres par des poids à travers différentes couches pour comprendre le contexte, et ajuster les poids en comparant la probabilité des tokens de l'élève par rapport au professeur.
4) Chiffres de revenus annoncés : Aucun chiffre de revenus n'est mentionné (les seuls chiffres concernent 151 millions d'échanges volés et 3 mois).
