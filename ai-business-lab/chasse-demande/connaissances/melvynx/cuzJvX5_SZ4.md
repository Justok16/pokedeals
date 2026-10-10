# Hermes Agent : 10 VRAIS usages quotidiens que je fais avec mon Agent IA

Vidéo : https://youtu.be/cuzJvX5_SZ4 · durée 16:33 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, répondant à vos critères :

---

### 1) Idée principale
La vidéo présente **Hermes / OpenClaw**, un agent IA autonome connecté à Telegram, qui fonctionne comme un « assistant ou agent informatique personnel » (AI Agent). Grâce à un accès complet à l'ordinateur, au terminal et à divers outils (Stripe, FrontApp, CodeLynx, Google Flights, etc.), il peut automatiser des tâches complexes du quotidien et professionnelles : gestion des e-mails, intégration d'outils, organisation de voyages, création de contenu (LinkedIn, YouTube), gestion du SAV, et analyse de données/business intelligence. L'auteur met en avant son autonomie, sa capacité à créer ses propres scripts/skills, et l'efficacité de son utilisation avec Claude Code.

---

### 2) Liste des outils, sites et dépôts GitHub cités
*   **OpenClaw / Hermes** (Agent IA / Computer Agent) :
    *   *Nom exact :* OpenClaw / Hermes (ou Hermes Agent).
    *   *Gratuit / Payant :* Non précisé (nécessite des coûts d'API selon les modèles utilisés).
    *   *Rôle :* Agent IA autonome et connectable à Telegram pour exécuter des tâches informatiques et administratives complexes.
*   **Telegram** :
    *   *Nom exact :* Telegram.
    *   *Gratuit / Payant :* Gratuit.
    *   *Rôle :* Interface de chat pour communiquer avec l'agent Hermes.
*   **Himalaya** (outil de messagerie/CLI) :
    *   *Nom exact :* Himalaya.
    *   *Gratuit / Payant :* Gratuit (Open Source).
    *   *Rôle :* Utilisé pour gérer les e-mails via le terminal (recherche, envoi, etc.).
*   **CodeLynx** :
    *   *Nom exact :* codelynx.dev.
    *   *Gratuit / Payant :* Non précisé (site personnel de l'auteur / plateforme).
    *   *Rôle :* Site de formation et blog de l'auteur géré avec l'IA.
*   **Stripe CLI** :
    *   *Nom exact :* Stripe CLI.
    *   *Gratuit / Payant :* Gratuit (outil officiel Stripe).
    *   *Rôle :* Permet à l'agent d'accéder aux factures, abonnements et de gérer les remboursements.
*   **FrontApp** :
    *   *Nom exact :* FrontApp / Front.
    *   *Gratuit / Payant :* Payant (logiciel de support client).
    *   *Rôle :* Gestion des e-mails et du support client (envoi de réponses, factures, etc.).
*   **Google Flights** :
    *   *Nom exact :* Google Flights.
    *   *Gratuit / Payant :* Gratuit.
    *   *Rôle :* Recherche de vols et de voyages de manière automatisée via le navigateur.
*   **Typefully** :
    *   *Nom exact :* Typefully.
    *   *Gratuit / Payant :* Payant/Freemium (outil de création de contenu).
    *   *Rôle :* Utilisé pour générer et planifier des posts sur les réseaux sociaux.
*   **YouTube Transcript / API** :
    *   *Nom exact :* YouTube Content / `youtube-transcript-io-cli`.
    *   *Gratuit / Payant :* Gratuit.
    *   *Rôle :* Récupérer les transcriptions de vidéos YouTube pour générer du contenu dérivé.
*   **Convex** :
    *   *Nom exact :* Convex (Prod Convex).
    *   *Gratuit / Payant :* Freemium / Payant.
    *   *Rôle :* Base de données / backend pour stocker et interroger les messages et données.
*   **ChatGPT / Claude (Anthropic)** :
    *   *Nom exact :* ChatGPT / Claude (Claude Code).
    *   *Gratuit / Payant :* Payant (abonnements/API).
    *   *Rôle :* Modèles de langage utilisés pour le raisonnement et le code.

---

### 3) Astuces concrètes et réutilisables
*   **Délégation de tâches répétitives par chat :** Au lieu de faire des recherches de vols ou de rédiger des e-mails soi-même, envoyer la conversation complète ou le contexte à l'agent pour qu'il effectue les actions en arrière-plan (en *background process*).
*   **Création dynamique de « Skills » (compétences) :** Lorsqu'une tâche est réussie une première fois, l'agent peut créer un script/skill réutilisable (ex. workflow de facturation manuelle) pour pouvoir exécuter la même tâche instantanément à l'avenir.
*   **Automatisation de la gestion du SAV et des remboursements :** Donner à l'agent l'accès à la CLI Stripe et aux e-mails pour qu'il identifie les paiements non désirés, rédige les demandes d'annulation et de remboursement, et confirme l'envoi directement dans le fil de discussion.
*   **Extraction et repurposing de contenu :** Télécharger les transcripts de vidéos YouTube ou de threads, analyser les styles d'écriture et générer automatiquement des dizaines de posts LinkedIn ou d'idées de contenu adaptés à sa propre audience.
*   **Gestion des sponsors et partenariats :** Centraliser les propositions de sponsors reçues, demander à l'agent de négocier ou de donner les grilles tarifaires, puis recevoir un *Digest* quotidien pour valider ou rejeter les propositions en un clic.
*   **Consolidation de la mémoire (Dream Memory) :** Lancer des scripts réguliers (cron jobs) pour consolider les conversations et extraire les informations clés (préférences, historique médical, données clients) afin que l'agent dispose d'un contexte persistant et précis à tout moment.

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)
*   *Montant de la facture annulée/remboursée (Frontier Tower) :* **190 $**
*   *Nombre de lignes de messages dans la base de données (Convex prod) :* **43 795** (dont 3 198 visiteurs, 2 809 agents, 3 195 IA, 34 593 système).
*   *Consommation de tokens (données du dashboard Hermes) :* **767,6 millions de tokens** au total pour **1 421 sessions** et **39 550 appels API**.
*   *Coût estimé affiché sur le dashboard Hermes :* **12 526,56 $** (l'auteur précise qu'il pense que c'est « un peu bullshit » ou surévalué).
