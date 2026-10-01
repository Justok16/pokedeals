# Ship ton SaaS AUJOURD'HUI : voici la méthode ULTIME

Vidéo : https://youtu.be/uFV7lVf7r60 · durée 55:40 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo avec toutes les informations demandées :

### 1) Idée principale
La vidéo montre comment créer et publier un SaaS complet (dans cet exemple, un réducteur d'URL et un gestionnaire de liens nommé *LinkQuick*) en une seule fois (« in one shot ») grâce à une méthode de développement pilotée par l'IA et structurée autour d'un dépôt GitHub et de compétences (skills) automatisées.

---

### 2) Outils, sites et dépôts GitHub cités

* **NowStack-SaaS** (Dépôt GitHub : `Melvynx/nowstack-saas`)
  * **Prix :** Non précisé
  * **À quoi il sert :** Dépôt de démarrage (boilerplate) utilisé comme base pour créer tous les SaaS du créateur.
* **NowStack** (`mlv.sh/formation-nowstack` / `mlv.sh/join-nowstack`)
  * **Prix :** Payant (mention de 49 $/mois ou plan Pro/Ultra, et mini-formation payante) — *affirmé par l'auteur*.
  * **À quoi il sert :** Plateforme de formation, communauté, et accès aux outils/skills pour lancer un SaaS en une semaine.
* **Codex** (Outil d'IA / interface de développement)
  * **Prix :** Non précisé
  * **À quoi il sert :** Assistant de code propulsé par l'IA pour créer, planifier (fichiers `.md`), exécuter et automatiser la création du projet.
* **GitHub**
  * **Prix :** Gratuit / Payant (selon l'offre)
  * **À quoi il sert :** Hébergement de code, gestion de versions et clonage des dépôts.
* **Lumail** (`Lumail.ai`)
  * **Prix :** Non précisé
  * **À quoi il sert :** Outil d'e-mail marketing pour les créateurs et fondateurs de SaaS.
* **Subfast**
  * **Prix :** Non précisé
  * **À quoi il sert :** Mentionné comme exemple de SaaS / landing page existante.
* **Savevits**
  * **Prix :** Non précisé
  * **À quoi il sert :** Mentionné dans la pile marketing/e-mail.
* **Glow**
  * **Prix :** Non précisé
  * **À quoi il sert :** Mentionné dans la pile marketing/e-mail.
* **Vercel**
  * **Prix :** Gratuit / Payant (Vercel Pro mentionné)
  * **À quoi il sert :** Hébergement et déploiement d'applications web, gestion des domaines et des certificats SSL.
* **Dub** (`dub.co`)
  * **Prix :** Gratuit / Payant (forfaits Free à 30 $, Pro à 30 $/mois, Business à 90 $/mois) — *affirmé par l'auteur*.
  * **À quoi il sert :** Plateforme de liens de redirection et de tracking (mentionné comme alternative ou benchmark pour l'outil LinkQuick).
* **Short.io**
  * **Prix :** Non précisé
  * **À quoi il sert :** Raccourcisseur d'URL et outil de tracking de liens.
* **Bitly**
  * **Prix :** Core 10 $, Growth 29 $, Premium 199 $ — *affirmé par l'auteur*.
  * **À quoi il sert :** Raccourcisseur d'URL et gestion de liens.
* **Rebrandly**
  * **Prix :** Non précisé
  * **À quoi il sert :** Gestion de liens personnalisés.
* **Convex** (`Convex Cloud` / `Convex Professional`)
  * **Prix :** Gratuit / Payant (Convex Professional) — *affirmé par l'auteur*.
  * **À quoi il sert :** Base de données et backend temps réel pour l'application.
* **Cloudflare**
  * **Prix :** Gratuit / Payant
  * **À quoi il sert :** Gestion des DNS, proxy et sécurité pour les noms de domaine.
* **Google Sheets**
  * **Prix :** Gratuit
  * **À quoi il sert :** Tableur mentionné comme méthode traditionnelle (non utilisée ici).
* **Notion**
  * **Prix :** Gratuit / Payant
  * **À quoi il sert :** Outil de documentation et de prise de notes mentionné.
* **shadcn/ui** (`ui.shadcn.com`)
  * **Prix :** Gratuit
  * **À quoi il sert :** Bibliothèque de composants UI et de thèmes pour React.
* **Resend**
  * **Prix :** Non précisé
  * **À quoi il sert :** API pour l'envoi d'e-mails transactionnels (authentification OTP).
* **PostHog**
  * **Prix :** Non précisé
  * **À quoi il sert :** Outil d'analyse et de product product (mentionné comme optionnel dans le CLI).

---

### 3) Astuces concrètes et réutilisables

* **Utiliser un starter / boilerplate :** Cloner un dépôt de départ (comme `nowstack-saas`) permet d'économiser un temps précieux car l'authentification, les abonnements Stripe et la base de données sont déjà pré-configurés.
* **La phase de cadrage par l'IA :** Avant de coder, utiliser l'IA avec un workflow de planification (création de fichiers `discovery.md`, `idea.md`, `archi.md` et `prd.md`) permet de définir clairement les fonctionnalités, d'identifier les coûts et d'éviter des dizaines d'heures de corrections ultérieures.
* **Réutiliser les clés API :** Pour gagner du temps et éviter de divulguer de nouvelles clés, demander à l'IA de récupérer et d'injecter directement les clés API d'un précédent projet fonctionnel (comme Resend ou Convex).
* **Automatiser la configuration des outils (Toolchain) :** Utiliser des commandes automatisées (`$setup-project`, `$setup-stripe`, `$ship-deploy`) pour vérifier que tous les services (GitHub, Vercel, Convex, Resend) sont correctement installés et configurés.
* **Déléguer les tests et le debug à l'IA :** En cas d'erreur de production (comme un statut `draft` ou une erreur de redirection), utiliser des skills de runtime et de logs (ex. `runtime-incident` ou `convex-monitor`) pour laisser l'IA identifier et corriger le problème en autonomie.

---

### 4) Chiffres de revenus annoncés
* **Non précisé** (la vidéo se concentre uniquement sur la création technique d'un SaaS et mentionne des tarifs d'outils tiers, mais aucun chiffre de chiffre d'affaires ou de revenus réalisés par l'auteur n'est annoncé).
