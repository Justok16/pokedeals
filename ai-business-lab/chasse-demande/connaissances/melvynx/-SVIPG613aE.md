# Arrête d'utiliser Codex sans ça : 3 600 outils en 1 commande

Vidéo : https://youtu.be/-SVIPG613aE · durée 21:17 · résumé Gemini (gemini-3.8-flash) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
Un agent IA (comme Claude Code, Hermes ou Codex) est limité et perd l'essentiel de sa valeur s'il n'est pas connecté à des outils et services externes (SEO, réseaux sociaux, plateformes publicitaires, scraping, enrichissement de données). Pour éviter de payer des dizaines d'abonnements séparés et de perdre des heures à configurer manuellement des intégrations ou des serveurs MCP, l'auteur présente **Treg** (`treg.to`). Conçu comme un « OpenRouter pour les outils d'agents », ce service centralise plus de 3 600 outils et 90 fournisseurs derrière une seule clé API/MCP, avec une tarification à l'usage réel (0 % de marge ajoutée) ou gratuitement en connectant ses propres comptes OAuth.

---

### 2) Outils, sites et dépôts cités

* **Treg (`treg.to`)** :
  * *Statut* : Freemium / Paiement à l'usage (crédits offerts au démarrage ; gratuit si vous connectez vos propres comptes OAuth ; sinon facturation au coût réel du fournisseur sans marge).
  * *Rôle* : Hub / routeur unifié d'outils et d'API pour agents IA (SEO, pubs, réseaux sociaux, B2B lead gen, enrichissement).
* **Claude Code** :
  * *Statut* : Payant (via crédits API Anthropic).
  * *Rôle* : Agent IA en ligne de commande capable d'exécuter des scripts, coder et appeler des compétences/outils.
* **Codex** :
  * *Statut* : Modèle commercial non précisé (utilise des LLM payants à l'usage).
  * *Rôle* : Environnement de travail / interface d'agent IA utilisé par l'auteur pour piloter ses projets.
* **Hermes Agent / SteveClaw (sur Discord)** :
  * *Statut* : Non précisé (agent IA propriétaire/personnalisé).
  * *Rôle* : Agent IA intégré à un serveur Discord pour exécuter des tâches d'automatisation et des audits.
* **Autres agents mentionnés sur Treg** (*OpenClaw, Grok Bot, Claude.ai, opencode, pi, Cursor, Gemini CLI*) :
  * *Statut* : Dépend de chaque outil (gratuits, freemium ou payants).
  * *Rôle* : Agents compatibles avec l'intégration Treg en une commande.
* **Meta Ads (Facebook & Instagram Ads)** :
  * *Statut* : Gratuit pour l'accès aux API via connexion de son propre compte OAuth (les dépenses publicitaires restent payantes).
  * *Rôle* : Création, modification, consultation et gestion de campagnes/publicités.
* **Google Ads / Google Search Console / Google Analytics** :
  * *Statut* : Gratuit via connexion OAuth de son compte Google.
  * *Rôle* : Suivi SEO, mots-clés, indexation et gestion des annonces Google.
* **YouTube Data API** :
  * *Statut* : Gratuit si connecté avec son propre compte (via OAuth).
  * *Rôle* : Récupération des commentaires, des vidéos et des statistiques de chaîne.
* **ScrapeCreators / TikHub** :
  * *Statut* : Payant à l'appel via Treg (ex. fractions de centime : ~0,00188 $ par appel pour ScrapeCreators, ~0,0008 $ pour TikHub).
  * *Rôle* : Extraction de transcripts de vidéos YouTube, données TikTok, etc.
* **Outils SEO intégrés** (*DataForSEO, Serpstat, SE Ranking, Moz, Semrush, Majestic, Ahrefs*) :
  * *Statut* : Payant à la requête via le solde Treg, ou gratuit si vous renseignez votre propre clé d'abonnement.
  * *Rôle* : Analyse des mots-clés, volume de recherche, backlinks, audits techniques et visibilité IA.
* **Outils d'enrichissement B2B / Cold Email** (*Bright Data, Hunter, Apollo, Lusha, People Data Labs, QuickEnrich, Tomba, TryKit, LeadMagic, Dropcontact/Dropleads*) :
  * *Statut* : Payant par résultat trouvé / par requête via le solde Treg.
  * *Rôle* : Scraping de données d'entreprises, recherche d'adresses e-mail professionnelles et vérification SMTP.
* **GitHub** :
  * *Statut* : Gratuit / Freemium.
  * *Rôle* : Création et gestion automatique d'issues/tickets suite aux audits réalisés par les agents (dépôt privé `Lumail.io` montré en exemple).
* **Lumail.io & TrendTrack.io** :
  * *Statut* : Services tiers / SaaS.
  * *Rôle* : Cas concrets utilisés pour les démos (audit SEO complet pour Lumail, identification du CEO Vincent Alonzo et de son e-mail pour TrendTrack).

---

### 3) Astuces concrètes et réutilisables

1. **Configuration instantanée de l'agent** : Plutôt que d'écrire des fichiers de configuration manuellement, copiez la commande fournie par Treg (ex. `set up treg - https://treg.to/llms.txt <VOTRE_CLE_API>`) et collez-la directement dans le chat de votre agent (Claude Code, Codex, etc.). L'agent lit le fichier markdown, installe la CLI/skill et configure ses droits automatiquement.
2. **Éviter les coûts inutiles avec OAuth ("Bring Your Own Key/Account")** : Connectez vos comptes Google Search Console, YouTube et Meta Ads directement dans Treg. Les requêtes passant par vos comptes propres ne vous coûtent rien sur votre solde Treg (affichées en statut `free`).
3. **Plafond budgétaire dans le prompt** : Lorsque vous demandez à l'agent d'utiliser des API payantes (recherche d'e-mails, SEO, scraping), imposez-lui une contrainte budgétaire dans le prompt (ex. *« utilise un budget maximal de 2 USD, vérifie le prix avant chaque appel et indique les coûts réels »*). Le skill Treg fournit les prix unitaires et l'agent sélectionnera automatiquement le fournisseur le moins cher.
4. **Gestion des campagnes publicitaires en langage naturel** : Vous pouvez demander à votre agent d'inspecter vos publicités actives sur Meta, de désactiver celles qui ne fonctionnent pas, d'ajuster le budget quotidien au niveau de l'ensemble de publicités et de générer 5 variantes de textes/titres inspirés de vos meilleures pubs sans ouvrir le gestionnaire de publicités.
5. **Audits automatisés convertis en tâches GitHub** : Combinez les compétences SEO de Treg avec l'accès GitHub de votre agent pour générer un audit complet (Lighthouse, mots-clés, cannibalisation) et créer automatiquement les tickets d'intervention (`issues`) prêts à être résolus.

---

### 4) Chiffres de revenus annoncés

* **Revenus de l'auteur** : non précisé.
* **Programme d'affiliation Treg** : L'auteur indique qu'il gagne **5 $** par parrainage lorsque l'utilisateur ajoute 10 $ sur la plateforme (*« affirmé par l'auteur »*).
* **Tarifs de produits affichés à l'écran lors des tests publicitaires** : Landing page affichant une offre à **199 €** ou **299 €**, et un budget test de **10 CHF / jour** (*« affirmé par l'auteur »* comme exemple de paramétrage de campagne, pas un revenu).
