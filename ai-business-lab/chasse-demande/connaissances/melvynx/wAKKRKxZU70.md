# Ça change tout : OpenClaw ne va plus supporter tes tokens Claude Code

Vidéo : https://youtu.be/wAKKRKxZU70 · durée 11:35 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
Anthropic a mis à jour sa politique concernant les outils tiers (tels qu'OpenClaw) : il n'est désormais plus possible d'utiliser directement les quotas des abonnements Claude (ex. Claude Code / Max) via des interfaces non officielles sans activer le crédit payant (« Extra Usage » / facturation API). La vidéo détaille l'impact de ce changement, comment réclamer les crédits de compensation offerts par Anthropic, les solutions de contournement techniques (utilisation du CLI local) et les alternatives économiques (GLM, MiniMax).

---

### 2) Outils, sites et dépôts cités

* **Claude / Claude Code / Claude Co-work (Anthropic)** : *Payant* (abonnement à environ 200 $/mois ou crédits d'usage à la consommation). Écosystème officiel d'assistants IA et CLI d'Anthropic pour le développement.
* **OpenClaw** : *Gratuit / Open-source* (nécessite des crédits d'API ou une configuration de modèle). Outil d'automatisation et d'orchestration d'agents IA.
* **T3 Code (par Theo)** : *Gratuit / Open-source* (*coût exact du projet : non précisé*). Wrapper/CLI local utilisant le SDK Agent officiel de Claude (confirmé comme autorisé et sûr par Anthropic).
* **Z.ai / GLM Coding Plan** : *Payant* (plans Lite à 10 $/mois, Pro à 30 $/mois, Max à 80 $/mois). Fournisseur de modèles IA (GLM-4 / GLM-5) alternatifs et compatibles avec OpenClaw / Claude Code.
* **MiniMax (Token / Coding Plan)** : *Payant* (Starter à 10 $/mois, Plus à 40 $/mois, Max à 80 $/mois, Ultra à 150 $/mois). Plateforme fournissant des modèles IA alternatifs pour le code.
* **Hetzner** : *Payant*. Hébergeur de serveurs VPS économiques utilisé pour faire tourner des instances d'agents IA.
* **Telegram** : *Gratuit*. Messagerie utilisée comme interface de chat pour interagir avec le bot OpenClaw.
* **`mlv.sh/fo` / Codeline.app** : *Gratuit* (formation promotionnelle). Plateforme de l'auteur proposant un script d'installation automatisée pour configurer OpenClaw et un bot Telegram sur un VPS.

---

### 3) Astuces concrètes et réutilisables

1. **Réclamer le crédit offert par Anthropic :** Dans les paramètres de l'application Claude (`Settings` > `Usage`), cliquer sur le bouton *« Claim your credit »* pour récupérer un crédit gratuit équivalent au prix mensuel de votre abonnement (ex. 200 $).
2. **Profiter des remises sur l'« Extra Usage » :** Pour continuer à utiliser des outils tiers via l'API officielle, Anthropic propose des packs dégressifs (jusqu'à 30 % de réduction, par exemple 1 000 $ de crédits facturés 700 $).
3. **Connecter OpenClaw via le backend Claude CLI local :** Configurer OpenClaw pour qu'il invoque directement l'exécutable local `claude` (`claude-cli`) plutôt que l'API distante. Cela permet de réutiliser la session authentifiée locale liée à votre abonnement.
4. **Utiliser des plans de modèles tiers économiques :** En cas de blocage, intégrer des fournisseurs tiers spécialisés dans le code (comme les forfaits GLM à 10 $/mois) directement dans OpenClaw pour réduire les coûts d'inférence.

---

### 4) Chiffres de revenus annoncés
* **Gains / Revenus financiers générés :** *Non précisé* (la vidéo traite uniquement de la gestion des coûts, des crédits d'API et des abonnements).
* **Crédits et coûts évoqués (*affirmé par l'auteur*) :**
  * Abonnement Claude Code : **200 $/mois**.
  * Crédit de transition récupéré : **200 $** (l'auteur affirme avoir réussi à réclamer deux fois ce crédit via un bug d'affichage, montant sa balance à **445 $**).
  * Remise pack de crédits Anthropic : **300 $ d'économie** pour un pack de 1 000 $ (coût : **700 $**).
  * Alternative GLM Lite : **10 $/mois** pour environ 3× plus d'usage que l'offre de base.
  * Alternative MiniMax Starter : **10 $/mois** pour 1 500 requêtes toutes les 5 heures.
