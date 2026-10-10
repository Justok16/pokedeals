# "use workflow" de Next.js : la solution ultime pour le server less ?

Vidéo : https://youtu.be/yCT8BnolMZA · durée 16:55 · résumé Gemini (gemini-3.5-flash-lite, lot de 8) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation de la librairie **Workflow** pour rendre les fonctions TypeScript durables et exécuter des workflows asynchrones complexes sur plusieurs heures ou jours avec réessai automatique et observabilité.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Workflow (useworkflow.dev) :** gratuit (modèle de tarification basé sur le stockage et le nombre de steps/exécutions), sert à créer des fonctions durables et des workflows robustes en TypeScript.
   - **Ingest (ingest.cloud) :** gratuit / freemium, utilisé pour exécuter et orchestrer des workflows complexes.
   - **Gemini / GPT :** payant, utilisés pour générer du contenu textuel ou des images dans les workflows.
   - **Vercel :** payant, hébergeur et plateforme d'application.
3) **Astuces concrètes et réutilisables :**
   - Utiliser la directive `use workflow` pour transformer une fonction classique en workflow durable avec gestion automatique des retries et persistance des états.
   - Intégrer des steps (`use step`) pour découper les processus longs et pouvoir debugger ou reprendre chaque étape individuellement.
   - Utiliser des outils d'inspection comme `pnpm dlx workflow-inspector --web` pour suivre et debugger les workflows en local.
4) **Chiffres de revenus annoncés :** non précisé.
