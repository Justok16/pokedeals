# Je crée "letmegooglethat" mais pour ChatGPT en 40 minutes.

Vidéo : https://youtu.be/6idfpTFrRaY · durée 51:44 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Le créateur réalise un défi en direct : créer en 40 minutes une application web inspirée de « Let Me Google That For You », mais adaptée pour ChatGPT (permettant de générer un lien interactif qui simule la recherche d'une question sur ChatGPT avec une animation de curseur).

2) **Outils, sites et dépôts GitHub cités :**
- **Cursor** (ou l'éditeur de code utilisé dans la vidéo) : éditeur de code basé sur l'IA (non précisé si gratuit ou payant).
- **ChatGPT** (openai.com) : outil d'IA conversationnelle (non précisé si gratuit ou payant).
- **Porkbun** (porkbun.com) : site d'achat et de gestion de noms de domaine (payant).
- **shadcn/ui** (ui.shadcn.com) : bibliothèque de composants UI pour React/Tailwind (gratuit).
- **Vercel** (vercel.com) : plateforme de déploiement et d'hébergement web (gratuit/payant selon les offres).
- **GitHub** (github.com) : plateforme de gestion de code source et de déploiement (gratuit/payant).

3) **Astuces concrètes et réutilisables :**
- Utiliser un générateur de noms de domaine (comme sur Porkbun) pour trouver rapidement des idées de noms courts et pertinents.
- Cloner l'interface d'un site existant (comme ChatGPT ou une application de référence) en inspectant les éléments du DOM pour récupérer les classes CSS, les couleurs et les polices, puis les réadapter dans son projet Next.js avec Tailwind.
- Utiliser `useSearchParams` de Next.js pour récupérer dynamiquement une requête (query) dans l'URL et afficher l'interface en conséquence.
- Créer un composant d'animation de curseur et de saisie de texte pour simuler une recherche interactive.

4) **Chiffres de revenus annoncés :** Non précisé.

---
