# Et si nous arrêtions d'utiliser des GPU ? | YC Paper Club

Vidéo : https://youtu.be/xc2FTBGRSJo · durée 1:20:35 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-05
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une synthèse de la présentation sous forme de fiche de connaissances.

### **1) Sujet et thèse principale**
*   **Sujet :** L'évolution des paradigmes de calcul (informatique) pour répondre aux besoins croissants en efficacité énergétique des modèles d'intelligence artificielle.
*   **Thèse principale :** Le matériel informatique traditionnel (basé sur le silicium et des architectures numériques) atteint ses limites de consommation d'énergie face aux besoins de l'IA. Pour progresser vers une intelligence de niveau humain, il est nécessaire de concevoir de nouvelles architectures matérielles (neuromorphiques, optiques) inspirées du fonctionnement biologique du cerveau, qui est bien plus économe en énergie.

### **2) Notions expliquées**
*   **Calcul Neuromorphique :** Conception de puces informatiques inspirées de la structure et du fonctionnement des neurones et des synapses du cerveau biologique.
*   **Calcul Optique :** Utilisation de la lumière (photons) pour transmettre et traiter l'information. Cette technologie est jugée prometteuse car la lumière ne génère que très peu de chaleur lors de son passage dans un support, contrairement au courant électrique dans les métaux.
*   **Spikes (pics) :** Signaux électriques brefs utilisés par les neurones (biologiques ou artificiels) pour communiquer entre eux.
*   **Backpropagation :** Méthode mathématique standard pour entraîner les réseaux de neurones (consiste à ajuster les connexions internes pour réduire les erreurs).
*   **PPO (Proximal Policy Optimization) :** Un algorithme d'apprentissage par renforcement utilisé pour entraîner des systèmes à prendre des décisions (ici, pour faire jouer des cellules cérébrales à un jeu vidéo).
*   **Synapses :** Zones de contact entre neurones qui servent à transmettre l'information. En informatique, elles sont modélisées par des "poids" numériques qui déterminent l'importance d'une donnée.

### **3) Chiffres, taux et plafonds**
*   **Consommation du cerveau humain :** 20 Watts (comparé à des centres de données qui consomment des quantités massives d'énergie).
*   **Avantage des photons vs électrons :** Environ 10 000 fois moins de perte d'énergie et une bande passante 10 000 fois plus grande pour la transmission de données.
*   **Capacité du système de jeu vidéo cité :** 65,5 TOPS (Téra-opérations par seconde).
*   **Stimulation neuronale :** Environ 1,0 à 2,5 microampères (µA) pour les stimulations des cellules.
*   **Remarque fiscale/légale :** Aucune règle fiscale ou légale citée dans cette vidéo technique.

### **4) Conseils concrets, limites et risques**
*   **Conseil (approche de recherche) :** Privilégier le "co-design" matériel et logiciel (concevoir l'architecture physique de la puce en même temps que les algorithmes qu'elle devra exécuter) plutôt que de tenter d'adapter des logiciels d'IA existants sur du matériel non optimisé.
*   **Limites et risques :**
    *   **Complexité de fabrication :** La miniaturisation et la précision requises pour les composants optiques ou neuromorphiques sont extrêmement complexes.
    *   **Réplicabilité :** Le passage à l'échelle (industrialisation) pour des systèmes massifs est un défi majeur.
    *   **Énergie :** Certaines opérations non linéaires (essentielles pour l'IA) sont très difficiles à réaliser avec la lumière, ce qui nécessite des mécanismes complexes et coûteux en énergie.

### **5) Produits, applications et entreprises cités**
*   **Entreprises citées (à titre informatif) :**
    *   **NVIDIA :** Leader actuel du marché des puces pour l'IA (GPU).
    *   **Intel :** Mentionné pour ses recherches avec la puce "Loihi".
    *   **IBM :** Mentionné pour la puce "NorthPole".
    *   **Google DeepMind :** Collaborateur sur les recherches présentées.
    *   **Parasma :** Entreprise dirigée par l'un des intervenants (Sean Cole).
    *   **d-Matrix :** Startup travaillant sur les puces d'inférence.
    *   **Lightmatter :** Entreprise spécialisée dans le calcul photonique.
*   **Note :** Les intervenants mentionnent ces entreprises dans le cadre de leurs recherches académiques ou professionnelles. Il ne s'agit pas de conseils d'investissement, mais d'un état des lieux du secteur technologique.
