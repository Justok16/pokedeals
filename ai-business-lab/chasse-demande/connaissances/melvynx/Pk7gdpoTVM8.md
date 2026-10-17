# Économise +99$ en 5 Minutes avec cette IA !

Vidéo : https://youtu.be/Pk7gdpoTVM8 · durée 8:51 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-17
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Remplacer l'API d'OpenAI par des modèles open source (comme Mistral via Perplexity) dans une application pour réduire considérablement les coûts d'appel à l'API tout en conservant des performances similaires.
2) **Outils, sites ou dépôts cités :**
   - **Mistral :** Modèle open source (performances comparables à GPT-4 pour certaines tâches).
   - **Perplexity AI (perplexity.ai) :** Plateforme fournissant une API permettant d'accéder à des modèles open source (comme Mistral). Modèle payant basé sur l'achat de crédits (montant flexible, ex. 10 $).
   - **PowerPost :** Application présentée dans l'exemple (affichage et chat avec des articles).
   - **Next AI (cours en description) :** Cours de formation payant/gratuit (non précisé en détail, mais mentionné comme "cours gratuit" pour les abonnés ou premier lien).
3) **Astuces concrètes et réutilisables :**
   - Utiliser un modèle open source (Mistral) via une API alternative (Perplexity) au lieu d'OpenAI pour baisser les coûts.
   - Configurer le fichier `.env` en y ajoutant la clé API de Perplexity (`PERPLEXITY_AI_KEY`) et en changeant la `baseURL` de l'API OpenAI vers celle de Perplexity (`https://api.perplexity.ai`).
   - Sélectionner le bon modèle dans le code (ex: `mistral-8x7b-instruct`).
4) **Chiffres de revenus annoncés :** Non précisé (l'accent est mis sur la réduction des coûts, environ 100 fois moins cher, et non sur des gains financiers).
