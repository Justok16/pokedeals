# Mon nouveau portfolio et blog de développeur (redesign complet)

Vidéo : https://youtu.be/oYY0NRfO3iw · durée 14:07 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de présenter la refonte complète et minimaliste du blog et du site personnel de l'auteur (codelynx.dev et melvynx.com), passés sous Next.js (SSG/SSR), avec un design épuré, des polices de caractères soignées et l'utilisation de tests A/B (avec PostHog) pour optimiser les conversions.

2) Outils, sites et dépôts cités :
- Next.js : Framework React (gratuit), utilisé pour la structure et le rendu des sites (SSG/SSR).
- Prisma : ORM (gratuit), utilisé pour la gestion de la base de données.
- PostgreSQL : Base de données (gratuite/payante selon l'hébergement).
- Tailwind CSS : Framework CSS (gratuit) pour le design.
- PostHog : Outil d'analyse et d'A/B testing (gratuit/payant), utilisé pour tester les versions des pages (contrôle vs test).
- GitHub : Dépôt de code (gratuit/payant) pour stocker les projets.
- Vercel : Plateforme d'hébergement (gratuite/payante) pour déployer les sites.

3) Astuces concrètes et réutilisables :
- Épurer le design des blogs/sites en supprimant les éléments superflus (vues, likes, etc.) pour se concentrer sur l'essentiel et améliorer la lisibilité.
- Utiliser le rendu côté serveur (SSR/SSG) avec Next.js et MDX (via next-mdx-remote) pour injecter des composants React directement dans les articles de blog.
- Mettre en place des tests A/B (ex: avec PostHog et des feature flags) pour comparer la conversion de différentes versions d'une page (ex. page de formation ou d'inscription).
- Configurer des redirections (rewrites) dans Next.js pour fusionner plusieurs domaines/sous-domaines sous un même site principal sans tout migrer manuellement.

4) Chiffres de revenus annoncés (affirmés par l'auteur) :
- Non précisé.
