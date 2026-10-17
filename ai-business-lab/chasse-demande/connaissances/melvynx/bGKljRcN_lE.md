# ARRÊTE LES MCP : Voici ce qu'il faut utiliser MAINTENANT

Vidéo : https://youtu.be/bGKljRcN_lE · durée 30:22 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé détaillé de la vidéo, structuré selon vos demandes :

---

### 1) Idée principale
L'auteur affirme que les **MCP (Model Context Protocol)** sont obsolètes car trop lourds : ils s'exécutent en tâche de fond (processus NPM consommateurs de RAM) et surchargent inutilement la fenêtre de contexte de l'IA dès le début de chaque conversation. 

Sa solution consiste à remplacer les MCP par des **CLI (interfaces en ligne de commande)** exécutées via l'outil universel **Bash**, associées à des **Skills** (fichiers de consignes légers au format Markdown). Grâce à ce système, l'agent IA (comme *Claude Code*) ne charge les instructions détaillées dans son contexte que lorsqu'il en a réellement besoin, ce qui économise des milliers de tokens, accélère le traitement et permet d'enchaîner des workflows complexes multi-outils.

---

### 2) Outils, sites et dépôts GitHub cités

1. **Claude Code / Claude (Anthropic)**
   - **Nom exact :** Claude Code / Anthropic Claude
   - **Gratuit / Payant :** Payant (Abonnement Claude / souscription Anthropic requis).
   - **Usage :** Agent IA en terminal qui exécute du code, gère les fichiers et lance des commandes Bash.

2. **Context7**
   - **Nom exact :** Context7 (`context7.com` / `ctx7`)
   - **Gratuit / Payant :** Gratuit (inscription gratuite sans carte bancaire) avec offres payantes.
   - **Usage :** Fournit à l'IA la documentation et les exemples de code les plus récents pour les bibliothèques et frameworks.

3. **api2cli**
   - **Nom exact :** api2cli (`api2cli.dev`)
   - **Gratuit / Payant :** Non précisé (projet open-source créé par l'auteur lors d'un hackathon).
   - **Usage :** Registre open-source et générateur qui transforme n'importe quelle API (OpenAPI/Swagger) en CLI et en Skill prêts pour les agents IA.

4. **Dub CLI**
   - **Nom exact :** Dub CLI (`dub-cli` / `dub.co`)
   - **Gratuit / Payant :** Non précisé.
   - **Usage :** Service de raccourcissement de liens et d'analyse de clics.

5. **Typefully CLI**
   - **Nom exact :** Typefully CLI (`typefully-cli`)
   - **Gratuit / Payant :** Non précisé.
   - **Usage :** Création, rédaction et planification de tweets / publications sur les réseaux sociaux.

6. **Lumeil CLI**
   - **Nom exact :** Lumeil CLI (`lumeil-cli`)
   - **Gratuit / Payant :** Non précisé.
   - **Usage :** Outil de gestion d'email marketing (envoi de campagnes, gestion des abonnés et des styles de rédaction).

7. **Codeline CLI**
   - **Nom exact :** Codeline CLI (`codeline-cli`)
   - **Gratuit / Payant :** Non précisé.
   - **Usage :** Gestion de plateforme e-learning (création de coupons de réduction, gestion des formations et produits).

8. **Gemini CLI**
   - **Nom exact :** Gemini CLI (`gemini-cli`)
   - **Gratuit / Payant :** Non précisé (utilise l'API Google Gemini).
   - **Usage :** Génération d'images (models Nano Banana, Imagen) et de texte via l'API Gemini.

9. **Exa**
   - **Nom exact :** Exa (`exa`)
   - **Gratuit / Payant :** Non précisé.
   - **Usage :** Moteur de recherche web optimisé pour les agents IA.

10. **Zed**
    - **Nom exact :** Zed (`zed.dev`)
    - **Gratuit / Payant :** Gratuit (Open-source).
    - **Usage :** Éditeur de code léger et ultra-rapide utilisé par l'auteur.

11. **OpenClaw**
    - **Nom exact :** OpenClaw
    - **Gratuit / Payant :** Non précisé.
    - **Usage :** Dépôt/environnement personnel de l'auteur pour synchroniser ses agents, scripts et Skills entre ses machines (VPS/Mac).

12. **Stripe**
    - **Nom exact :** Stripe
    - **Gratuit / Payant :** Non précisé.
    - **Usage :** API de traitement de paiements en ligne.

13. **Linear**
    - **Nom exact :** Linear
    - **Gratuit / Payant :** Non précisé.
    - **Usage :** Gestion de tickets et suivi de projet.

14. **GitHub**
    - **Nom exact :** GitHub
    - **Gratuit / Payant :** Gratuit / Freemium.
    - **Usage :** Hébergement de code et gestion des dépôts.

15. **ChatGPT (OpenAI)**
    - **Nom exact :** ChatGPT
    - **Gratuit / Payant :** Freemium.
    - **Usage :** Montré brièvement pour illustrer la connaissance native d'un modèle sans recherche web.

16. **Outils secondaires mentionnés dans les démonstrations :**
    - **PostHog** (Analytics) : Non précisé.
    - **Cloudflare** (Gestion DNS/sécurité) : Non précisé.
    - **Shadcn/UI & Next.js devtools** (Développement web) : Gratuit / Open-source.

---

### 3) Astuces concrètes et réutilisables

* **Abandonner les serveurs MCP permanents :** Au lieu d'installer des MCP qui tournent en arrière-plan et consomment de la mémoire, donnez simplement à l'agent IA la permission d'exécuter des commandes **Bash**.
* **Utiliser le système de Skills ("Load on demand") :**
  Créez de petits fichiers Markdown (`SKILL.md`) contenant une courte description de vos outils. L'agent IA lit uniquement la description au départ. Il ne télécharge le fichier complet de consignes que s'il doit effectuer la tâche correspondante.
* **Filtrer et tronquer les sorties de commandes (Pipe Bash) :**
  Pour éviter de saturer la fenêtre de contexte de l'IA quand une commande renvoie trop de texte, demandez à l'IA d'utiliser des filtres Unix comme `head -n 50`, `head -c 150` ou le drapeau `--json` dans les CLI.
* **Générer des CLI automatiquement à partir d'une API :**
  À l'aide d'un outil comme `api2cli` et de `Claude Code`, vous pouvez demander à l'IA de lire la documentation Swagger/OpenAPI d'un service et de vous scaffolder automatiquement une CLI personnalisée en quelques secondes.
* **Créer des workflows multi-étapes automatisés :**
  Vous pouvez demander à l'agent d'enchaîner plusieurs CLI en une seule instruction. *Exemple de la vidéo :* Créer un coupon de réduction sur Codeline $\rightarrow$ Générer un lien court personnalisé avec Dub $\rightarrow$ Rédiger et planifier une newsletter avec Lumeil $\rightarrow$ Programmer un tweet sur Typefully.

---

### 4) Chiffres de revenus

* **Revenus financiers :** Non précisé (aucun chiffre d'affaires ou revenu financier direct en € ou $ n'est mentionné par l'auteur dans la vidéo).
* **Volumétrie mentionnée par l'auteur :** L'auteur montre à l'écran une base de **29 000 abonnés actifs** sur sa liste email lors de la démonstration de l'outil Lumeil (*affirmé par l'auteur*).
