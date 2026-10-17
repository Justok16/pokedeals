# 6 mois de Claude Code leçons en 22 minutes

Vidéo : https://youtu.be/33lvXU1BYu8 · durée 21:57 · résumé Gemini (gemini-3.5-flash-lite, lot de 8) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Conseils avancés pour optimiser l'utilisation de Claude Code en gérant rigoureusement le contexte, en désactivant les MCP inutiles et en utilisant des boucles de feedback pour maximiser la qualité des résultats.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Claude Code :** payant (abonnement), assistant de code en ligne de commande.
   - **MCP (Model Context Protocol) Tools (Stripe, Next.js, Supabase, etc.) :** gratuits/payants selon les services, outils externes connectés à Claude.
   - **Supabase CLI, GitHub CLI, Neon CLI, Vercel CLI :** gratuits, outils de ligne de commande pour interagir avec les services.
3) **Astuces concrètes et réutilisables :**
   - Désactiver les MCP (Model Context Protocol) non utilisés pour économiser le contexte de l'IA (qui peuvent consommer 15% à 20% du contexte global).
   - Traiter le fichier `CLAUDE.md` avec soin en y incluant uniquement les informations essentielles, structurées et applicables pour éviter d'encombrer le contexte.
   - Mettre en place des "feedback loops" (boucles de rétroaction) en cas de bug : demander à Claude de corriger son code et de lancer lui-même les requêtes de test (`curl`, `pnpm run dev`) jusqu'à ce que le résultat attendu soit atteint.
4) **Chiffres de revenus annoncés :** non précisé.
