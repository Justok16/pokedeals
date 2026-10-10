# Utilise cette Statusline ou SUPPRIME Claude Code (sérieux)

Vidéo : https://youtu.be/CgxOnY-RIlo · durée 11:07 · résumé Gemini (gemini-3.5-flash-lite, lot de 7) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation de la création d'une ligne d'état (« statuline ») sur mesure pour Claude Code dans le terminal, permettant de suivre précisément la consommation de tokens, les limites d'utilisation, le contexte et d'autres paramètres pour optimiser son code.

2) **Outils, sites ou dépôts GitHub cités :**
* **Claude Code** (payant) : outil en ligne de commande d'Anthropic.
* **GitHub** (gratuit) : plateforme de gestion de code.
* **mlv.sh/ai** (gratuit/payant) : site de l'auteur proposant le setup complet et la formation sur Claude Code.

3) **Astuces concrètes et réutilisables :**
* Créer un script de statuline personnalisé (`index.ts`) qui affiche l'utilisation des tokens du contexte (avec seuil d'alerte et auto-compactage à l'approche de 99%).
* Récupérer et parser le fichier `transcript.json` de Claude Code pour calculer précisément la longueur du contexte et le coût de la session.
* Utiliser les limites d'utilisation (`usageLimits`) pour suivre le temps restant avant le reset des quotas (ex: limites sur 5 heures ou 7 jours) et éviter de saturer son quota d'API.
* Configurer l'affichage de la barre de progression en mode `progressive` pour un retour visuel minimaliste et efficace dans le terminal.

4) **Chiffres de revenus annoncés, marqués « affirmé par l'auteur » :**
* Non précisé (l'auteur mentionne un coût de plan max à **200 $ / mois** pour l'utilisation intensive de Claude Code, affirmé par l'auteur).

---
