# T-iXDsz1XAw — « Mythos et Fable 5.2 : Claude devient de la science-fiction ? »

- Auteur : Alexis FH ; lien : https://youtu.be/T-iXDsz1XAw
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Vidéo d'actualité : annonce des modèles Claude Fable 5.2 et Mythos 5.2, comparaison avec les concurrents, entrée en bourse annoncée d'Anthropic, et un conseil de partage du travail entre modèles pour dépenser moins.

- **Fable pour le plan, Opus 5.5 pour l'exécution, Sonnet ou Haiku pour les sous-agents** : déjà en place (`connaissances/consignes-detaillees.md`, « Modèle à utiliser », conseil du 24/10 ; sous-agents avec le modèle choisi, notés « déjà en place » dans `connaissances/boite-a-outils-catalogue.md`, vidéo UcvD53jqHRU). Le réglage appartient à l'utilisateur.
- **Artificial Analysis (comparaison indépendante des modèles)** : en réserve, déjà noté le 11/11 (tri de `videos-resumes/Ib9rUSgIzpI.md`) ; à ressortir seulement s'il faut choisir un modèle pour un service rendu à un client.
- **Se méfier des comparatifs publiés par les fabricants eux-mêmes** : c'est notre règle « vérifier à la source » (toute affirmation revérifiée avant d'être retenue).
- **Mythos 5.2 (accès restreint), Lean (preuves mathématiques), robotique, jeux fabriqués en un passage** : écartés, hors sujet pour des sites d'artisans.
- **Entrée en bourse d'Anthropic, valorisation, salariés millionnaires** : écarté ; sujet de finance, hors de l'entreprise (décision du 01/11).
- **Compte X cité par l'auteur** : écarté, simple source de l'auteur, rien à en tirer pour DIG16.
- **Tarifs des modèles (8 $ et 40 $, 2 $ et 10 $ par million de jetons), durées et coûts des démonstrations (30 heures, 8 jours, environ 550 $), valorisation de 1 500 à 2 000 milliards de dollars** : affirmés par l'auteur, non vérifiés ; aucun achat (budget 0 €).

Conclusion : rien à installer, rien à changer ; le seul conseil utile (partager le travail entre modèles) est déjà dans nos consignes.

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo, structuré pour répondre aux besoins d'un créateur ou entrepreneur cherchant à optimiser ses workflows et ses coûts avec l'IA.

---

### 1) Idée principale
Anthropic vient d'annoncer ses nouveaux modèles **Claude Fable 5.2** et **Mythos 5.2**. La vidéo décrypte leurs performances (codage, mathématiques, biologie, robotique), explique la guerre commerciale et les benchmarks des grands acteurs d'IA (Anthropic, OpenAI, Google), et détaille les enjeux financiers de la prochaine entrée en bourse (IPO) d'Anthropic. Elle présente également **une stratégie concrète d'architecture multi-agents** pour réduire drastiquement ses coûts API tout en maximisant la puissance de calcul lors du développement d'applications ou de projets d'IA.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude / Anthropic (Plateforme & API)**
    *   *Statut :* Payant (selon modèle et utilisation API).
    *   *Rôle :* Écosystème de modèles d'IA pour le texte, l'analyse, la planification et le code.
*   **Claude Fable 5.2**
    *   *Statut :* Payant ($8 / M tokens entrée, $40 / M tokens sortie).
    *   *Rôle :* Le modèle « haut haut de gamme » d'Anthropic. Très puissant, conçu pour le raisonnement complexe, la planification de haut niveau, l'organisation globale de projets et le contrôle robotique.
*   **Claude Mythos 5.2**
    *   *Statut :* Payant (accès sur demande / restreint).
    *   *Rôle :* Identique à Fable 5.2 en termes de puissance, mais **sans aucun garde-fou de sécurité**. Réservé à la recherche poussée (biologie, cybersécurité sensible).
*   **Claude Opus 5.5**
    *   *Statut :* Payant ($2 / M tokens entrée, $10 / M tokens sortie).
    *   *Rôle :* Le modèle recommandé pour l'exécution quotidienne du travail (rédaction, codage standard). Très performant et 4 fois moins cher que Fable 5.2.
*   **Claude Sonnet & Haiku**
    *   *Statut :* Payant (modèles à bas coût).
    *   *Rôle :* Modèles légers idéaux pour faire tourner des sous-agents sur des tâches répétitives à faible coût.
*   **Lean (Langage de programmation)**
    *   *Statut :* Gratuit / Open-source.
    *   *Rôle :* Langage informatique d'assistant de preuve mathématique, utilisé par les agents IA pour formaliser des théorèmes.
*   **Artificial Analysis Index (AA Index / AA Briefcase)**
    *   *Statut :* Gratuit / Plateforme d'analyse.
    *   *Rôle :* Benchmark indépendant et consolidé évaluant les performances réelles des LLM sur diverses tâches (code, travail documentaire CSV/PDF, etc.).
*   **Compte X `@Frenchie`**
    *   *Statut :* Gratuit.
    *   *Rôle :* Compte X francophone cité pour sa synthèse des cas d'usage avancés de Fable 5.2.
*   **Grok 4.8 / Gemini 4 Carbon / GPT-6.2 / DeepSeek V4**
    *   *Statut :* Payant / Variable (non détaillé).
    *   *Rôle :* Modèles d'IA concurrents comparés dans les tableaux de prix et de performances.
*   **Dépôts GitHub cités :** *Aucun dépôt GitHub spécifique n'est mentionné dans la vidéo.*

---

### 3) Astuces concrètes et réutilisables

*   **Stratégie Multi-Agents pour économiser sur l'API Claude :**
    1.  **Le « Cerveau » (Planification / Architecture) :** Utilisez **Fable 5.2** uniquement au début pour planifier, concevoir l'architecture globale ou utiliser la commande `/goal`.
    2.  **L'« Exécuteur principal » (Code & Rédaction) :** Passez sur **Opus 5.5** pour l'écriture effective du code et des livrables. Il est nettement moins cher ($2/$10 au lieu de $8/$40) tout en restant extrêmement capable.
    3.  **Les « Sous-agents » (Tâches secondaires) :** Définissez dans vos réglages de projet que les sous-agents (tâches autonomes isolées) doivent utiliser **Sonnet** ou **Haiku** pour exécuter les petites tâches sans faire exploser votre facture.
*   **Méthode de décodage des Benchmarks (« Cherry Picking ») :**
    *   Ne vous fiez pas aux tableaux présentés par les laboratoires (Anthropic ou Google choisissent les tests qui les placent en tête).
    *   Consultez des indices neutres comme l'**Artificial Analysis Index (AA Index)** et regardez spécifiquement les sous-benchmarks adaptés à votre besoin (*TerminalBench* pour le terminal/code, *AA Briefcase* pour la bureautique/CSV/PDF).
*   **Prototypage rapide de logiciels/jeux par prompt :**
    *   Profitez de la capacité de Fable 5.2 à générer du code complexe en un seul passage (ex: création d'un jeu FPS 3D fonctionnel en HTML/JS pour navigateur ou génération d'œuvres d'art visuelles simulées par des scripts Python).

---

### 4) Chiffres de revenus et données financières annoncés
*(Toutes les données ci-dessous sont énoncées et affirmées par l'auteur de la vidéo)*

*   **Coûts des API Anthropic (affirmé par l'auteur) :**
    *   *Claude Fable 5.2 :* 8 $ / million de tokens en entrée | 40 $ / million de tokens en sortie.
    *   *Claude Opus 5.5 :* 2 $ / million de tokens en entrée | 10 $ / million de tokens en sortie.
*   **Performances de projets réalisés par IA (affirmé par l'auteur) :**
    *   *Formalisation du théorème de Fermat :* Réalisée par 1 000 agents IA en **30 heures** (un travail humain estimé normalement à des semaines ou des mois).
    *   *Reconstruction d'un OS type Windows :* Réalisée par 1 000 agents IA en **8 jours** pour un coût de compute (non précisé).
    *   *Génération d'une peinture par code Python :* 700 000 coups de pinceau simulés pour environ **550 $** de coût de calcul.
    *   *Score en robotique (RoboDojo) :* Passage d'un score de 30-40 % (anciens modèles) à près de **65 %** pour Fable 5.2.
*   **Valorisation d'Anthropic & IPO (affirmé par l'auteur) :**
    *   Valorisation estimée de l'entreprise lors de son entrée en bourse : **entre 1 500 et 2 000 milliards de dollars**.
    *   L'IPO créerait environ **4 250 millionnaires** parmi les employés d'Anthropic, répartis comme suit :
        *   **50 employés :** fortune supérieure à **100 millions de dollars**.
        *   **1 200 employés :** fortune située entre **10 et 99 millions de dollars**.
        *   **3 000 employés :** fortune située entre **1 et 9 millions de dollars**.
*   *Revenus personnels générés directement par l'auteur dans la vidéo :* **Non précisé** (la vidéo traite de l'actualité tech et d'architecture d'IA).
