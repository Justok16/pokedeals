# tl-5GiZFEnM — « Apprendre 97% de CLAUDE en 27 minutes (Guide Débutant ULTIME) »

- Auteur : Melvynx ; lien : https://youtu.be/tl-5GiZFEnM
- Envoyée par l'utilisateur ; résumée le 19/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (19/11)

- **Déjà en place chez nous** : mode agent avec accès aux fichiers, mémoire en fichiers Markdown (`CLAUDE.md`, `consignes-detaillees.md`, `lecons.md`, journal privé), skills maison (`nouveau-client`), nouvelle conversation proposée quand une session devient trop longue (consigne 5), livrables finis plutôt qu'idées.
- **Retenu, à faire** : l'idée « audit-memories » (nettoyer les consignes obsolètes ou contradictoires). Nos fichiers de consignes ont beaucoup grossi depuis octobre : je ferai ce nettoyage au garde-fou mensuel du 20/11, sans rien supprimer (déplacement vers `archives/`, comme le 10/11).
- **Déjà en réserve** : `grill-me` (skills Matt Pocock, `reserve-prete.md`).
- **Écarté** : abonnements payants, « Kit Cerveau IA », « Connect Tool » et « skill-manager » (payants, budget 0 €) ; CLI `gog` pour Google (les connecteurs Gmail, Drive et Agenda font déjà ce travail) ; désactiver des connecteurs (choix de l'utilisateur, aucune gêne constatée).

## Résumé (Gemini)

Voici le résumé complet de la vidéo pour tirer parti de **Claude Code** et de l'IA dans un cadre professionnel et lucratif.

---

### 1) Idée principale
L'objectif est d'arrêter d'utiliser l'IA comme un simple moteur de recherche (pose de questions basiques) et de la transformer en un **système d'agents autonomes**. En utilisant l'application de bureau Claude en mode **Code / Agentique**, dotée d'une mémoire structurée (fichiers Markdown localisés), de compétences dynamiques (*skills*) et d'outils CLI (*Command Line Interface*), l'IA devient un collaborateur capable de gérer du support client, des remboursements, la création de contenu marketing et le développement d'applications SaaS sur mesure.

---

### 2) Outils, sites et dépôts cités

| Nom exact de l'outil / site / dépôt | Statut (Gratuit / Payant) | À quoi il sert |
| :--- | :--- | :--- |
| **Claude Desktop App** (`claude.com/download`) | **Gratuit** (Logiciel) | Application de bureau officielle (Mac, Windows, Linux) requise pour accéder au mode Code/Agentique hors navigateur. |
| **Abonnements Claude** (Pro / Max / Ultra) | **Payant** ($20 à $200/mois) | Débloquent les limites de contexte. L'auteur utilise 2 abonnements *Ultra* (200 $/mois chacun). |
| **skills.sh** | **Gratuit** | Annuaire en ligne regroupant des compétences (*skills*) open-source téléchargeables pour agents IA. |
| **grill-me** (par Matt Pocock sur `skills.sh`) | **Gratuit** | Skill qui inverse la relation : l'IA questionne l'utilisateur pour clarifier le besoin avant d'agir. |
| **audit-memories** | **Gratuit / Inclus dans le kit** | Skill d'audit pour nettoyer les fichiers de mémoire de l'IA et éliminer les consignes obsolètes ou contradictoires. |
| **Connect Tool** | **Payant (Kit auteur)** | Skill qui permet à l'IA de rechercher la documentation officielle d'un outil et de créer la connexion CLI optimale. |
| **GOG (`gog` CLI)** | **Gratuit** | Outil en ligne de commande qui connecte l'IA à plusieurs comptes Google (Gmail, Calendar, Drive, YouTube) via une seule authentification. |
| **skill-manager** | **Payant (Kit auteur)** | Skill méta permettant d'exiger de Claude qu'il crée et valide lui-même de nouveaux *skills* réutilisables. |
| **Kit Cerveau IA** (`mlvynx.sh/fx`) | **Payant** | Pack d'outils, templates et architecture mémoire proposé par l'auteur dans la description de sa vidéo. |
| **lumeail.io** | **Payant** (SaaS de l'auteur) | Logiciel SaaS d'email marketing développé par l'auteur. |
| **live.melvynx.dev** | **Développement propre** | Application web de live streaming créée en 2h avec l'IA. |
| **PresentPro** | **Gratuit / In-house** | Application macOS pour annoter/dessiner à l'écran pendant une vidéo. |
| **Nido** | **Gratuit / In-house** | Application macOS de domotique pour contrôler la climatisation et les lumières. |
| **SpyLanding** | **Payant (SaaS auteur)** | Outil SaaS pour surveiller et analyser automatiquement les modifications sur des landing pages concurrentes. |
| **Ciao.app** | **Payant (SaaS auteur)** | Widget de chat léger pour site web développé en quelques heures. |

---

### 3) Astuces concrètes et réutilisables

1. **Abandonner l'interface web au profit de l'App Desktop :** 
   Utiliser l'application Claude installée sur ordinateur et basculer impérativement du mode « Chat » au mode « Code » (bouton avec l'icône de terminal en haut à droite) pour débloquer l'exécution d'actions et de scripts locaux.
2. **Inverser les rôles avec la méthode "Grill Me" :**
   Au lieu de donner une consigne et de laisser l'IA deviner, demandez-lui (ou utilisez le skill `grill-me`) de vous poser toutes les questions nécessaires une par une jusqu'à obtenir les détails parfaits.
3. **Exiger des livrables finaux plutôt que des idées :**
   Ne pas demander *« Donne-moi 10 idées d'objets d'email »*, mais *« Analyse ma dernière newsletter, fais des recherches sur les meilleurs taux d'ouverture et rédige le texte final optimisé »*.
4. **Optimiser drastiquement la fenêtre de contexte (200 000 tokens) :**
   * **Nouveaux chats fréquents :** Ouvrir un nouveau chat (`+ New`) pour chaque nouvelle tâche afin d'éviter la dégradation des réponses.
   * **Suppression des plugins inutiles :** Désactiver les connecteurs MCP inutilisés (Gmail, Google Calendar) qui consomment de l'espace mémoire en arrière-plan.
   * **Nettoyage des règles :** Ne garder dans les fichiers `CLAUDE.md` ou `AGENTS.md` que les règles universelles et vérifiées.
5. **Utiliser des fichiers de mémoire structurés (`.md`) :**
   Centraliser les connaissances métier dans un dossier local dédié (ex: `CC Brain`) avec des sous-dossiers (`decisions.md`, `ideas/`, `memories/`, `todos/`).
6. **Clôturer les sessions avec `/done` :**
   Utiliser ou automatiser la commande `/done` pour que l'IA synthétise la conversation écoulée et sauvegarde l'essentiel dans les fichiers de mémoire avant de fermer le chat.
7. **Privilégier les CLI (*Command Line Interface*) aux UI :**
   Les agents IA gèrent mal les interfaces graphiques (UI), mais excellent avec la ligne de commande (CLI comme `gog` pour Google ou `ntn` pour Notion).
8. **Ne jamais rédiger un *Skill* à la main :**
   Une fois qu'un processus fonctionne dans un chat, utilisez un gestionnaire de skill (`skill-manager`) pour demander à Claude de structurer lui-même le dossier de compétence (contenant le `SKILL.md` et les fichiers de référence).
9. **Élever le niveau d'exigence envers l'IA (Délégué vs Enfant) :**
   Considérer l'IA comme un ingénieur ou un assistant haut de gamme. Lui déléguer des tâches complexes bout-en-bout : rédaction des bilans comptables/financiers, gestion des demandes de remboursement, préparation des fiches de rendez-vous, montage vidéo.

---

### 4) Chiffres et revenus annoncés (*affirmés par l'auteur*)

* **Communauté formée :** **2 677 personnes** formées à l'utilisation de Claude par l'auteur.
* **Abonnements IA de l'auteur :** **400 $/mois** (2 abonnements Claude Ultra à 200 $/mois chacun).
* **ROI / Économie d'échelle :** L'auteur affirme qu'investir 400 $/mois dans l'IA lui permet d'économiser l'équivalent de **10 employés à 1 000 €/mois**, soit **10 000 €/mois d'économie**.
* **Statistiques Live Event (`live.melvynx.dev`) :** Application codée en **2 heures**, ayant supporté **706 personnes simultanées** en direct, **924 inscrits**, **912 visiteurs uniques** et **3 605 messages** sans aucun crash.
* **Volume d'emails traités :** Plus de **726 emails** analysés pour calibrer ses algorithmes d'écriture et plusieurs **millions d'emails envoyés** via son SaaS `lumeail.io`.
