# Anthropic est furieux que la Chine ait fait ce qu'elle a fait.

Vidéo : https://youtu.be/sNCPV-Og9A8 · durée 13:25 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, adapté à votre recherche :

### 1. Idée principale
Anthropic accuse trois entreprises chinoises (DeepSeek, Moonshot, MiniMax) d'avoir mené une campagne coordonnée de « distillation de modèle » en utilisant 24 000 faux comptes, 16 millions d'échanges et des serveurs proxy pour entraîner leurs propres IA sur les capacités de Claude, contournant les interdictions géographiques. L'ironie est qu'Anthropic (et d'autres géants de l'IA) a lui-même entraîné ses modèles en aspirant massivement du contenu sur internet et fait face à des procès pour violation de droits d'auteur (notamment par *The New York Times*, des auteurs, et *Reddit*). Le problème juridique du droit d'auteur et du vol de données dans l'IA reste entier et flou.

---

### 2. Outils, sites ou dépôts GitHub cités
*   **Claude (par Anthropic) :** Modèle d'IA (dont Opus, Haiku, etc.). Payant/Freemium (API et abonnements). Utilisé comme « modèle enseignant » (teacher) pour la distillation.
*   **DeepSeek :** Entreprise/IA chinoise. Modèle concurrent. Utilisé pour la distillation à partir de Claude.
*   **Moonshot AI (Kimi) :** Entreprise/IA chinoise. Modèle concurrent.
*   **MiniMax :** Entreprise/IA chinoise. Modèle concurrent.
*   **OpenAI (ChatGPT / GPT-4 / GPT-5.2) :** Modèle d'IA. Payant. Également visé par des poursuites pour le scraping de données (YouTube, livres, etc.).
*   **xAI (Grok) / Google :** Entreprises et modèles d'IA également impliqués dans le scraping de livres et de données protégées.

---

### 3. Astuces concrètes et réutilisables
*   **La distillation de modèle (Model Distillation) :** Une technique consistant à utiliser les réponses et la « chaîne de pensée » (chain of thought) d'un modèle grand, puissant et coûteux (le « professeur ») pour entraîner un modèle plus petit, plus rapide et moins cher (l'« élève »), sans avoir à ingérer tout l'Internet brut.
*   **Contournement des restrictions géographiques :** Utilisation de faux comptes et de réseaux proxy pour accéder à des services d'IA bloqués ou interdits dans une région (pratique illégale ou contraire aux conditions d'utilisation, mais mise en avant dans le rapport d'Anthropic).

---

### 4. Chiffres de revenus annoncés
*   *Affirmé par l'auteur* (concernant le règlement d'un procès) : **1,5 milliard de dollars** qu'Anthropic a accepté de payer pour régler un recours collectif (class action) intenté par des auteurs pour violation de droits d'auteur, avec environ **3 000 $** par livre pour environ **500 000 livres** concernés.
*   *Coûts d'entraînement d'un grand modèle (affirmé par l'auteur)* : **Des centaines de millions de dollars** (voire des milliards en R&D) pour entraîner des modèles phares sur 90 à 100 jours via des clusters massifs de GPU.
*   *Volume d'échanges de distillation (affirmé par l'auteur d'après le rapport d'Anthropic)* : 
    *   DeepSeek : **Plus de 150 000 échanges**
    *   Moonshot AI : **Plus de 3,4 millions d'échanges**
    *   MiniMax : **Plus de 13 millions d'échanges**
*   *Faux comptes utilisés (affirmé par l'auteur)* : **24 000 faux comptes** (chiffre global mentionné au début).
