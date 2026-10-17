# SKILLATON à San Francisco : va-t-on réussir à gagner 1 000 $ à San Francisco (c'est galère...)

Vidéo : https://youtu.be/nwNvBz2-qFc · durée 24:21 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé détaillé de la vidéo, structuré spécialement pour une personne cherchant à générer des revenus légalement avec l'IA et le développement assisté.

---

### 1. Idée principale
La vidéo retrace le quotidien à San Francisco de Melvyn, développeur et créateur de contenu. Il illustre comment il monétise ses compétences en IA à travers deux leviers principaux :
1. **La vente de formations en ligne** destinées aux développeurs et non-développeurs souhaitant utiliser l'IA.
2. **La création rapide d'applications et de produits IA** (notamment lors de hackathons/skillathons) en s'appuyant sur des agents autonomes (*OpenClaude*, *Claude Code*) pilotés parfois simplement par des notes vocales sans ouvrir d'environnement de développement (IDE).

---

### 2. Outils, sites et dépôts GitHub cités

| Nom exact | Gratuit / Payant | Utilité / Usage dans la vidéo |
| :--- | :--- | :--- |
| **Claude Code** (Anthropic) | Payant (via API / abonnement) | Génération automatique de code et création de supports de présentation de diapositives. |
| **OpenClaude** | Gratuit / Open Source (*accès API requis*) | Framework d'agent IA autonome utilisé par l'auteur pour coder, générer des landing pages, régler des bugs et tout déployer via des commandes/vocaux Telegram/Discord sans ouvrir d'IDE. |
| **Cursor** | Freemium / Payant | Éditeur de code assisté par IA, utilisé dans le projet pour générer du référencement (SEO). |
| **Vercel** (`vercel.com`) | Freemium / Payant | Plateforme d'hébergement et de déploiement continu pour les applications web et landing pages. |
| **Cloudflare** | Freemium | Bouclier de sécurité anti-DDoS placé devant Vercel pour bloquer le trafic malveillant et éviter la surfacturation. |
| **API to CLI** (`api-cli`) | Projet du Hackathon (*Non précisé*) | Marketplace/outil créé durant le Skillathon pour convertir n'importe quelle API en commande CLI compréhensible par un agent IA. |
| **Skill Link – Inter-Skill Evolving System** | Projet GitHub (*Non précisé*) | Projet gagnant du Skillathon (par *Troy Rocket*) permettant l'apprentissage continu et l'enrichissement dynamique des compétences (*skills*) des agents IA. |
| **YouTube** | Gratuit | Plateforme de publication de vlogs et vidéos de contenu pour bâtir une audience et promouvoir les formations. |
| **X (ex-Twitter)** | Gratuit | Canal marketing et réseau sur lequel un bot automatique a été connecté pour tweeter chaque nouveau CLI publié. |

---

### 3. Astuces concrètes et réutilisables

* **Développement 100 % délégué aux agents IA (No-IDE workflow) :** 
  En configurant des agents autonomes (*OpenClaude*) connectés à une messagerie (Telegram/Discord), il est possible de leur dicter des consignes par message vocal. L'agent écrit le code, corrige les erreurs, crée les commits et déploie directement sur Vercel.
* **Sécurisation des coûts d'infrastructure Serverless :**
  Lorsqu'on déploie sur des hébergeurs facturant à la consommation (comme Vercel), il est impératif d'installer un pare-feu anti-DDoS comme **Cloudflare** afin d'éviter qu'une attaque ou une boucle infinie n'engendre des centaines de dollars de frais imprévus.
* **Format de lancement de formation à forte conversion :**
  Pour vendre un produit numérique à fort panier (ex: 700 €), la séquence éprouvée par l'auteur est : 
  1. Landing page dédiée ;
  2. Campagne d'emails de rappel ;
  3. Live interactif d'environ 2 heures ;
  4. Envoi de l'email d'ouverture des ventes immédiatement après le live.
* **Modularité des « Agent Skills » :**
  Plutôt que d'alourdir inutilement le prompt principal d'un agent IA, il est plus efficace d'isoler des compétences métier sous forme de « skills » autonomes (workflows de documentation, d'API, etc.) que l'agent appelle uniquement lorsqu'il détecte qu'il en a besoin.

---

### 4. Chiffres de revenus et coûts annoncés *(affirmé par l'auteur)*

* **Formation « AI Builder » (pour non-développeurs) :**
  * Prix de vente : **700 €** par élève (*affirmé par l'auteur* [16:28]).
  * Ventes réalisées : **7 personnes inscrites** en 10 minutes à la fin du live, soit **4 900 €** générés immédiatement (*affirmé par l'auteur* [16:32]).
* **Incidents / Coûts d'infrastructure & IA :**
  * Facture de surconsommation / attaque subie sur Vercel : **574,80 $** (*affirmé par l'auteur* [01:40]).
  * Consommation estimée de tokens IA lors du Skillathon : plus de **1 000 $** (*affirmé par l'auteur* [15:45]).
  * Coût estimé de location d'un bureau fermé à San Francisco : **4 000 $ à 5 000 $ / mois** (*affirmé par l'auteur* [00:25]).
  * Repas / Petit-déjeuner café français à San Francisco : **38 $** (~32 €) (*affirmé par l'auteur* [05:39]).
