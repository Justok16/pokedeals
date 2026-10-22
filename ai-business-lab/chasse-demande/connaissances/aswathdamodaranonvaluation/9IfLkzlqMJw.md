# Country Equity Risk Premiums: Dataset support

Vidéo : https://youtu.be/9IfLkzlqMJw · durée 11:06 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances basée sur le contenu de la vidéo :

### 1) Sujet et thèse principale
**Sujet :** Le calcul de la prime de risque des capitaux propres (*Equity Risk Premium* - ERP) par pays.
**Thèse :** La prime de risque n'est pas uniforme à travers le monde. Il est nécessaire d'ajuster l'ERP selon le pays dans lequel une entreprise opère pour refléter les risques locaux (guerre, système politique, cadre légal, cycle économique). Bien que la diversification mondiale ait été un argument pour uniformiser l'ERP par le passé, la corrélation croissante entre les marchés rend désormais indispensable l'ajustement du risque pays.

### 2) Notions expliquées
*   **Equity Risk Premium (ERP) :** La prime de risque exigée par les investisseurs pour investir dans des actions par rapport à des actifs sans risque.
*   **Sovereign CDS (Credit Default Swap) :** Un dérivé financier agissant comme une assurance contre le défaut de paiement d'un pays.
*   **Spread de défaut (*Default Spread*) :** Le surcoût (prime) demandé par les investisseurs pour prêter à un pays par rapport à un pays considéré comme sûr (ex: USA).
*   **Marché mature :** Marché stable, généralement noté AAA (ex: USA, Allemagne, Singapour, pays scandinaves).

### 3) Chiffres, taux et règles cités
*   **Corrélation des marchés :** Les marchés mondiaux bougent ensemble à 95-97 % lors des périodes de crise (*donnée pour le siècle actuel*).
*   **Exemple de calcul :** Si l'ERP des USA est de 5 % et le *spread* de défaut d'un pays est de 2 %, l'ERP pour ce pays est de 7 %.
*   **Ratio de volatilité :** L'auteur utilise un ratio d'environ 1,4 (volatilité des actions / volatilité des obligations d'un pays) pour ajuster les *spreads* de défaut.
*   **Règles fiscales :** Aucune règle fiscale ou légale spécifique n'est citée. *(À vérifier à la source officielle)*.

### 4) Conseils concrets, limites et risques
*   **Méthode de calcul conseillée :** L'auteur recommande d'estimer l'ERP d'un pays mature (USA) comme point de départ, puis d'y ajouter un *spread* de défaut (via CDS ou notation souveraine), et enfin d'ajuster ce *spread* selon la volatilité relative entre actions et obligations.
*   **Cas des pays sans notation :** Pour les pays sans notation (*frontiers markets* comme la Syrie ou le Soudan), l'auteur suggère d'utiliser le score de risque politique pour s'inspirer d'autres pays aux scores similaires.
*   **Limites :** L'auteur reconnaît lui-même que ses modèles sont des estimations ("approximations") et qu'il est possible de ne pas être d'accord avec ses choix méthodologiques. Il souligne que le calcul précis de la volatilité relative est complexe car peu de pays ont des marchés d'obligations d'État suffisamment liquides.

### 5) Produits, applications et entreprises cités
*   **S&P 500 :** Utilisé comme référence pour l'ERP d'un marché mature (outil d'analyse, non publicitaire).
*   **Moody’s :** Agence de notation citée pour obtenir les notations souveraines.
*   **Aucune publicité :** L'auteur présente ses propres méthodes de travail ; aucun produit commercial, application ou service payant de sa propre marque n'est mis en avant pour la vente.
