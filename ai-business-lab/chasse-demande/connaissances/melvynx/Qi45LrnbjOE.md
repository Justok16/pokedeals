# NextJS Version 13.2 - Test des nouveautés ⚛️ (c'est du très lourd)

Vidéo : https://youtu.be/Qi45LrnbjOE · durée 13:29 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. L'idée principale de cette vidéo est de présenter et de tester en direct les nouveautés de la version 13.2 de Next.js (métadonnées simplifiées, route handlers, intégration MDX, etc.) en développant une application concrète avec Prisma et TypeScript.

2. Outils, sites ou dépôts GitHub cités :
- Next.js 13.2 (framework, gratuit) : version testée dans la vidéo.
- Prisma (ORM, gratuit) : utilisé pour gérer la base de données.
- TypeScript (langage, gratuit) : utilisé pour le typage.
- Vercel (plateforme d'hébergement, gratuit/payant) : mentionné pour le déploiement.
- React (librairie, gratuit) : mentionné.
- Dépôt GitHub / site du créateur (CodeLynx / Codeline, avec un cours gratuit sur Next.js, Server Components, TypeScript et React-Query) : mentionné pour approfondir l'apprentissage.

3. Astuces concrètes et réutilisables :
- Utiliser l'objet de constante `metadata` dans le fichier `layout.tsx` pour définir dynamiquement et proprement le titre et les balises meta d'une page sans créer de fichiers *head* séparés.
- Mettre en place des *Route Handlers* dans le dossier `app/api/.../route.ts` pour créer des points de terminaison API robustes en récupérant les requêtes JSON (`await request.json()`) et en renvoyant des réponses adaptées (`NextResponse.json(...)`).
- Utiliser l'option `use client` en haut de fichier pour basculer un composant en mode client lorsque l'interactivité ou des hooks (comme `useState` ou `useEffect`) sont nécessaires.

4. Chiffres de revenus annoncés :
- Non précisé.
