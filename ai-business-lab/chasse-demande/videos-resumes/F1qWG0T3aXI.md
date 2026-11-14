# F1qWG0T3aXI — « 31 façons INCROYABLES d'utiliser Claude en 2027 »

- Auteur : Thomas Berton ; lien : https://youtu.be/F1qWG0T3aXI
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Liste de 31 usages de Claude Code, surtout hors du bureau (appareils de la maison, vieux matériel, réseau, jeux, recherche), avec la publicité du service payant de l'auteur et de son groupe en ligne.

- **Remplacer ses logiciels payants par des outils faits sur mesure avec Claude Code** : déjà notre façon de faire (devis, factures, kit client, contrôles et veille sont des outils maison dans `outils/`, sans abonnement) ; rien à résilier (budget 0 €). Laisser Claude fouiller une boîte mail personnelle pour lister des abonnements : écarté (jamais de connexion aux comptes personnels de l'utilisateur).
- **Résumer de longues vidéos ou podcasts en une méthode courte** : déjà en place (`outils/resumer_video.py`, base de connaissances vidéo, registre `46`). NotebookLM : déjà en réserve (`connaissances/reserve-prete.md` : outil que l'utilisateur peut employer lui-même).
- **Visite ou maquette 3D d'une maison dans le navigateur (Three.js)** : en réserve ; Three.js est déjà chez nous (skills `threejs-web`, `threejs-animation`). À ressortir seulement si un client du bâtiment (constructeur, menuisier, cuisiniste) demande une vue 3D sur son site, après le premier client payant. Le prix de 5 000 à 10 000 € par plan est affirmé par l'auteur, non vérifié, à ne jamais reprendre.
- **Petit jeu personnalisé offert à un client, ouvert par un QR code** : écarté pour l'instant ; aucune demande d'artisan (règle n° 1), nouvelles démos en pause.
- **Chercher des idées de produits qui n'existent pas encore dans un grand catalogue (exemple des jeux Steam)** : écarté ; DIG16 a déjà sa piste, et la priorité reste la preuve de la demande (`57`).
- **Audit de routeurs, d'appareils Android, déblocage de téléviseurs, liseuses ou véhicules, contrôle d'un téléphone contre les logiciels espions (outil MVT)** : écartés ; hors métier, et débloquer un appareil peut annuler sa garantie ou enfreindre ses conditions d'usage.
- **Domotique, vieux appareils recyclés, imprimante à tickets, simulateur de drone, recherche médicale** : écartés, hors sujet (rien qui concerne l'entreprise).
- **AIOS (service payant de l'auteur)** : écarté (publicité, budget 0 €). **Groupe Skool « Le Club IA » (annoncé gratuit, donne les 31 consignes)** : non retenu ; il faudrait un compte personnel de l'utilisateur, et rien dans la liste ne répond à un besoin de DIG16. Chaîne de Nick Saraev : simple source de l'auteur.
- **Chiffres cités (240 € par an économisés par logiciel résilié, 5 000 à 10 000 € par plan 3D, 186 transactions et 4 000 $ dans une expérience d'Anthropic, 30 000 $ de crédits offerts, matériel à 20 €, drone à 400 €)** : affirmés par l'auteur, non vérifiés.

Conclusion : rien à installer, rien à changer ; une seule idée gardée en réserve (vue 3D pour un client du bâtiment).

## Résumé (Gemini)

Voici le résumé structuré de la vidéo, spécialement orienté pour une personne souhaitant exploiter **Claude Code** et l'IA pour générer de la valeur ou créer des services rémunérateurs de manière légale.

---

### 1) Idée principale

La vidéo démontre que **Claude Code** (et les agents IA associés) ne doit pas être limité à de simples tâches rédactionnelles (comme reformuler des e-mails), mais utilisé comme un **ingénieur logiciel et matériel autonome**. Grâce à sa capacité d'interaction directe avec le code, les fichiers, le réseau et les appareils physiques (via Wi-Fi, USB, Bluetooth, API), Claude Code permet à une seule personne :
* De créer des applications sur-mesure ou du matériel personnalisé en quelques heures.
* De supprimer des coûts récurrents (remplacement de logiciels SaaS payants).
* De réparer, auditer ou débloquer des équipements existants (TV, routeur, liseuse, véhicule, climatisation).
* D'automatiser des processus complexes de recherche ou de développement (jeux vidéo, biotech, analyse de marché).

---

### 2) Outils, sites et dépôts GitHub cités

* **Claude Code / Claude (Anthropic)** *(Payant via abonnement à partir de 20 $/mois ou API ; version gratuite de base)* : Agent IA en ligne de commande capable d'exécuter des scripts, d'auditer du matériel/logiciel, de développer des applications complètes et de contrôler des outils externes.
* **Claude Opus / Sonnet / Haiku (Anthropic)** *(Payant / Inclus dans les offres Claude)* : Les différents modèles de LLM d'Anthropic (Opus étant le plus puissant pour la négociation/réflexion complexe).
* **AIOS (aios.fr)** *(Payant - Service/Logiciel)* : Solution développée par l'auteur (Thomas Berton) proposant un « employé IA » tournant sur serveur privé pour centraliser et remplacer les outils logiciels des entreprises.
* **Le Club IA (Skool - skool.com/le-club-ia)** *(Gratuit)* : Communauté en ligne créée par l'auteur pour partager gratuitement les 31 prompts cités dans la vidéo.
* **Chaîne YouTube de Nick Saraev** *(Gratuit)* : Source d'inspiration citée par l'auteur pour avoir regroupé une partie des cas d'usage de Claude.
* **Outil d'audit Amnesty International (Mobile Verification Toolkit / MVT)** *(Gratuit / Open-Source)* : Outil utilisé dans le prompt d'inspection de sécurité smartphone/hôtel contre les logiciels espions.
* **Three.js** *(Gratuit / Open-Source)* : Bibliothèque JavaScript 3D utilisée pour générer des visites interactives ou des simulations 3D dans le navigateur.
* **Google NotebookLM** *(Gratuit)* : Outil d'IA de Google recommandé par l'auteur pour résumer et synthétiser de grands volumes de documents ou de podcasts.
* **Imprimante thermique à tickets de caisse Bluetooth** *(Matériel - Payant, environ 20 €)* : Utilisée pour imprimer automatiquement un récapitulatif papier d'e-mails/news chaque matin.
* **Boîtier domotique générique** *(Matériel - Payant, environ 20 €)* : Utilisé pour centraliser les objets connectés d'une maison sous une seule interface IA.

---

### 3) Astuces concrètes et réutilisables (idées de business / valeur)

1. **Remplacement systématique de SaaS payants (*SaaS Killing*)** :
   * *Principe* : Connecter Claude Code à sa boîte mail pour lister tous les abonnements logiciels professionnels (CRM, agenda, relances, facturation), puis lui demander de recoder un par un des équivalents sur-mesure hébergés sur son propre serveur.
2. **Re-centralisation domotique et revalorisation d'ancien matériel** :
   * *Principe* : Récupérer de vieux appareils (iPad mini de 2012, Kindle, vieux smartphones) et demander à Claude Code de contourner le système d'origine via USB/Wi-Fi pour y installer un tableau de bord domotique unifié ou une application dédiée.
3. **Services d'audit et d'optimisation réseau / sécurité (prestations de service)** :
   * *Principe* : Proposer à des clients d'auditer leurs routeurs Wi-Fi ou leurs équipements Android (ex. autoradios de voiture ou boîtiers TV) avec Claude Code pour détecter les malwares (ex. mineurs de cryptomonnaie cachés), débloquer les bridages et multiplier le débit internet sans changer de matériel.
4. **Mine d'idées de produits par analyse d'espace vectoriel (*Vector Space Mining*)** :
   * *Principe* : Extraire les métadonnées et descriptions d'un grand catalogue (ex. les 146 000 jeux de Steam), transformer ces données en vecteurs avec Claude, puis faire repérer par l'IA les « trous » (concepts n'existant encore nulle part) pour concevoir un produit totalement inédit.
5. **Génération de micro-jeux vidéo personnalisés comme cadeaux/outils marketing** :
   * *Principe* : Utiliser Claude Code pour développer en une soirée un jeu web interactif en 2D/3D thématisé pour un client, une entreprise ou un événement privé, accessible directement via un QR code.
6. **Synthèse de connaissances massives en guides vendables ou outils de prospection** :
   * *Principe* : Faire ingérer des dizaines d'heures de podcasts ou de vidéos d'experts à Claude Code/NotebookLM pour en extraire une méthodologie condensée en 10 minutes de lecture.

---

### 4) Chiffres de revenus et montants financiers annoncés
*(Toutes ces données sont directement affirmées par l'auteur dans la vidéo)*

* **Économie sur la résiliation d'un SaaS individuel** : un outil payé 20 €/mois coûte 240 €/an ; sa création via Claude Code permet d'annuler cet abonnement *(affirmé par l'auteur)*.
* **Économie sur les rendus / visites 3D de maisons** : les constructeurs facturent généralement entre **5 000 € et 10 000 €** par plan pour une modélisation 3D interactive, réalisable via Claude Code et Three.js *(affirmé par l'auteur)*.
* **Expérience Anthropic « Project Deal »** : 69 employés ont reçu **100 $** chacun pour faire négocier leurs agents IA autonomes, générant **186 transactions** et **4 000 $** d'échanges automatisés sans intervention humaine *(affirmé par l'auteur)*.
* **Financement de recherche médicale (Miriam González)** : Anthropic a versé **30 000 $** de crédits Claude gratuits pour soutenir son projet de recherche d'un vaccin personnalisé contre son cancer *(affirmé par l'auteur)*.
* **Prix d'une imprimante ticket Bluetooth** : environ **20 €** *(affirmé par l'auteur)*.
* **Prix d'un boîtier domotique d'entrée de gamme** : environ **20 €** *(affirmé par l'auteur)*.
* **Valeur marchande d'un écran de contrôle domotique mural** : plus d'une centaine d'euros en magasin *(affirmé par l'auteur)*.
* **Économie sur l'apprentissage du pilotage de drone** : évite le crash d'un drone FPV de course d'une valeur d'environ **400 €** grâce à un simulateur d'assemblage 3D codé par l'IA *(affirmé par l'auteur)*.
