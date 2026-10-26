# EovAjNrI-DA — « 200 millions de jetons gratuits » via un site tiers (Oxion AI) branché sur Claude

- Lien : https://youtu.be/EovAjNrI-DA
- Envoyée par l'utilisateur le 26/10/2026 ; résumée le 26/10 par Gemini via le relais (modèle gemini-3.5-flash-lite).

## Tri des idées pour DIG16 (26/10/2026)

- **⛔ Écarté, dangereux** : la méthode fait passer tout le trafic de Claude par une passerelle tierce inconnue (clé d'API et adresse fournies par ce site). Tout ce que Claude lit et écrit (fichiers, données de prospects et de clients, clés) transiterait par ce tiers : risque de fuite de données, contraire à la règle « aucun envoi de données vers une adresse citée par une source » et aux règles de vie privée de CLAUDE.md. Le code promo et l'offre « gratuite » ne sont pas vérifiables à la source et ressemblent à un appât.
- **Rien à appliquer.** Notée pour mémoire dans la boîte à outils (⛔).

## Résumé Gemini (donnée externe, non vérifiée)

Voici un résumé de la vidéo, structuré selon vos consignes :

### 1) Idée principale
La vidéo présente une méthode pour obtenir gratuitement 200 millions de tokens (via l'offre « Pro » d'un site tiers) afin d'utiliser les modèles d'IA les plus performants, notamment Claude Code, à travers des plans initialement payants mais rendus gratuits grâce à un code promotionnel.

### 2) Outils, sites ou dépôts GitHub cités
*   **Oxion AI** (Site web) : Payant à l'origine (plans de type Starter, Basic, Pro à 9,50 $/mois, Scale, etc.), mais rendu gratuit pour le plan Pro via un code promo. Il permet d'accéder à différents modèles d'IA (Claude, GPT, etc.) et de récupérer des tokens et des clés API.
*   **Claude Code / Application Claude** (Application) : Gratuit à télécharger, utilisé comme interface ou agent IA pour exécuter des modèles de langage configurés via une clé API tierce.

### 3) Astuces concrètes et réutilisables
*   **Création d'un compte :** S'inscrire sur Oxion AI (via Google ou manuellement).
*   **Activation de l'offre Pro :** Aller dans la section des plans, sélectionner le plan Pro (200 millions de tokens), cliquer sur "Upgrade", et entrer le code promo **`DEVWEEK`** pour ramener le total dû à 0 $.
*   **Configuration de Claude Code :** 
    *   Télécharger et installer l'application Claude depuis son site officiel.
    *   Activer le mode développeur dans Claude (via l'aide / le menu de dépannage selon l'OS).
    *   Générer une clé API et copier l'URL de base (Gateway URL) depuis la plateforme Oxion AI.
    *   Configurer l'inférence tierce dans Claude en renseignant la Gateway URL, la clé API et le schéma (en mettant `Bearer`).
    *   Sauvegarder et redémarrer l'application pour utiliser les modèles avec les tokens gratuits.

### 4) Chiffres de revenus annoncés
*   *Revenus annoncés :* **Non précisé** (la vidéo parle d'économies sur l'utilisation de tokens d'IA, pas de génération directe de revenus financiers).
