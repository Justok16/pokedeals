# Il a créé l'outil d'espionnage ultime (gratuit et open-source)

Vidéo : https://youtu.be/S2VJU5DQqlU · durée 21:48 · résumé Gemini (gemini-3.7-flash) du 2026-09-30
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo présente **God’s Eye View**, un projet open-source créé par Bilawal Sidhu qui fonctionne comme un simulateur de satellite espion / tableau de bord de renseignement géospatial (OSINT) directement dans le navigateur. Il agrège en temps réel et en 3D des données publiques mondiales (vols aériens, navires maritimes, trafic routier, caméras de surveillance publiques, feux de forêt, tremblements de terre, câbles sous-marins, centres de données, lancements spatiaux). La vidéo montre également comment utiliser un agent de code IA (comme l'application ChatGPT avec environnement local ou Claude Code) pour cloner, installer et faire tourner automatiquement un projet GitHub complexe en moins de 2 minutes.

---

### 2) Outils, sites et dépôts GitHub cités

| Nom exact | Gratuit / Payant | Utilité / Rôle |
| :--- | :--- | :--- |
| **gods-eye-view** (GitHub : `bilawalsidhu/gods-eye-view`) | **Gratuit** (Open-source) | Application principale : simulateur 3D géospatial interactif affichant des flux de données mondiaux en temps réel. |
| **Cesium Ion** | **Gratuit** (avec paliers payants selon usage) | Moteur de globe 3D et fournisseur d'imagerie satellite/terrain. |
| **Google Maps Platform** (3D Photorealistic Tiles / Places) | **Gratuit** (crédit mensuel offert / payant à l'usage au-delà) | Fournit la cartographie photoréaliste 3D des villes et les données d'adresses/bâtiments. |
| **OpenAI API** (ChatGPT Realtime / Voice) | **Payant à l'usage** (quelques centimes à dollars selon usage ; optionnel) | Permet de commander la carte à la voix et d'obtenir des explications contextuelles orales sur les éléments observés. |
| **OpenSky Network / adsb.lol** | **Gratuit** (clé optionnelle pour plus de requêtes) | Suivi en temps réel des vols commerciaux et militaires. |
| **AISStream** | **Gratuit** (avec clé API) | Suivi en temps réel de la position des navires et bateaux dans le monde. |
| **NASA FIRMS** | **Gratuit** (avec clé API) | Détection par satellites thermiques des feux de forêt et incendies actifs sur Terre. |
| **TomTom API** | **Gratuit** (palier gratuit / payant au-delà) | Données en direct sur la densité et la fluidité du trafic routier urbain. |
| **Launch Library 2** | **Gratuit** (avec clé API) | Données sur les lancements de fusées et missions spatiales récentes/à venir. |
| **Claude (Opus 3.5 / Claude Code)** | **Payant / Gratuit selon forfait** | Modèle d'IA utilisé pour le développement full-stack du code et l'automatisation d'installation. |
| **Google Gemini** | **Payant / Gratuit selon forfait** | Utilisé lors de la conception pour le raisonnement spatial. |
| **ChatGPT App / Desktop Projects** | **Gratuit / Payant (Plus/Team)** | Utilisé dans la vidéo pour cloner le dépôt, installer les dépendances et lancer l'application en local sans coder manuellement. |
| **Vantor** | **Commercial / Payant** *(cité)* | Fournisseur d'imagerie satellite commerciale haute résolution (utilisé pour les reconstructions après catastrophes). |

---

### 3) Astuces concrètes et réutilisables

* **Déploiement en 1 invite (prompt) via agent IA** : Au lieu d'installer manuellement Node.js, Git et les dépendances, vous pouvez ouvrir l'application ChatGPT (mode Projet local) ou Claude Code, cibler un dossier vide et coller le prompt suivant :
  > *"Clone this GitHub repo `[URL]`, read the instructions, install all necessary dependencies, and then tell me what I need to do to finalize the setup and get everything working."*
* **Création d'expériences 3D interactives rentables** : Bilawal explique avoir combiné des modèles spécialisés pour coder le projet (Gemini pour le raisonnement spatial et Claude Opus pour le code full-stack). Vous pouvez réutiliser cette architecture open-source pour vendre des dashboards sur-mesure (suivi logistique, surveillance d'infrastructures, analyses d'assurance après sinistre ou journalisme d'investigation).
* **Reconstruction 3D d'événements réels** : En synchronisant les flux satellites, les modèles 3D photoréalistes, les données audio ATC (contrôle aérien) et les vidéos d'utilisateurs (UGC), il est possible de reconstruire précisément le déroulement d'accidents (ex. crash d'avion NTSB) ou de catastrophes naturelles (ex. inondations au Népal).
* **Gestion des coûts d'API** : Le projet fonctionne gratuitement si l'on n'active pas l'interaction vocale en direct (OpenAI Realtime). Pour un usage personnel standard, les clés d'API gratuites des différents fournisseurs de données suffisent largement.

---

### 4) Chiffres de revenus annoncés

* **Revenus / Gains mentionnés** : **Non précisé** *(la vidéo ne mentionne aucun chiffre de revenus, de gains financiers ou de ventes ; il s'agit d'une présentation technique d'un projet open-source gratuit).*
