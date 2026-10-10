# Utilisez N8N pour créer une newsletter personnalisée alimentée par l'IA

Vidéo : https://youtu.be/jAEG5RMxvNQ · durée 27:44 · résumé Gemini (gemini-3.5-flash-lite, lot de 5) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale** :  
   Cette vidéo montre comment créer un système automatisé de veille financière de A à Z en utilisant **n8n** (un outil d'automatisation de type Make/Zapier), **Gmail** (pour collecter et marquer les e-mails), **Google Gemini** (pour résumer et traiter le contenu textuel), et un serveur VPS hébergé sur **Hostinger** pour faire tourner n8n en continu et à moindre coût.

2. **Outils, sites et dépôts GitHub cités** :  
   - **n8n** : Outil d'automatisation de workflows (version cloud payante ou version open-source auto-hégeable gratuite disponible sur GitHub). Sert à connecter différentes applications et automatiser des processus.
   - **Gmail** : Service de messagerie de Google (gratuit) utilisé pour recevoir et marquer les newsletters.
   - **Google Gemini (via Google AI Studio)** : Modèle de langage (freemium / payant à l'utilisation via l'API) utilisé pour résumer et structurer le contenu des newsletters en HTML.
   - **Hostinger** : Hébergeur web et de serveurs VPS (payant, avec des réductions Black Friday mentionnées). Sert à héberger n8n en auto-hébergement pour qu'il tourne 24h/24.
   - **Exploding Topics (explodingtopics.com)** : Site de veille de tendances (gratuit/payant) source de listes de newsletters financières.
   - **GitHub (dépôt n8n)** : Plateforme de code (gratuit) pour télécharger et installer n8n localement ou sur un serveur.

3. **Astuces concrètes et réutilisables** :  
   - Créer une adresse Gmail dédiée pour s'inscrire à toutes ses newsletters et éviter de polluer sa boîte mail principale.
   - S'auto-héberger sur un VPS (comme Hostinger avec l'offre KVM 2) pour s'assurer que les automatisations n8n tournent en continu sans dépendre d'un ordinateur personnel allumé.
   - Utiliser le nœud "Aggregate" dans n8n pour fusionner des dizaines d'e-mails reçus en un seul gros document texte avant de l'envoyer à une IA.
   - Convertir les données textuelles en HTML via le nœud "Markdown" pour conserver la mise en forme (liens, URLs) lors de l'envoi de l'e-mail récapitulatif.
   - Configurer le nœud de lecture Gmail sur "Unread Status" avec "Unread emails only" et ajouter un nœud "Mark as read" en parallèle pour automatiser le nettoyage de la boîte de réception après traitement.
   - Utiliser les codes promo (comme `MATTWOLFE`) pour obtenir des réductions supplémentaires sur les hébergements web.

4. **Chiffres de revenus annoncés** :  
   - Non précisé

---
