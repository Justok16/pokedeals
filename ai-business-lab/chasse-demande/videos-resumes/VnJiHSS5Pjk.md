# VnJiHSS5Pjk — « You NEED to Try Claude Projects From Your Phone (Building A Full App) »

- Auteur : Riley Brown ; lien : https://youtu.be/VnJiHSS5Pjk
- Envoyée par l'utilisateur le 13/11/2026 ; résumée le 13/11 par Gemini (via le relais, modèle gemini-3.5-flash ; vidIQ sans crédits ce mois-ci)
- Les durées et nombres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (13/11)

Démonstration : une application complète (Mac, iPhone, site, vidéos) construite depuis un téléphone, à la voix, avec Claude Code. Comparé à ce que fait DIG16 :

- **Travail depuis le téléphone, à la voix** : c'est déjà notre façon de travailler (l'utilisateur dicte ou écrit depuis son téléphone, Claude exécute). Rien à changer.
- **Plusieurs conversations en parallèle, une par chantier** : à l'inverse de la décision du 11/11 (une seule conversation pour l'utilisateur). On garde notre règle : les conversations de service existent, mais elles restent invisibles et renvoient tout dans LA conversation.
- **Produire aussi les supports de vente (site, vidéo, annonce), pas seulement le produit** : déjà notre règle (kit client complet, textes d'annonce, vidéos de conseils).
- **Convex (base de données)** : déjà en réserve (`connaissances/reserve-prete.md`, à ressortir pour un client qui veut un espace membre ou vendre en ligne). Offre gratuite à relire à la source le jour où on s'en sert.
- **Blender piloté par Claude** : déjà en réserve (même auteur, direct lKIhUBjCgZM).
- **Écartés** : RunPod (payant, budget 0 €), ElevenLabs (nos vidéos ont déjà leur voix ; offre gratuite limitée), Screen Studio et Rotato (payants, hors besoin).

Conclusion : rien à installer, rien de nouveau à retenir ; la vidéo confirme la méthode en place.

## Résumé (Gemini)

Voici le résumé structuré de la vidéo, rédigé pour une personne souhaitant créer et vendre des produits logiciels ou des services grâce à l'IA et à Claude Code :

---

### 1) Idée principale
L'auteur démontre qu'il est possible de **concevoir, développer et lancer un produit logiciel complet (applications Mac & iOS, site web et vidéos marketing)** en quelques heures, entièrement depuis son smartphone grâce aux commandes vocales transmises à l'agent **Claude Code**. 

Dans cet exemple, il crée l'application **Glaze** (un clone de *Screen Studio* pour Mac et iPhone), génère sa charte graphique, développe les applications natives, crée la landing page et produit deux vidéos promotionnelles (une vidéo 3D et une pub vidéo UGC).

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code (Application Claude / Projects)**
    *   *Statut :* Payant (Nécessite un abonnement Anthropic ou accès API).
    *   *Rôle :* Agent IA principal piloté à la voix sur iPhone qui génère le code, gère les sous-tâches, conçoit le design et orchestre les builds.
*   **Opus 5.5 / Fable 5.2 / Mythos 5.2**
    *   *Statut :* Inclus dans l'écosystème Claude (payant).
    *   *Rôle :* Modèles de langage et d’IA utilisés par Claude Code pour le raisonnement, le code complexe et la création graphique.
*   **Convex** *(Sponsor de la vidéo)*
    *   *Statut :* Gratuit (Plan *Free & Starter* à 0 $/mois) ; payant pour les besoins d'entreprise.
    *   *Rôle :* Base de données temps réel et backend réactif. Il gère la synchronisation instantanée des données entre mobile et navigateur, le stockage et les fonctions serveur sans gestion d'infrastructure.
*   **Plugin Convex pour Claude Code** (`/plugin install convex`)
    *   *Statut :* Gratuit / Open-source.
    *   *Rôle :* Permet à Claude Code de connecter et de configurer automatiquement le backend Convex dans l'application.
*   **Vercel**
    *   *Statut :* Gratuit (avec offres payantes).
    *   *Rôle :* Plateforme d'hébergement où la landing page du produit est déployée automatiquement par l'IA.
*   **Blender**
    *   *Statut :* Gratuit / Open-source.
    *   *Rôle :* Logiciel 3D piloté par l'IA pour créer la scène 3D de démonstration du produit et la vidéo de lancement.
*   **RunPod**
    *   *Statut :* Payant (Calcul GPU cloud à la consommation).
    *   *Rôle :* Ferme de rendu dans le cloud permettant de calculer et rendre les scènes 3D Blender très rapidement.
*   **ElevenLabs**
    *   *Statut :* Gratuit (limité) / Payant.
    *   *Rôle :* Générateur de voix off IA ultra-réaliste pour la vidéo publicitaire UGC.
*   **Screen Studio** *(Référence)*
    *   *Statut :* Payant.
    *   *Rôle :* Logiciel de capture d'écran Mac utilisé comme modèle/référence pour le produit créé ("Glaze").
*   **Rotato** *(Référence)*
    *   *Statut :* Payant.
    *   *Rôle :* Logiciel d'animation 3D de maquettes d'appareils cité pour inspirer le comportement des animations mobiles.

---

### 3) Astuces concrètes et réutilisables

1.  **Pilotage 100 % vocal sur mobile :** Utilisez la dictée vocale de votre smartphone dans l'application Claude. Vous pouvez décrire des fonctionnalités complexes, ajuster le design ou demander des correctifs de bugs sans toucher à un clavier.
2.  **Parallélisation des tâches via des sessions séparées (Threads) :** Pour éviter de surcharger la mémoire (contexte) de l'IA, ouvrez plusieurs conversations simultanées dans Claude Projects :
    *   Session 1 : Recherche et architecture globale.
    *   Session 2 : Design/UI (génération de planches Figma/mockups).
    *   Session 3 : Développement du code (Mac + iOS).
    *   Session 4 : Création du site web (Landing page).
    *   Session 5 : Production média (Scène 3D Blender & Vidéo UGC).
3.  **Utilisation d'un backend "Zero-Config" pour les apps générées par IA :** Associez Claude Code à une solution comme Convex. L'IA peut installer le plugin et intégrer une base de données temps réel + de l'authentification en quelques secondes sans écriture manuelle de scripts SQL.
4.  **Production automatisée d'assets marketing complets :** Ne vous arrêtez pas au code du logiciel. Demandez à l'IA de concevoir :
    *   L'identité visuelle (logos/icônes déclinés en plusieurs variantes).
    *   Le site vitrine prêt à recevoir des inscriptions.
    *   Une vidéo de lancement produit 3D (via des scripts Blender).
    *   Une publicité UGC dynamique avec sous-titres et voix off IA (ElevenLabs).
5.  **Boucle de test et correctif en direct :** Installez le build généré par l'IA sur votre propre Mac/iPhone, notez visuellement ce qui ne va pas (ex. : reflet trop fort, animation saccadée, zoom trop agressif), puis dictez les ajustements précis à l'IA pour qu'elle répare le code.

---

### 4) Chiffres de revenus annoncés

*   **Revenus générés :** Non précisé *(affirmé par l'auteur : aucun chiffre d'affaires ou revenu financier personnel n'est mentionné dans cette vidéo de démonstration technique)*.
*   **Temps de réalisation annoncé :** Produit complet développé en **quelques heures** avec environ **20 à 25 prompts vocaux** *(affirmé par l'auteur)*.
