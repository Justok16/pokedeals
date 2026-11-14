# J7NstDkNwLE — « Je teste Fable 5.2, le meilleur modèle jamais publié »

- Auteur : Erwan | IA ; lien : https://youtu.be/J7NstDkNwLE
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.6-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Essai comparatif de Fable 5.2 face à Opus 5.5 et à un modèle concurrent, centré sur le coût réel d'une tâche et sur le choix du bon modèle dans Claude Code.

- **Commencer avec Opus 5.5, monter l'effort si besoin, ne passer à Fable 5.2 que si Opus échoue** : idée déjà dans nos consignes (`connaissances/consignes-detaillees.md`, « Modèle à utiliser », conseil du 24/10 : Opus 5.5 moyen au quotidien, Fable élevé pour un site client ; même idée notée le 11/11). Le réglage appartient à l'utilisateur ; rien à changer.
- **Regarder le coût d'une tâche entière, pas le prix au jeton** : utile pour comprendre le quota, déjà couvert par notre règle « économiser le quota » ; nous ne payons rien à la consommation (budget 0 €).
- **Artificial Analysis (comparaison indépendante des modèles)** : en réserve, déjà noté le 11/11 (tri de `videos-resumes/Ib9rUSgIzpI.md`) ; à ressortir seulement s'il faut choisir un modèle pour un service rendu à un client.
- **Retrouver le lieu et l'heure d'une photo puis refaire la scène en 3D (Three.js, OpenStreetMap)** : écarté ; hors sujet pour des sites d'artisans, et retrouver où une photo a été prise touche à la vie privée.
- **Codex et GPT-6 Astra (concurrents, payants), Mythos 5.2 (accès restreint)** : écartés (budget 0 €, aucun besoin).
- **Chiffres cités (coût moyen par tâche de 26,54 $, 10,04 $ et 6,24 $ ; essai à 9,18 $, 15,26 $ et 4,42 $ ; tarifs au million de jetons ; quota de Fable limité à 50 % sur certains forfaits)** : affirmés par l'auteur, non vérifiés. À noter : le tarif d'Opus 5.5 cité ici (4 $ et 20 $) n'est pas le même que dans la vidéo T-iXDsz1XAw (2 $ et 10 $) : aucun des deux n'est retenu.

Conclusion : rien à installer, rien à changer ; la vidéo confirme notre partage des modèles.

## Résumé (Gemini)

Voici le résumé structuré de la vidéo, rédigé pour une personne souhaitant optimiser ses coûts et ses workflows pour créer de la valeur avec l'IA et Claude Code :

---

### 1) Idée principale
La vidéo présente et compare le modèle de frontière **Claude Fable 5.2** d'Anthropic face à **Claude Opus 5.5** et **GPT-6 Astra**. L'auteur analyse les performances agentiques élevées de Fable 5.2 (codage 3D, automatisation, résolution de problèmes complexes) et démontre qu'il existe une différence majeure entre le **coût au token** et le **coût réel à la tâche**. Il explique comment choisir stratégiquement entre Opus 5.5 et Fable 5.2 dans un environnement comme *Claude Code* pour ne pas dilapider son budget API ou son quota d'abonnement.

---

### 2) Outils, sites, modèles et technologies cités

*   **Claude Fable 5.2 (Anthropic)**
    *   *Statut :* Payant (API : 8 $/M-tokens en entrée, 40 $/M-tokens en sortie ; inclus sous forme de quota limité à 50 % sur les forfaits Claude Max/Ultra ; crédits d'usage sur Pro).
    *   *Utilité :* Modèle très puissant conçu pour le raisonnement exigeant, les tâches agentiques à long terme, la robotique et le codage complexe.
*   **Claude Mythos 5.2 (Anthropic)**
    *   *Statut :* Payant / Accès restreint (réservé aux organisations vérifiées).
    *   *Utilité :* Même modèle sous-jacent que Fable 5.2, mais sans les garde-fous stricts publics.
*   **Claude Opus 5.5 (Anthropic)**
    *   *Statut :* Payant (API : 4 $/M-tokens en entrée, 20 $/M-tokens en sortie ; inclus dans les abonnements Claude).
    *   *Utilité :* Modèle quotidien recommandé par Anthropic pour la majorité des tâches de codage et de création.
*   **GPT-6 Astra (OpenAI)**
    *   *Statut :* Payant (via API / Codex).
    *   *Utilité :* Modèle concurrent d'OpenAI évalué lors des benchmarks.
*   **Claude Code (Anthropic)**
    *   *Statut :* Gratuit/Payant selon l'accès API ou abonnement associé.
    *   *Utilité :* Agent de développement en ligne de commande/harnais pour exécuter directement des modèles Claude sur des projets complets.
*   **Codex (OpenAI)**
    *   *Statut :* Payant / Accès API OpenAI.
    *   *Utilité :* Environnement agentique de codage d'OpenAI utilisé pour exécuter GPT-6 Astra.
*   **Artificial Analysis (Site Web)**
    *   *Statut :* Gratuit (consultation).
    *   *Utilité :* Plateforme de benchmarks indépendante mesurant la vitesse, la qualité et le coût réel par tâche des différents modèles d'IA.
*   **Three.js / OpenStreetMap (OSM) / HTML5**
    *   *Statut :* Gratuits / Open Source.
    *   *Utilité :* Technologies web et bases de données géographiques exploitées par les agents IA pour reconstruire des environnements et scènes 3D interactives à partir de simples prompts ou photos.

---

### 3) Astuces concrètes et réutilisables

1.  **Distinguer le "Prix au Token" du "Prix à la Tâche" (Efficacité financière) :**
    *   Fable 5.2 a des tokens moins chers que sa version précédente (5.1), mais comme il effectue un raisonnement plus long et génère beaucoup plus de tokens (ex. 275 M de tokens générés sur un benchmark contre 54 M pour GPT-6 Astra), **une tâche complète sur Fable 5.2 coûte en moyenne 26,54 $**, contre 10,04 $ sur Opus 5.5 et 6,24 $ sur GPT-6 Astra.
2.  **Méthodologie d'escalade recommandée (Économie de crédits) :**
    *   **Étape 1 :** Lancer le projet/code avec **Claude Opus 5.5**.
    *   **Étape 2 :** Si le résultat est insuffisant, augmenter l'effort sur Opus 5.5 en mode `xhigh` ou `max`.
    *   **Étape 3 :** Basculer sur **Claude Fable 5.2** uniquement si Opus 5.5 échoue sur du raisonnement très complexe.
3.  **Capacités d'investigation et création autonome (OSINT + Codage 3D) :**
    *   En injectant une simple image (sans métadonnées EXIF), Claude Code équipé de Fable 5.2 est capable de déterminer la géolocalisation exacte, la date, l'heure et l'angle de prise de vue via des calculs astronomiques/d'ombres, puis de générer automatiquement une application web 3D (Three.js) retranscrivant la scène.

---

### 4) Chiffres de revenus annoncés

*   **Revenus professionnels/gains financiers :** Non précisé (la vidéo ne mentionne aucun chiffre de revenus d'entreprise ou de vente de services).
*   **Données financières et coûts d'usage affirmés par l'auteur / sources :**
    *   *Coût moyen par tâche (Benchmark Artificial Analysis) :*
        *   GPT-6 Astra : **6,24 $**
        *   Claude Opus 5.5 : **10,04 $**
        *   Claude Fable 5.2 : **26,54 $**
    *   *Coût et durée du test à l'aveugle (Reconstruction 3D d'une photo) :*
        *   **Modèle X (Claude Fable 5.2 via Claude Code) :** 9,18 $ (Durée : 21 min 13 s) — *Gagnant du test.*
        *   **Modèle Y (GPT-6 Astra via Codex) :** 15,26 $ (Durée : 40 min 46 s).
        *   **Modèle Z (Claude Opus 5.5 via Claude Code) :** 4,42 $ (Durée : 23 min 55 s).
