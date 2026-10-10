# J'ai créé une IA qui automatise ma routine matinale (avec n8n).

Vidéo : https://youtu.be/L09kacrneOc · durée 20:50 · résumé Gemini (gemini-3.5-flash-lite, lot de 5) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Ce tutoriel montre comment automatiser la collecte de données sur Internet (RSS), les agréger, les résumer à l'aide d'une IA (OpenAI), et envoyer automatiquement une newsletter quotidienne par e-mail, en utilisant **n8n** (en local ou hébergé sur un VPS) et **Hostinger**.
2) **Outils, sites ou dépôts GitHub cités** :
   - **n8n** (n8n.io) : Logiciel d'automatisation de flux de travail. Gratuit (limité) / Payant (à partir de 24 $/mois en mode géré), ou gratuit en open-source auto-hébergé (code source disponible sur GitHub). Sert à créer des automatisations et des agents IA.
   - **GitHub** : Plateforme d'hébergement de code source (mentionnée pour trouver le code source de n8n). Gratuit.
   - **Hostinger** (hostinger.com/mattn8n) : Service d'hébergement web/VPS. Payant (plan KVM 2 à partir de 6,99 $/mois, avec réduction possible en utilisant le code promo `mattwolf`). Sert à héberger n8n sur un serveur privé virtuel pour qu'il tourne 24h/24.
   - **TechCrunch** (techcrunch.com) : Site d'actualité. Gratuit. Fournit un flux RSS d'actualités.
   - **Engadget** (engadget.com) : Site d'actualité. Gratuit. Fournit un flux RSS.
   - **Wired** (wired.com) : Site d'actualité. Gratuit. Fournit un flux RSS.
   - **The Verge** (theverge.com) : Site d'actualité. Gratuit. Fournit un flux RSS.
   - **OpenAI / ChatGPT** (platform.openai.com) : Modèles de langage par API. Payant (nécessite une clé API OpenAI). Sert à agréger, résumer et structurer le contenu des actualités en texte compréhensible et non technique.
   - **Gmail** : Service de messagerie de Google. Gratuit. Sert à envoyer la newsletter quotidienne générée automatiquement.
   - **Google Cloud Console** : Plateforme de développement Google (console.cloud.google.com). Gratuit. Sert à configurer les identifiants OAuth pour connecter Gmail à n8n.
   - **Mailchimp** : Service d'e-mailing (mentionné comme alternative pour envoyer des newsletters). Payant/Gratuit (non précisé).
3) **Astuces concrètes et réutilisables** :
   - Automatiser la récupération quotidienne de flux RSS de plusieurs sites web (TechCrunch, Engadget, etc.) pour en faire un résumé unique par IA.
   - Utiliser n8n en auto-hébergement local (via la commande `npx n8n` dans le terminal) pour tester gratuitement des automatisations.
   - Héberger n8n sur un VPS (comme Hostinger) pour que l'automatisation tourne en continu, même lorsque l'ordinateur principal est éteint.
   - Utiliser un nœud de type « Split Out » pour diviser un tableau d'URL en flux individuels afin de les lire un par un, puis utiliser le nœud « Aggregate » pour regrouper tous les extraits de texte en un seul bloc avant de l'envoyer à l'IA.
   - Convertir le texte brut généré par l'IA du format Markdown vers HTML (grâce au nœud « Markdown » de n8n) pour qu'il s'affiche correctement dans un e-mail.
4) **Chiffres de revenus annoncés** : Non précisé.
