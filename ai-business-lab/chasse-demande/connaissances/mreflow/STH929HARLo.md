# 9 compétences IA gratuites qui ressemblent à des codes de triche

Vidéo : https://youtu.be/STH929HARLo · durée 29:14 · résumé Gemini (gemini-3.8-flash) du 2026-09-30
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale

La vidéo présente une sélection des meilleures **compétences (*skills*)** et **extensions (*plugins*)** open-source et gratuites à intégrer dans des environnements de développement pilotés par l'IA (comme Claude Code ou OpenAI Codex). 
Ces modules permettent de transformer un agent IA en une équipe d'ingénierie complète : ils automatisent le cadrage d'idées de projets, l'audit de code, la création de designs soignés, la recherche de tendances en ligne, la cartographie de bases de code et la génération automatisée de vidéos animées en code. Pour quelqu'un cherchant à monétiser ces outils, ils permettent de créer des applications, des services d'audit ou du contenu vidéo commercialisable beaucoup plus rapidement.

---

### 2) Outils, sites et dépôts GitHub cités

| Nom exact | Gratuit ou Payant | Utilité |
| :--- | :--- | :--- |
| **Claude Code** (Anthropic) | Non précisé dans la vidéo (généralement soumis à la tarification de l'API / abonnement Anthropic) | Outil en ligne de commande / environnement agentique de développement pour interagir avec Claude. |
| **OpenAI Codex** (Application Codex) | Non précisé dans la vidéo | Environnement de bureau pour exécuter des tâches de codage assisté par IA. |
| **Claude Cowork**, **Cursor**, **OpenClaw**, **Hermes**, **VS Code**, **GitHub Copilot** | Non précisé dans la vidéo | IDEs et environnements d'exécution pour agents IA compatibles avec les compétences présentées. |
| **gstack** (`github.com/garrytan/gstack`) | Gratuit (licence MIT) | Créé par Garry Tan (CEO de Y Combinator). Transforme Claude Code / Codex en équipe d'ingénieurs virtuelle (23 spécialistes et 8 commandes rapides) : cadrage de produit, audit de code, QA, tests de sécurité, etc. |
| **stop-slop** (`github.com/hardikpandya/stop-slop`) | Gratuit (licence MIT) | Fichier de compétence qui supprime des textes générés par IA le style générique, pompeux ou répétitif typique des LLMs (*AI slop*). |
| **ChatGPT** (OpenAI) | Non précisé (utilisé ici pour un exemple de texte) | Modèle de langage utilisé brièvement pour générer un texte brut à corriger. |
| **graphify** (`github.com/safishamshi/graphify`) | Gratuit | Analyse des bases de code, wikis ou notes et les convertit en un graphe de connaissances interactif (HTML/JSON). Sert de couche mémoire interrogeable pour économiser des tokens. |
| **Understand-Anything** (`github.com/chienvon/Understand-Anything`) | Gratuit | Convertit n'importe quel dépôt de code en carte d'architecture interactive (routes API, modèles de données, sécurité) facilitant l'onboarding et l'analyse. |
| **skills.sh** | Gratuit (accès web) | Annuaire et registre en ligne répertoriant les compétences pour agents IA les plus populaires. |
| **frontend-design** (`anthropics/skills`) | Gratuit | Compétence officielle d'Anthropic pour concevoir des interfaces web et composants front-end plus esthétiques et modernes. |
| **taste-skill** (`github.com/Leonxlnx/taste-skill`) | Gratuit | Framework anti-slop front-end qui applique de bonnes pratiques de typographie, d'espacement et de design aux pages web générées. |
| **Remotion** (`github.com/remotion-dev/remotion`) | Gratuit (open-source) | Outil permettant de créer et rendre des vidéos et animations (ex. graphiques animés, faux échanges SMS) directement via du code React/Web. |
| **hyperframes** (`github.com/heygen-com/hyperframes`) | Gratuit | Développé par HeyGen. Compétence de génération d'animations vidéo (courbes boursières, révélations de logos, effets particules) à partir d'un simple prompt textuel. |
| **Future Tools** (`futuretools.io`) | Gratuit (site et newsletter) | Plateforme de l'auteur répertoriant les outils d'IA. Il y mentionne une ressource gratuite appelée « AI Income Database » accessible via l'inscription à sa newsletter. |

---

### 3) Astuces concrètes et réutilisables

1. **Installation ultra-rapide des compétences :** 
   - Pour installer une compétence ou un plugin dans Claude Code ou Codex, il suffit de coller l'URL du dépôt GitHub directement dans le prompt et d'écrire : `Install this for me please: [URL_GITHUB]`. L'agent clone, configure et intègre les fichiers sans intervention manuelle.
2. **Valider une idée de SaaS ou d'application avant de coder :**
   - Utilisez la commande `/gstack-office-hours` issue de `gstack`. L'agent endosse le rôle d'un associé Y Combinator et vous soumet à un *stress-test* de 20 minutes (questions sur votre cible, modèle économique, proposition de valeur) et produit un cahier des charges complet en Markdown.
3. **Auditer son code automatiquement :**
   - Avec `/gstack-review`, l'IA inspecte le différentiel de code comme un ingénieur senior (recherche de failles de sécurité OWASP, incohérences UX, cas limites non gérés).
4. **Réduire la consommation de tokens et les coûts d'API :**
   - En créant un graphe de connaissances avec `graphify` ou `Understand-Anything`, vous donnez à l'IA une couche mémoire structurée. Vous pouvez l'interroger sur l'ensemble de votre projet sans devoir réinjecter tous les fichiers sources dans le contexte.
5. **Combinaison de compétences front-end pour de meilleurs résultats :**
   - Associer deux compétences complémentaires dans le même prompt (par exemple `frontend-design` d'Anthropic et `taste-skill`) permet de générer des prototypes de sites web plus vendeurs pour des clients, sans effet « modèle générique IA ».
6. **Vente de services de création vidéo automatisée :**
   - Avec `hyperframes` ou `Remotion`, un seul prompt permet de générer des vidéos verticales animées (type messages iPhone déroulants ou visualisations de données de cours de bourse). C'est un service vendable à des créateurs de contenu ou entreprises sur les réseaux sociaux.

---

### 4) Chiffres de revenus annoncés

- **Aucun chiffre de revenus n'est mentionné dans la vidéo** (affirmé par l'auteur : *non précisé*). 
- L'auteur mentionne uniquement l'accès à une ressource appelée « *AI Income Database* » (base d'astuces pour générer des revenus avec l'IA) offerte lors de l'inscription à sa newsletter, mais ne cite aucun montant, gain moyen ou chiffre d'affaires.
