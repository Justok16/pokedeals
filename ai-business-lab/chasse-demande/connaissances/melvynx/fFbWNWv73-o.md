# Top 5 des applications macOS pour coder avec l'IA en 2026

Vidéo : https://youtu.be/fFbWNWv73-o · durée 17:32 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur présente sa sélection d'applications macOS et sa configuration matérielle/logicielle optimisée pour le « vibe coding » et le développement assisté par agents IA (tels que Claude Code et Codex). L'objectif est de maximiser la vitesse d'exécution, réduire l'empreinte mémoire/batterie sur Mac et automatiser les tâches répétitives (dictée vocale, compression d'images, lancement de scripts, visualisation rapide de code).

---

### 2) Outils, sites et dépôts GitHub cités

1. **Handy / Parler**
   - **Nom exact / Source :** *Handy* (dépôt GitHub : `cjpais/Handy` / site : `handy.computer`) et son fork *Parler* (dépôt GitHub : `Melynx/Parler`).
   - **Prix :** Gratuit (Open source).
   - **Utilité :** Speech-to-Text fonctionnant en local/hors ligne. Permet de dicter rapidement ses prompts et textes via un raccourci clavier global.

2. **Zed**
   - **Nom exact / Source :** *Zed* (site : `zed.dev`).
   - **Prix :** Gratuit (Open source).
   - **Utilité :** Éditeur de code ultra-rapide et léger écrit en Rust. Utilisé pour afficher instantanément les projets, inspecter les diffs Git et exécuter des agents IA intégrés (*Claude Agent*, *Codex CLI*).

3. **Klack**
   - **Nom exact / Source :** *Klack* (Mac App Store).
   - **Prix :** Payant (~5 $).
   - **Utilité :** Émulateur de sons de clavier mécanique lors de la frappe pour rendre la saisie de prompts et de texte plus satisfaisante.

4. **Raycast**
   - **Nom exact / Source :** *Raycast* (site : `raycast.com`).
   - **Prix :** Gratuit (fonctionnalités IA *Quick AI* accessibles gratuitement ou via abonnement optionnel à ~8 $/mois).
   - **Utilité :** Remplaçant de Spotlight. Gestion de l'historique du presse-papier, sélecteur d'emojis par langage naturel IA, correction instantanée de grammaire/orthographe (avec Gemini Flash), lancement d'applications et de scripts de redimensionnement/capture.

5. **Helium Browser**
   - **Nom exact / Source :** *Helium* (site : `helium.computer` / GitHub : `imputnet/helium`).
   - **Prix :** Gratuit (Open source).
   - **Utilité :** Navigateur web basé sur Chromium, économe en batterie et mémoire vive, doté d'onglets verticaux et d'une vue scindée (*Split View*).

6. **Clop**
   - **Nom exact / Source :** *Clop* (site : `lowtechguys.com/clop` ou via *Setapp*).
   - **Prix :** Payant (~15 $ à l'achat unique, ou inclus dans Setapp ; code source open source disponible).
   - **Utilité :** Compresse et réduit automatiquement le poids des captures d'écran, images et vidéos copiées dans le presse-papier avant de les envoyer aux modèles d'IA.

7. **Setapp**
   - **Nom exact / Source :** *Setapp* (site : `setapp.com`).
   - **Prix :** Payant (abonnement mensuel).
   - **Utilité :** Magasin d'applications macOS par abonnement regroupant divers utilitaires présentés (Clop, CleanMyMac, Vivid pour doubler la luminosité, JoyCast pour filtrer le micro, Presentify pour annoter l'écran, etc.).

8. **Outils IA & Agents de code cités :**
   - **Codex CLI / Codex App :** Payant (mentionné à 200 $/mois) – Agent autonome pour le code.
   - **Claude Code :** Payant (mentionné à 100 $/mois) – Outil CLI d'Anthropic pour coder via l'IA.
   - **Cursor :** Éditeur de code IA (l'auteur indique ne plus l'utiliser pour l'édition de code classique).
   - **Hermes Agent + Telegram :** Agent IA connecté à Telegram.

9. **Sites personnels cités :**
   - `mlv.sh/coding` : Page listant sa stack logicielle IA à jour.
   - `mlv.sh/fa` : Page d'inscription à sa formation gratuite / blueprint pour devenir *AI Engineer*.

---

### 3) Astuces concrètes et réutilisables

- **Accélérer le prompt par la voix :** Configurer un raccourci clavier global (Speech-to-Text local avec Handy/Parler) pour dicter de longs contextes d'un coup aux agents CLI plutôt que de tout taper manuellement.
- **Optimiser la transmission d'images aux LLM :** Utiliser Clop pour réduire la taille des captures d'écran copiées de 50 à 75 % afin d'accélérer l'upload et économiser des tokens / de la bande passante.
- **Changer de paradigme d'IDE :** À l'ère des agents autonomes (Claude Code, Codex), privilégier un visualiseur ultra-léger et rapide à l'ouverture comme Zed plutôt qu'un IDE lourd (VS Code / Cursor), afin d'inspecter les diffs Git en une fraction de seconde.
- **Automatiser la correction et les actions système :** Utiliser Raycast pour corriger instantanément un texte sélectionné (*Fix Spelling and Grammar*) ou requêter rapidement un modèle IA (*Quick AI*) sans changer de fenêtre.

---

### 4) Chiffres de revenus annoncés

- **Revenus générés :** Non précisé (aucun chiffre de gains ou de revenus n'est mentionné dans la vidéo).
- **Coûts d'outils mentionnés (*affirmé par l'auteur*) :** 
  - Abonnement Codex : 200 $/mois.
  - Abonnement Claude Code : 100 $/mois.
  - Abonnement Raycast AI : environ 8 $/mois.
  - Licence Clop : 15 $.
  - Licence Klack : environ 5 $.
