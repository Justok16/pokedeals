# LUMAIL GROSSIT TROP VITE : les comptes de phishing arrivent (je fixe ça) | Scale $10k #4

Vidéo : https://youtu.be/XVdG2T837mo · durée 23:33 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes consignes :

---

### 1) Idée principale
La vidéo présente un retour d’expérience sur la gestion d’une plateforme d’emailing (appelée **Lumail**) propulsée et gérée en partie grâce à l’IA (notamment **Claude Code**). L’auteur détaille les défis rencontrés (comptes de phishing, blocages de spam, gestion du débit d’envoi) et les solutions mises en place pour automatiser et sécuriser l’infrastructure, tout en maintenant une croissance de son activité.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Lumail** *(nom exact : Lumail.io)*
    *   **Tarif :** Non précisé (mentionne un plan payant et un plan Creator à 20 $ par mois pour certaines organisations).
    *   **Utilité :** Plateforme d’emailing/marketing automatisée permettant d’envoyer des campagnes, de gérer des listes et de s’intégrer avec des outils d’IA.

*   **Claude Code** *(mentionné via l’intégration Codex / MCP)*
    *   **Tarif :** Non précisé.
    *   **Utilité :** Agent IA utilisé pour automatiser des tâches de code, le setup et l’intégration de l’onboarding de la plateforme.

*   **Prickly Mails** *(nom exact : PricklyMails.com)*
    *   **Tarif :** Non précisé (offre une formule gratuite avec un quota, puis payante).
    *   **Utilité :** API de vérification d’e-mails en temps réel (syntaxe, lookup MX, SMTP, détection des adresses jetables, pièges à spam, etc.) pour nettoyer les listes d’abonnés et éviter les rebonds.

*   **Spamhaus**
    *   **Tarif :** Service externe (non précisé).
    *   **Utilité :** Base de données/fournisseur de listes de spam qui répertorie les IP et domaines considérés comme spammeurs.

*   **Gemini** *(mentionné comme outil d’IA externe)*
    *   **Tarif :** Non précisé.
    *   **Utilité :** Utilisé pour analyser des échantillons d’e-mails et détecter s’ils s’apparentent à du phishing.

---

### 3) Astuces concrètes et réutilisables

*   **Limiter l’automatisation du contrôle selon le volume :** Ne pas faire de vérification agressive pour les petits volumes (par exemple, aucun check automatique sous 500 e-mails) afin d’éviter de bloquer injustement de nouveaux utilisateurs légitimes.
*   **Utiliser un système de « Minimum e-mails » et de seuils de rebond :** Fixer des règles strictes (taux de rebond < 5 %, plaintes < 0,1 %) et basculer automatiquement les comptes en révision humaine (`HUMAN_REVIEW`) si les seuils sont dépassés.
*   **Dissocier le domaine d’envoi du domaine de clic :** Utiliser des sous-domaines dédiés pour le tracking des liens (ex. `click.lumail.app` ou `lumail.codeleine.app`) afin de préserver la réputation de l’expéditeur principal (sender).
*   **Gérer le stockage des e-mails en amont (Base de données puis R2) :** Pour gérer des débits élevés sans perte de données, stocker les e-mails en base (PostgreSQL) avant l’envoi, puis purger via un système de priorité par organisation (les abonnements payants ayant la priorité).
*   **Intégrer une API de vérification d’e-mail à l’onboarding :** Valider automatiquement la listes d’abonnés à l’import via une API externe pour empêcher l’import d’adresses non délivrables ou de pièges à spam.

---

### 4) Chiffres de revenus annoncés

*   **Abonnement Creator :** 20 $ par mois *(affirmé par l’auteur)*.
*   **Volume d’e-mails envoyés :** ~4 517 490 e-mails sur une période récente *(affirmé par l’auteur)*.
*   **Taux d’ouverture global (avec bots) :** ~43 % *(affirmé par l’auteur)*.
*   **Débit d’envoi testé :** 20 e-mails par seconde *(affirmé par l’auteur)*.
