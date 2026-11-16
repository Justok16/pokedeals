# vu3pgbLgaMw — « Arrête de créer des agents IA, fais des skills »

- Auteur : Melvynx ; lien : https://youtu.be/vu3pgbLgaMw
- Envoyée par l'utilisateur ; résumée le 16/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (16/11)

Confirme notre organisation : un seul agent + des skills dans `.claude/skills/` (nouveau-client, etc.). Rien à changer ; guide « ORGANISE » non téléchargé (inutile, déjà appliqué).

## Résumé (Gemini)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
Il faut **arrêter de créer une multitude d’agents IA spécialisés** (un agent pour la comptabilité, un pour le copywriting, un pour les mails, etc.) qui cherchent à communiquer entre eux. Cette approche multi-agents crée de la complexité inutile et des erreurs. 

La méthode recommandée (soutenue par les ingénieurs d'Anthropic) consiste à **utiliser un seul agent central** auquel on fournit une **bibliothèque de compétences (*skills*)** modulaires. L'agent unique charge dynamiquement la compétence nécessaire pour accomplir la tâche demandée.

---

### 2) Outils, sites et ressources cités

1. **Anthropic / Conférence AI Engineer (*"Don't Build Agents, Build Skills Instead"* par Barry Zhang & Mahesh Murag)**
   * **Gratuit / Payant :** Gratuit (conférence/vidéo publique).
   * **À quoi il sert :** Référence scientifique/technique citée dans la vidéo pour démontrer pourquoi l'architecture basée sur des *skills* (compétences) est supérieure à l'architecture multi-agents.

2. **Claude / Arborescence de compétences (`./.claude/skills/`)**
   * **Gratuit / Payant :** Non précisé dans la vidéo (dépend de l'abonnement/API Claude d'Anthropic).
   * **À quoi il sert :** Sert d'agent principal (nommé par exemple *Steve*) qui lit les dossiers de compétences locales (ex: `copywriting/`, `script/`, `apps/`, contenant des fichiers `SKILL.md`) et les exécute à la demande dans le chat.

3. **Site web `mlv.sh/r`**
   * **Gratuit / Payant :** Gratuit.
   * **À quoi il sert :** Permet de télécharger la ressource/guide prêt à copier nommé **« ORGANISE »** pour configurer ce système.

---

### 3) Astuces concrètes et réutilisables

* **Ne multipliez pas les bots :** Évitez les architectures complexes à plusieurs agents (orchestrateur, routeur, vérificateur, etc.) qui génèrent des pertes de temps et des erreurs de transmission.
* **Structurez vos compétences dans des fichiers locaux :** 
  * Créez un répertoire dédié aux compétences (ex: `./.claude/skills/`).
  * Organisez chaque compétence dans son propre dossier (`mails/`, `script/`, `short-editing/`, `sav/`, `whatsapp/`, `instagram/`, etc.) contenant les consignes précises (ex: `SKILL.md`).
* **Invoquez la compétence à la demande :** 
  * Dans une interface de chat unique avec l'agent, tapez simplement votre besoin (ex: *"Fais le copywriting de ma page de vente"*).
  * L'agent va automatiquement détecter et charger le module correspondant (`Skill - copywriting`) pour réaliser la tâche sans lancer de sous-agents inutiles.

---

### 4) Chiffres de revenus annoncés

* **Non précisé** *(aucun chiffre de revenus n'est mentionné directement dans la vidéo)*.
