# Les métadatas streaming de Next.js mises au clair

Vidéo : https://youtu.be/_Y7x9vh_CIk · durée 3:00 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes consignes :

### 1) Idée principale
La vidéo discute de l’utilisation de Next.js et de son impact sur le référencement naturel (SEO) en raison du mécanisme de "metadata streaming". L'auteur analyse les implications négatives potentielles de cette fonctionnalité sur l'indexation par les moteurs de recherche pour les sites dynamiques et statiques, en insistant sur le fait que certains bots incapables d'exécuter JavaScript (comme Twitterbot) pourraient bloquer le rendu des pages.

---

### 2) Outils, sites et dépôts GitHub cités
* **Next.js**
  * **Type :** Gratuit (open-source)
  * **Utilité :** Framework de développement web basé sur React, connu pour sa portabilité et sa modularité, permettant de créer des applications web et des sites statiques ou dynamiques.
* **Vercel**
  * **Type :** Non précisé (offrant des services gratuits et payants pour l'hébergement)
  * **Utilité :** Plateforme d'hébergement et de déploiement optimisée pour les applications Next.js.
* **Googlebot**
  * **Type :** Gratuit
  * **Utilité :** Robot d'indexation de Google capable d'exécuter du JavaScript.
* **Twitterbot**
  * **Type :** Gratuit
  * **Utilité :** Robot d'indexation de Twitter (X) incapable d'exécuter du JavaScript.

---

### 3) Astuces concrètes et réutilisables
* **Attention au SEO dynamique avec Next.js :** Éviter de générer des métadonnées dynamiques trop complexes si cela bloque ou ralentit le rendu initial des pages, car cela peut nuire à l'indexation par les robots qui n'exécutent pas JavaScript.
* **Vérification du User-Agent :** Next.js analyse le `User-Agent` pour déterminer si les métadonnées doivent être "streamées" ou non, selon la capacité du bot à exécuter du JavaScript.

---

### 4) Chiffres de revenus annoncés
* **Affirmé par l'auteur :** Non précisé
