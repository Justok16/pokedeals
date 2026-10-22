# J'arrête Vercel : je migre pour un nouvelle outil qui me coûte 2x moins chère

Vidéo : https://youtu.be/jUMDZyN7qTo · durée 16:00 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo, spécialement rédigé pour une démarche d'optimisation financière et technique avec l'IA et Claude Code.

---

### 1) Idée principale
L'auteur explique comment il a réduit drastiquement ses coûts d'infrastructure SaaS en quittant la tarification à l'usage de Vercel pour migrer l'ensemble de ses applications et services annexes (analytics, monitoring, backups) sur un serveur VPS dédié Hetzner géré par Dokploy. L'élément clé est que **l'intégralité de la migration, de la configuration du serveur et du débogage a été réalisée de manière autonome par un agent IA (Claude Code / Codex) connecté en SSH au VPS**.

---

### 2) Outils, sites et dépôts cités

*   **Vercel** *(Payant / Freemium)* : Plateforme PaaS Serverless. Idéale pour démarrer, mais devient très chère dès que le trafic ou les calculs augmentent (coûts au Mo/To et à la consommation CPU/Mémoire).
*   **Hetzner** *(Payant - abonnement fixe bas)* : Hébergeur de serveurs VPS/Cloud offrant un rapport performance/prix très avantageux et incluant un volume massif de bande passante (20 To).
*   **Just fucking use Hetzner** (`justfuckingusehetzner.com`) *(Gratuit - site comparatif)* : Site informatif mettant en évidence les écarts de coûts de bande passante entre les gros hébergeurs Cloud (AWS, Vercel) et Hetzner.
*   **Codex / Claude Code** *(Payant - via API/Abonnement)* : Agent et interface IA utilisé par l'auteur. Connecté en SSH directement au VPS, il exécute les commandes terminal et gère l'infrastructure via le chat.
*   **Dokploy** *(Gratuit & Open-source)* : Alternative PaaS auto-hébergée à Vercel. Il s'installe sur le VPS et permet de déployer des applications (Docker, Git) avec une interface proche de celle de Vercel.
*   **Cloudflare (et Cloudflare R2)** *(Gratuit / Payant très bon marché)* : Utilisé pour la gestion des clés API DNS et le stockage des sauvegardes automatisées (S3) des bases de données.
*   **Uptime Kuma** *(Gratuit & Open-source)* : Outil de monitoring d'indisponibilité ("uptime") auto-hébergé sur le VPS pour tester la disponibilité des sites et API en continu.
*   **Umami Analytics** *(Gratuit & Open-source)* : Alternative auto-hébergée à Plausible ou Google Analytics pour suivre le trafic, les événements, UTM et conversions sans payer d'abonnement SaaS tiers.
*   **Telegram (Bot Telegram)** *(Gratuit)* : Utilisé pour recevoir des notifications automatiques en temps réel après chaque déploiement (succès ou erreurs).
*   **Coolify** *(Gratuit & Open-source)* : Autre alternative PaaS à Vercel. L'auteur l'a testée mais a préféré Dokploy pour son ergonomie plus proche de Vercel.
*   **Templates Dokploy (Ackee, Cap.so, Convex, Excalidraw, etc.)** *(Gratuit / Open-source)* : Catalogue d'outils open-source déployables en un clic sur Dokploy.

---

### 3) Astuces concrètes et réutilisables

1.  **Pilotage de serveur VPS à 100 % via l'Agent IA (SSH) :**
    *   Au lieu de configurer le serveur à la main (Linux/Docker), ajoutez les identifiants SSH de votre VPS dans votre agent IA (Codex / Claude Code).
    *   Donnez-lui accès à vos clés API (Cloudflare, GitHub CLI) et laissez-le installer le PaaS (Dokploy), builder les conteneurs et configurer les noms de domaine de façon autonome.
2.  **Stratégie d'hébergement hybride Vercel / VPS (Rentabilité maximale) :**
    *   Conservez les **déploiements de preview (branches de test)** sur Vercel pour profiter de la gratuité du forfait de base.
    *   Basculez les **déploiements de production (fort trafic)** sur Dokploy / Hetzner pour payer un montant fixe, peu importe le nombre de visiteurs.
3.  **Auto-hébergement du "Stack de gestion" (Analytics & Monitoring) :**
    *   Ne payez plus pour des SaaS tiers de statistiques ou d'uptime. Installez **Umami** et **Uptime Kuma** directement sur votre VPS via Dokploy. L'agent IA peut lier automatiquement chaque nouveau SaaS déployé à votre instance Analytics et à votre instance Uptime Kuma.
4.  **Audit de serveur et sécurité par l'IA :**
    *   Programmez un prompt / agent IA pour auditer régulièrement l'état de votre VPS : vérification de la mémoire, analyse des logs d'erreurs, sécurité des accès et nettoyage des conteneurs inutilisés.
5.  **Sauvegardes quotidiennes externalisées :**
    *   Configurez Dokploy pour envoyer automatiquement des backups quotidiens des bases de données vers un stockage S3 économique (ex: Cloudflare R2).

---

### 4) Chiffres de revenus et coûts annoncés

*   **Coûts Vercel passés de l'auteur :** **83 $ / mois** de facturation globale *(affirmé par l'auteur)*.
*   **Exemple de coût unitaire Vercel :** ~**18 $ / mois** pour un seul projet (`saveit.now`) *(affirmé par l'auteur)*.
*   **Coût de la bande passante supplémentaire Vercel :** **150 $ / To** *(affirmé par l'auteur / vu à l'écran)*.
*   **Coût du serveur VPS Hetzner retenu :** Environ **41 € / mois** (~41 $) pour 8 Go de RAM, 160 Go de SSD et 20 To de bande passante incluse *(affirmé par l'auteur)*.
*   **Revenus générés par ses projets SaaS :** **Non précisé** *(la vidéo se concentre uniquement sur la réduction des dépenses d'infrastructure)*.
