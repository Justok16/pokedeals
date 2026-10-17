# Traduis une application NextJS en 15 minutes (App Router i18n)

Vidéo : https://youtu.be/C77hQdPxHxs · durée 15:50 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est d'expliquer comment implémenter l'internationalisation (i18n) et la traduction multilingue dans une application Next.js (supportant les composants serveur et client) à l'aide de bibliothèques spécialisées et de l'IA.
2)
- Next Intl : bibliothèque (gratuit/open-source) pour l'i18n dans Next.js (jugée très performante mais légèrement plus complexe).
- Next International : bibliothèque (gratuit/open-source) de type-safe i18n créée par une personne recommandée par l'auteur, gérant les composants serveur et client de manière simple via l'URL.
- ChatGPT / Claude : outils d'IA (freemium) utilisés pour traduire rapidement les fichiers de dictionnaires textuels (en, fr, etc.).
3) Astuces :
- Créer un dossier `locales/` contenant des fichiers séparés pour le client (`client.ts`) et le serveur (`server.ts`), ainsi que des fichiers de traduction par langue (`en.ts`, `fr.ts`).
- Utiliser un middleware pour détecter ou réécrire l'URL en fonction de la langue de l'utilisateur (ex. `/en/` ou `/fr/`).
- Automatiser la traduction des clés textuelles en passant le fichier source à une IA (comme ChatGPT) avec un prompt structuré exigeant le respect strict de la typage et de la syntaxe.
4) Chivres : non précisé.
