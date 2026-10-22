# Modéliser en 3D avec l'IA : mes tests en direct ! — Coben (direct de 3 h 17, animé par un remplaçant, Jean Philamand)

- Lien : https://youtu.be/golzvOVmXB4
- Méthode : transcription automatique (vidIQ, 5 crédits) résumée en deux parties par le relais Gemini, le 02/10/2026 ; Gemini ne lisait pas la vidéo directement (réponses vides sur chaque morceau)
- Affirmations de l'auteur, non vérifiées

## Partie 1/2 (modèle gemini-3.1-flash-lite)

Voici un résumé structuré de la première partie du direct de la chaîne Coben sur la modélisation 3D assistée par IA.

### 1. Outils testés
L'auteur teste plusieurs solutions d'IA et de logiciels de modélisation :
*   **Logiciels de CAO/DAO :**
    *   **FreeCAD (Gratuit) :** Logiciel de conception paramétrique. L'auteur souligne sa force : un interpréteur de code Python intégré qui permet à l'IA de générer et d'exécuter des scripts de modélisation.
    *   **CADQuery (Gratuit) :** Interpréteur de code pur pour la modélisation.
    *   **ForgeCAD (Gratuit/Freemium) :** Outil web exceptionnel selon l'auteur pour modifier des paramètres (ex: diamètre) sur des modèles existants.
*   **Modèles d'IA et agrégateurs :**
    *   **Chat GPT (versions Astra/6) et Claude (Opus/Fable 5.1) :** Utilisés pour la génération de code et la prise de contrôle via des "connecteurs MCP" (passerelles permettant à l'IA de piloter directement le logiciel).
    *   **Tripo :** Utilisé pour la génération de modèles 3D organiques.
    *   **Plateforme agrégatrice française (non nommée, évoquée comme "Moon") :** Permet d'accéder à 80 modèles différents avec une fonction de "mode agent" pour choisir automatiquement l'IA la plus adaptée.
*   **Qualité constatée :** L'IA produit des résultats très propres pour le paramétrique (côtes précises) et l'organique, mais avec une gestion parfois complexe de la topologie des maillages (nécessite souvent une retopologie).

### 2. Astuces concrètes
*   **Stratégie de communication :** L'auteur recommande de ne jamais rester vague. Il conseille de structurer le prompt ainsi : « Si tu as des questions, pose-les-moi avant de lancer la modélisation et n'invente rien. »
*   **Aide au diagnostic :** En cas d'erreur de code ou de problème sur une pièce, l'auteur conseille de prendre une capture d'écran du logiciel (ex: FreeCAD ou Slicer) et de la soumettre à l'IA pour qu'elle identifie précisément où appliquer la correction.
*   **Gestion des quotas :** L'auteur insiste sur la consommation élevée des crédits. Il préconise d'utiliser les modèles "légers" (type "moyen") pour les tâches simples et de réserver les modèles "très élevés" (type Astra/Opus) uniquement pour les étapes de conception complexes.
*   **Utilisation du micro :** L'auteur préfère dicter ses instructions par la voix plutôt que d'utiliser le clavier pour fluidifier le processus.

### 3. Limites et échecs constatés
*   **Hallucinations :** L'auteur prévient que plus la conversation s'étire pour corriger un modèle, plus l'IA a tendance à "halluciner" pour tenter de satisfaire l'utilisateur, ce qui dégrade la qualité géométrique.
*   **Besoin de compétences techniques :** L'auteur affirme qu'il est illusoire de réussir une modélisation complexe sans bagage technique minimal (CAO, mécanique, impression 3D). L'IA n'est pas un substitut au savoir-faire, mais une extension.
*   **Problèmes de connectivité :** Des échecs de communication entre l'IA et les logiciels locaux sont fréquents et nécessitent des ajustements de protocole.

### 4. Chiffres et prix
*   **Abonnements :** L'auteur mentionne des coûts d'abonnement aux IA allant de **20 € à 500 € par mois** selon le niveau d'utilisation et l'accès aux modèles API.
*   **Coûts variables :** L'utilisation de modèles "agentiques" (Claude Fable, GPT-6 Astra) est décrite comme très gourmande en quotas/crédits.

## Partie 2/2 (modèle gemini-3.1-flash-lite)

Voici un résumé structuré des échanges du direct de Coben :

### 1. Outils d'IA testés
L'auteur souligne une utilisation intensive de différents outils, bien qu'il admette une phase d'expérimentation exploratoire :
*   **ChatGPT (Forfait 20€/mois) :** Utilisé principalement pour la gestion des mails et les échanges professionnels. L'auteur souligne que la génération de fichiers 3D par IA n'était pas fonctionnelle à l'époque de son abonnement, mais salue l'efficacité pour le textuel.
*   **Claude (Forfait 20€/mois) :** Apprécié pour son aide dans le codage (via des fonctionnalités de type « vibe code »).
*   **Maker Map (V2 en développement) :** Projet personnel de l'auteur visant à connecter des imprimeurs 3D locaux. L'outil est décrit comme une infrastructure complexe utilisant l'IA pour faciliter la mise en relation.
*   **Outils mentionnés sans test approfondi :** Moon AI, Fable, Deic, Muse Spark, Qwen 3.7.
*   **Qualité constatée :** L'auteur note que si l'IA est un excellent assistant pour le code et l'organisation, sa capacité à générer des modèles 3D complexes reste un domaine en constante évolution.

### 2. Astuces concrètes et réutilisables
*   **Contournement des restrictions géographiques :** L'auteur conseille la création de comptes (Apple Store, sites web) localisés aux États-Unis pour accéder à des applications ou fonctionnalités bloquées en France (exemple cité : l'application *Super Human* pour le suivi de la fibromyalgie).
*   **Utilisation des réseaux sociaux pour le business :** L'auteur insiste sur le fait que, face à la concurrence de plateformes comme Temu, la survie d'une boutique d'impression 3D repose exclusivement sur le trafic naturel généré par les réseaux sociaux.
*   **Veille technologique :** Il recommande X (anciennement Twitter) plutôt qu'Instagram ou TikTok pour la veille technologique, soulignant que les fuites (leaks) et les innovations (ex: brevets Bambu Lab) y apparaissent en priorité.

### 3. Limites et échecs constatés
*   **Gestion de projet :** L'auteur reconnaît avoir perdu énormément de temps en "s'éparpillant" sur Maker Map, en ajoutant trop d'options inutiles au lieu de se concentrer sur le visuel.
*   **Éthique du business :** Il dénonce vigoureusement la revente d'impressions 3D bon marché (ex: Temu) présentées comme du "fait-maison".
*   **Fatigue de la création :** L'auteur évoque des périodes de baisse de moral ayant conduit au refus de collaborations avec des marques, préférant l'intégrité à l'accumulation de matériel.

### 4. Chiffres et prix cités
*   **Abonnements IA :** 20 €/mois (ChatGPT, Claude).
*   **Impression 3D (marché bas de gamme) :** Prix cités par l'auteur comme « impossibles » à tenir pour un artisan local (ex: dragon 30 cm à 2,41 € ou 2,91 € sur Temu).
*   **Revenus YouTube :** Environ 100 €/mois (selon l'auteur, "non précisé" comme revenu stable).
*   **Prix de vente/matériel :** CNC citée à 399 € (prix marché 570 €).
*   **Cartes de collection (Wiki Master) :** Cartes vendues jusqu'à 2 000 €.
