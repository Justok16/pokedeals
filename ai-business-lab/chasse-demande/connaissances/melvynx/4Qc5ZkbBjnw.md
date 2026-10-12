# TUTO / COURS Test Unitaire avec NextJS / Vitest

Vidéo : https://youtu.be/4Qc5ZkbBjnw · durée 16:24 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Apprendre à tester les composants et applications React/Next.js à l'aide du framework de test Vitest et de ses plugins dédiés.

2) **Outils, sites ou dépôts cités** :
- **Vitest** : Framework de test unitaire nouvelle génération (gratuit).
- **Vitest Plugin React** : Plugin pour intégrer React à Vitest (gratuit).
- **JSDOM** : Environnement DOM simulé pour Node.js (gratuit).
- **Testing Library (React Testing Library)** : Bibliothèque pour tester les composants React (gratuit).

3) **Astuces concrètes et réutilisables** :
- Installer Vitest et configurer le fichier `vitest.config.ts` avec le plugin React et l'environnement JSDOM.
- Créer un fichier de configuration globale `vitest.setup.ts` pour initialiser les matchers (comme `toBeInTheDocument`).
- Utiliser `beforeEach` pour nettoyer le DOM (`cleanup`) entre chaque test et éviter les conflits d'éléments multiples.
- Mocker les objets globaux non disponibles dans l'environnement de test (comme `ResizeObserver` ou `scrollIntoView`).
- Automatiser l'exécution des tests dans les workflows CI/CD (GitHub Actions) en configurant une étape dédiée avec `pnpm test:run`.

4) **Chiffres de revenus annoncés** :
- Non précisé.

---
