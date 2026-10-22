# Grok Bot : un VRAI employé qui travaille 24 h/24 ?

Vidéo : https://youtu.be/LS7qQJcLUgM · durée 22:07 · résumé Gemini (gemini-3.6-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet de la vidéo, structuré selon vos exigences :

---

### 1) Idée principale
L'auteur réalise un crash-test critique et sans filtre de **Grok Bot** (un logiciel d'agents IA autonomes tournant sur une machine virtuelle Linux distante, lié à l'écosystème Cursor). Il tente d'automatiser des tâches réelles (répondre à des commentaires LinkedIn/YouTube, interagir sur Discord, configurer du code GitHub). Son constat est très négatif : l'outil est jugé extrêmement lent, bloqué par les captchas et les restrictions d'IP (rate limits), et peu utilisable en l'état (note attribuée : 2/10). En parallèle, il promeut sa formation pour apprendre à utiliser des outils comme Claude Code et Cursor pour devenir *AI Engineer*.

---

### 2) Outils, sites ou dépôts GitHub cités

*   **Grok Bot**
    *   *Statut :* Payant / Freemium (nécessite un compte/abonnement Cursor, détails de prix exacts non précisés).
    *   *Utilité :* Application de bureau (macOS) exécutant des agents IA autonomes sur une VM distante pour réaliser des tâches de travail (navigateur, terminal, intégrations).
*   **Cursor (`cursor.sh`)**
    *   *Statut :* Freemium (accès gratuit avec options payantes).
    *   *Utilité :* Éditeur de code assisté par IA, servant ici également d'infrastructure d'authentification pour Grok Bot.
*   **Claude Code**
    *   *Statut :* Non précisé dans la vidéo.
    *   *Utilité :* Agent IA de développement mentionné comme l'un des outils phares pour coder rapidement.
*   **Codex**
    *   *Statut :* Non précisé dans la vidéo.
    *   *Utilité :* Outil d'IA pour développeurs cité dans la présentation de la formation.
*   **Site de formation : `mlv.sh/formation-ai` (ou `mlv.sh/fa`)**
    *   *Statut :* Mini-formation / Masterclass gratuite (accès sur inscription e-mail).
    *   *Utilité :* Plateforme de l'auteur ("AI Blueprint") pour apprendre à maîtriser les agents IA (Claude Code, Cursor, etc.) et devenir AI Engineer.
*   **Plateformes intégrées / testées (LinkedIn, Discord, GitHub, YouTube Studio, Lumail, Stripe, Notion, Vercel)**
    *   *Statut :* Services tiers (gratuits/payants selon le service).
    *   *Utilité :* Outils de travail du quotidien que Grok Bot tente de manipuler via API/MCP ou via navigateur web.

---

### 3) Astuces concrètes et réutilisables

1.  **Connexion sur environnement distant (VM/VPS) :** Lors de l'utilisation d'agents IA sur navigateur distant, privilégiez l'authentification par **QR Code** via smartphone (ex: Discord) plutôt que la saisie manuelle des identifiants/mots de passe, souvent ralentie par la latence de la VM.
2.  **Enregistrement de compétences ("Teach a task") :** Pour apprendre une routine à un agent IA sans API, enregistrez manuellement votre écran en effectuant l'action exacte (ex: filtrer les commentaires YouTube "sans réponse" et vieux de plus de 30 jours, écrire un modèle de réponse court, puis valider). L'IA convertit cette séquence en "Skill" réutilisable.
3.  **Vigilance sur les IP de datacenters / VPS :** Automatiser des actions web via des machines virtuelles distantes déclenche fréquemment des protections de sécurité avancées (CAPTCHA complexes, vérification faciale par selfie sur Google, erreurs `HTTP 429 Rate Limit` sur GitHub à cause des IP partagées Cloudflare).

---

### 4) Chiffres de revenus annoncés

*   « Devenir un AI Engineer, le nouveau rôle qui se paie **200k$+** » (*affirmé par l'auteur* à 06:51).
