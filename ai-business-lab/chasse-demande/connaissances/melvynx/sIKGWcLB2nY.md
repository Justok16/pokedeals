# TUTO Shadcn UI avec TailwindCSS : Tout comprendre en 30 minutes

Vidéo : https://youtu.be/sIKGWcLB2nY · durée 30:19 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** La vidéo présente **shadcn/ui**, une bibliothèque de composants moderne et populaire pour React et Next.js. Contrairement aux bibliothèques traditionnelles installées via npm, shadcn/ui permet de copier et d'installer directement le code source des composants dans son propre projet, offrant ainsi un contrôle total sur la personnalisation et la modification du code.

2. **Outils, sites ou dépôts cités :**
- **shadcn/ui** (*ui.shadcn.com*) : Bibliothèque de composants open source pour React et Next.js, gratuite.
- **Tailwind CSS** (*tailwindcss.com*) : Framework CSS utilitaire, gratuit.
- **React** (*react.dev*) : Bibliothèque JavaScript, gratuite.
- **Next.js** (*nextjs.org*) : Framework React, gratuit.
- **Radix UI** (*radix-ui.com*) : Bibliothèque de composants primitifs non stylisés pour React, gratuite.
- **clsx** et **tailwind-merge** : Bibliothèques utilitaires pour fusionner des classes CSS, gratuites.
- **VS Code** : Éditeur de code, gratuit.
- **GitHub** : Plateforme de code, gratuite.
- **ui.jin.dev** (*ui.jin.dev*) : Site proposant des thèmes communautaires pour shadcn/ui, gratuit.

3. **Astuces concrètes et réutilisables :**
- Utiliser la commande d'initialisation (`npx shadcn-ui@latest init`) pour configurer automatiquement le fichier `components.json` et lier Tailwind CSS.
- Créer une fonction utilitaire `cn` (combinant `clsx` et `tailwind-merge`) pour fusionner et gérer les priorités des classes CSS conditionnelles.
- Utiliser les variants via **CVA** (*Class Variance Authority*) pour gérer dynamiquement les styles (tailles, couleurs) d'un composant (ex: `<Button variant="red">`).
- Intégrer les composants primitifs de **Radix UI** pour bénéficier d'une accessibilité native gérée au clavier (navigation par tabulation, fermeture avec Échap).

4. **Chiffres de revenus annoncés :**
- Non précisé.
