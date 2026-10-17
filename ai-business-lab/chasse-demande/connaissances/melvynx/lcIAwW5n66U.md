# L'IA créée et PUBLIE une app iOS pour moi (100% automatiser)

Vidéo : https://youtu.be/lcIAwW5n66U · durée 17:50 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur montre comment créer, déboguer, tester et publier de manière 100 % autonome une application mobile et web complète (SaaS monétisable avec abonnements/crédits) sur l'App Store (iOS) et Google Play Store (Android) en utilisant un agent IA de code (type Claude Code / Codex) guidé par un ensemble de compétences personnalisées (*skills*) et un *boilerplate* prêt à l'emploi (*NowStack Mobile*).

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité / Rôle |
| :--- | :--- | :--- |
| **Codex / Claude Code CLI (Agent IA)** | Payant (coût des API / abonnements LLM) | Agent autonome exécutant des commandes terminal, modifiant le code et déboguant l'application. |
| **NowStack Mobile (`ns-mobile`)** | *Non précisé* (base de code / boilerplate propriétaire de l'auteur) | *Boilerplate* complet mobile (React Native) + web + backend avec *skills* d'agents IA intégrés. |
| **Glow AI (Funny Headshot)** | Application de démonstration | Application mobile/web générant des photos de profil professionnelles par IA à partir d'un selfie. |
| **Convex** | Freemium (Gratuit / Payant) | Backend réactif et base de données temps réel qui synchronise automatiquement l'état avec l'UI. |
| **React Native / Tailwind CSS / Shadcn UI** | Gratuit (Open-source) | Développement de l'interface mobile iOS et Android. |
| **TanStack Start** | Gratuit (Open-source) | Framework web pour la landing page et l'application web. |
| **Better-Auth** | Gratuit (Open-source) | Système d'authentification utilisateur (Email/OTP, Apple, Google). |
| **Cloudflare** | Freemium (Gratuit / Payant) | Hébergement, stockage et optimisation de la distribution des images. |
| **App Store Connect / TestFlight** | Payant (Compte Apple Developer à ~99 $/an) | Soumission, gestion des achats intégrés/abonnements et tests de l'application iOS. |
| **Google Play Console** | Payant (Frais unique de 25 $) | Publication et gestion des versions bêta Android. |
| **GitHub & Vercel** | Freemium | Gestion de versions et déploiement continu de l'application web. |
| **Excalidraw** | Gratuit / Freemium | Tableau blanc utilisé pour schématiser l'architecture technique. |
| **`mlv.sh/fm` (ou `mlv.sh/formation-fm`)** | Gratuit | Lien vers la mini-formation offerte par l'auteur (« De zéro à l'App Store avec l'IA »). |
| **SaveIt.now & Padel Tally** | Applications de l'auteur | Autres projets SaaS/mobiles créés avec la même méthodologie. |

---

### 3) Astuces concrètes et réutilisables

1. **Créer des *Skills* dédiés pour l'IA (fichiers Markdown / CLI) :** 
   Fournir à l'agent IA des guides procéduraux réutilisables (ex. déploiement TestFlight, configuration d'achats in-app, capture automatique de screenshots de stores) pour qu'il exécute ces tâches complexes sans intervention humaine.
2. **Implémenter une règle de vérification stricte (`/verify` / Proof of Work) :** 
   Interdire à l'agent IA de valider une tâche sans preuve d'exécution réelle (logs de runtime, captures d'écran sur simulateur Metro/iOS/Android).
3. **Centraliser les logs dans des fichiers plats (`.log`) :** 
   Rediriger les sorties console (`convex.log`, `web.log`, etc.) via un script unique (`pnpm start-all`). Cela permet à l'IA de lire directement les erreurs d'exécution pour s'auto-corriger.
4. **Utiliser un backend réactif (Convex) :** 
   La synchronisation temps réel évite d'avoir à faire coder à l'IA une gestion d'état complexe côté frontend (les crédits, paiements et listes s'actualisent automatiquement).
5. **Résolution automatique des rejets de stores :** 
   Copier-coller les messages de rejet de l'App Store Connect ou Google Play Console directement à l'agent pour qu'il mette à jour la configuration et reconstruise les versions automatiquement.

---

### 4) Chiffres de revenus annoncés
* **Affirmé par l'auteur :** Aucun chiffre de chiffre d'affaires ou de gain financier généré n'est mentionné dans la vidéo (le tableau de bord de test affiche `0.00 $` et les paliers de prix montrés dans l'application sont de `5 $` et `20 $`, mais aucun revenu global n'est revendiqué).
