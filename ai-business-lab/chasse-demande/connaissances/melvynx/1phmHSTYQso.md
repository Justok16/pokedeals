# Annule TOUS tes abonnements et remplace-les par des Personal SaaS - Formation gratuite 2026

Vidéo : https://youtu.be/1phmHSTYQso · durée 38:34 · résumé Gemini (gemini-3-flash-preview) du 2026-10-22
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour exploiter Claude Code dans la création de business en ligne :

### 1) L’idée principale
L'idée est de passer de "consommateur de SaaS" à "créateur de SaaS". Au lieu de payer des abonnements mensuels à des plateformes tierces, l'utilisateur utilise **Claude Code** (l'agent d'IA d'Anthropic) pour générer, configurer et déployer ses propres applications sur mesure (ex: une plateforme de formation avec espace membre et paiement). L'IA gère non seulement le code, mais aussi l'infrastructure (serveurs, base de données, DNS).

### 2) Outils, sites et ressources cités
*   **GitHub** (Gratuit) : Sert à sauvegarder le code généré par l'IA et à gérer le versionnage (historique des modifications).
*   **Cloudflare** (Gratuit) : Utilisé pour héberger le site et gérer le nom de domaine (DNS, SSL).
*   **Convex** (Gratuit/Freemium) : Base de données en temps réel pour stocker les données utilisateurs, les leçons et les modules.
*   **Tella.tv** (Payant) : Outil d'enregistrement et d'hébergement vidéo pour le contenu des formations.
*   **Lumail.io** (Gratuit jusqu'à 3000 emails/mois) : Service d'email marketing et d'envoi de codes de connexion (OTP).
*   **Stripe** (Frais par transaction) : Intégré pour encaisser les paiements des clients.
*   **Claude Desktop / Claude Code** (Payant/Crédits) : L'agent d'IA qui exécute les commandes et construit l'application.
*   **Stack technique mentionnée** (Gratuit) : *Tanstack Start* (framework), *Shadcn/UI* (composants design), *Tailwind CSS* (style) et *BetterAuth* (authentification).

### 3) Astuces concrètes et réutilisables
*   **Automatisation des permissions :** Dans les réglages de Claude Code, activer le mode **"Allow bypass permissions"**. Cela permet à l'IA d'exécuter des suites de commandes sans demander une validation manuelle à chaque étape.
*   **Le "Prompt de délégation" :** Ne pas essayer de configurer les clés API ou les DNS manuellement. Copiez les instructions de services tiers (comme Lumail) et dites à Claude : *"Installe et connecte cet outil à mon compte, fais-le toi-même et termine ce job"*.
*   **Debug par l'image :** Si une erreur apparaît sur le site, faites une capture d'écran et donnez-la à Claude avec l'URL. Il analysera l'erreur visuelle et le code simultanément pour corriger le bug.
*   **Commande `/fork` :** Si vous avez un doute sur une modification, utilisez `/fork` pour créer une branche de travail parallèle sans casser la version qui fonctionne déjà.
*   **Zéro configuration DNS :** En connectant Claude à l'API Cloudflare, l'IA peut modifier elle-même les enregistrements (CNAME, TXT, MX) nécessaires au fonctionnement des emails et du domaine.

### 4) Chiffres de revenus et économies
*   **Économies SaaS :** Remplacer des abonnements comme *Podia* (49 $/mois) ou *Système.io* (17 €/mois).
*   **Revenus de développeur :** L'auteur affirme avoir été payé **10 000 €, 28 717 € puis jusqu'à 30 000 € par mois** lorsqu'il travaillait comme développeur classique avant l'ère de l'IA (affirmé par l'auteur).
*   **Coût fixe :** L'exemple montre l'achat d'un nom de domaine spécifique pour **21,20 $/an**.
*   **Vitesse :** Déploiement d'une plateforme complète fonctionnelle en **25 minutes** environ.
