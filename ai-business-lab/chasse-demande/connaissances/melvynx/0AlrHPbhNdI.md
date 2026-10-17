# Mon SaaS IMPOSSIBLE à vibe-coder : ce que personne ne vous dit sur le vibe-coding

Vidéo : https://youtu.be/0AlrHPbhNdI · durée 23:19 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur présente l'architecture technique et les fonctionnalités de **Lumail**, un SaaS d'email marketing complexe qu'il a développé à l'aide d'outils d'IA (Cursor, Claude Code). Il démontre que si l'IA permet de coder rapidement, elle ne sait pas concevoir seule une architecture distribuée robuste (gestion des fortes charges, files d'attente, webhooks massifs, rate limits). Il montre également comment connecter un SaaS à des agents IA via un SDK, des outils (Tools/MCP) et un CLI (Skills).

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité / Rôle |
| :--- | :--- | :--- |
| **Lumail** (`lumail.io`) | Payant (plans visibles de 0 $ à 200 $/mois, accès sur sélection/appel) | SaaS d'email marketing développé par l'auteur (gestion de campagnes, snippets, analytics, workflows, délivrabilité). |
| **Next.js** | Gratuit (Open-source) | Framework React utilisé pour développer l'application frontend/backend. |
| **AWS SES (Simple Email Service)** | Payant à l'usage | Service Amazon utilisé pour acheminer les emails et renvoyer les statuts de délivrabilité. |
| **Upstash QStash** | Freemium / Payant selon usage | Système de file de messages servant de régulateur (*load balancer*) pour respecter la limite d'envoi d'emails (ex. 50 emails/seconde vers AWS). |
| **Upstash Redis Queue** | Freemium / Payant selon usage | File d'attente Redis pour absorber les webhooks massifs (clics, ouvertures, bounces) et les traiter par lots (*batching*). |
| **Cloudflare R2** | Payant / Freemium | Stockage objet servant à stocker le code HTML lourd des emails avec expiration (30 jours) pour soulager la base de données. |
| **Gemini (Google)** | Freemium / Payant (API) | Modèle IA intégré dans l'éditeur de Lumail pour la correction grammaticale automatique (*Fix grammar*). |
| **Vercel** | Freemium / Payant | Hébergement et gestion automatisée des domaines et DNS. |
| **Claude Code** (Anthropic) | Payant (via API / souscription Anthropic) | Outil CLI d'Anthropic pour générer du code, orchestrer des workflows et exécuter des compétences (*Skills*). |
| **Cursor** | Freemium / Payant | Éditeur de code assisté par IA utilisé aux débuts du projet. |
| **OpenClaw** | Non précisé | Agent IA personnalisé connecté à Telegram pour piloter Lumail en langage naturel via CLI. |
| **Ghostty** | Gratuit (Open-source) | Émulateur de terminal utilisé lors de la démonstration du CLI. |
| **Thumbfa.st** | Freemium / Payant | SaaS de création de miniatures YouTube (utilisé comme compte de démonstration). |
| **Formation Claude Code** (`mlv.sh/fa` / `codelynx.dev`) | Gratuit (*affirmé par l'auteur*) | Formation et configuration pour apprendre à utiliser Claude Code et les agents IA. |

---

### 3) Astuces concrètes et réutilisables

* **Lisser les envois pour respecter les quotas API :** Ne pas bombarder les API d'envoi (comme AWS SES) avec des milliers de requêtes instantanées. Intercaler une file comme *Upstash QStash* pour cadencer les appels (ex. par lots de 50/sec).
* **Traiter les webhooks à fort volume par lot (*Batching*) :** Pour éviter d'ouvrir des centaines de connexions par seconde sur la base de données lors de la réception d'événements (clics, ouvertures), stocker les événements dans une file Redis (*Upstash Redis*), puis exécuter des requêtes groupées (ex. 1 requête SQL pour 1 000 événements par worker).
* **Délester le contenu lourd vers un stockage objet :** Stocker le code HTML volumineux des emails dans un stockage de type Cloudflare R2 avec une politique de rétention (ex. suppression après 30 jours) plutôt que d'alourdir la base de données principale.
* **Créer des outils (Tools / Skills) pour agents IA :** Exposer les fonctionnalités de son SaaS sous forme de commandes CLI (avec sortie JSON) ou de SDK TypeScript pour permettre à des agents (Claude Code, bots Telegram) de gérer les opérations (création de campagne, recherche d'abonnés, analytics) en autonomie.
* **Superviser l'architecture face à l'IA :** Les modèles de langage optimisent pour le besoin immédiat et n'anticipent pas les problèmes de montée en charge (scalabilité). La conception des flux de données et la tolérance aux pannes doivent être validées par le développeur.

---

### 4) Chiffres de revenus annoncés

* **Revenu récurrent mensuel (MRR) affiché :** **0,00 $** (*affirmé par l'auteur / visible sur le tableau de bord d'administration Lumail*).
* **Statistiques d'utilisation annoncées :** Sur son organisation principale (*Codelynx, LLC*), l'auteur indique **2 810 854 emails envoyés**, **477 campagnes** et **55 583 abonnés** (*affirmé par l'auteur*).
