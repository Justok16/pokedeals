# GITHUB COPILOT Complètement Expliqué

Vidéo : https://youtu.be/g3MrfPY4Iog · durée 14:12 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Comprendre comment fonctionne GitHub Copilot en arrière-plan (architecture, communication avec VS Code et OpenAI, sélection et filtrage du contexte, gestion des snippets) pour mieux l'utiliser.
2) **Outils, sites ou dépôts GitHub cités :**
   - **GitHub Copilot** (payant, outil d'autocomplétion de code par IA)
   - **VS Code** (gratuit, éditeur de code source)
   - **OpenAI** (API, fournisseur des modèles de langage sous-jacents)
   - **Console Ninja** (gratuit/freemium, extension VS Code pour afficher les logs)
3) **Astuces concrètes et réutilisables :**
   - **Garder plusieurs onglets ouverts et bien nommer ses fichiers :** Copilot analyse non seulement le fichier actif, mais aussi les onglets ouverts dans l'éditeur (via le *snipping*) pour comprendre le contexte global du projet (chemins, technologies, structure monorepo).
   - **Structurer son code de manière claire :** Comme l'IA est limitée en contexte et privilégie le code situé au-dessus et au-dessous du curseur, avoir des fichiers bien découpés aide le modèle à générer des suggestions pertinentes.
   - **Créer des types génériques et utiliser le typage TypeScript rigoureux** pour éviter que Copilot ne se trompe dans les types de retours ou de paramètres.
4) **Chiffres de revenus annoncés :**
   - Non précisé.
