# TUTO : Cursor en mode AGENT pour créer des FONCTIONNALITÉS complètes !

Vidéo : https://youtu.be/TLiDfHfFtrw · durée 14:34 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :**
La vidéo montre comment utiliser **Cursor** (couplé à l'IA) pour créer rapidement une nouvelle fonctionnalité de A à Z dans une application existante (un outil de workflow d'e-mailing). L'auteur illustre l'importance de bien guider l'IA en lui fournissant un contexte précis (fichiers ciblés, règles strictes) plutôt que de lui laisser quartier libre, afin d'obtenir un code propre et fonctionnel du premier coup.

2. **Outils, sites et dépôts GitHub cités :**
- **Cursor** (IDE / Modèle freemium) : Éditeur de code assisté par IA utilisé pour coder la fonctionnalité.
- **Ingest** (Site/Outil : `ingest.dev` ou Ingest Dev Server / Gratuit) : Outil de gestion des flux, webhooks et files d'attente (queues) utilisé pour tester et exécuter les workflows en local.
- **Prisma** (ORM / Gratuit) : Utilisé pour la gestion de la base de données et les migrations.
- **Next.js** (Framework / Gratuit) : Framework React utilisé pour l'application SaaS.
- **TypeScript** (Langage / Gratuit) : Utilisé pour le typage des données.
- **Formation MLV (Site : `mlv.sh/ai`)** (Formation / Payant) : Programme de formation de l'auteur sur les agents IA et les bonnes pratiques de développement avec Cursor.

3. **Astuces concrètes et réutilisables :**
- **Règle d'or pour prompter l'IA :** Ne jamais laisser l'IA chercher le contexte toute seule (ce qui donne des résultats aléatoires et lents). Il faut **donner des fichiers en contexte**, **préciser *comment* faire la feature** et **donner des règles strictes à suivre**.
- Utiliser le mode "Composer" de Cursor pour orchestrer des modifications multi-fichiers en une seule fois (ex: mise à jour du schéma Prisma, des actions serveur, et des composants UI).
- Travailler en mode hybride (humain pilote + IA exécutant) : l'humain comprend le besoin, choisit l'architecture et guide l'IA pas à pas pour s'assurer que le code généré respecte les standards du projet.

4. **Chiffres de revenus annoncés :**
- Non précisé.

---
