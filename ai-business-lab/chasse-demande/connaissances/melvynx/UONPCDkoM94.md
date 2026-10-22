# Je refais mon blog de 0 (Design / Stack / NextJS)

Vidéo : https://youtu.be/UONPCDkoM94 · durée 13:34 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de présenter les 4 étapes clés (réflexion/design, création de l'application, rédaction du blog avec MDX, et déploiement) pour concevoir et lancer un blog moderne sous Next.js, en optimisant le référencement et l'expérience de développement.
2)
- Next.js : framework React (gratuit/open-source) pour le développement web.
- MDX : format de fichiers (gratuit/open-source) combinant Markdown et composants React pour rédiger des articles de blog.
- Vercel : plateforme d'hébergement et de déploiement (freemium).
- Upstash : service de base de données / Redis sans serveur (freemium/payant selon usage) utilisé pour stocker et compter les vues des articles en temps réel.
- Shiki : bibliothèque de coloration syntaxique (gratuit/open-source) pour mettre en valeur les blocs de code dans les articles.
3) Astuces :
- S'inspirer des meilleurs blogs existants (structure, design, table des matières) avant de coder pour valider l'expérience utilisateur.
- Utiliser Static Site Generation (SSG) dans Next.js pour pré-générer les pages de blog au moment du build (via `generateStaticParams`), garantissant un affichage instantané comparé au rendu côté client.
- Stocker les articles sous forme de fichiers MDX enrichis de métadonnées (frontmatter) et utiliser des plugins (comme Gray-matter et MDX Remote) pour les parser et y intégrer directement des composants React interactifs.
4) Chiffres :
- Plus de 1116 vues enregistrées sur un article de test (affirmé par l'auteur).
