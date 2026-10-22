# Session 10: Bottom up Betas - Private Businesses

Vidéo : https://youtu.be/_ZlLd9Olavc · durée 48:54 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances en finances personnelles :

1. Sujet et thèse principale
- Sujet : L'estimation des bêtas bottom-up (de bas en haut) et du coût des capitaux propres, notamment pour des entreprises diversifiées, internationales ou non cotées, ainsi que la gestion du risque (marché vs risque total) et l'utilisation de comparables.
- Thèse principale : L'utilisation d'un bêta "bottom-up" (fondé sur les différentes activités de l'entreprise et la moyenne des pairs) est plus précise et robuste que la régression historique d'une entreprise individuelle. De plus, pour les actifs non cotés ou les entreprises privées, il faut ajuster le bêta pour intégrer le risque total (via le $R^2$) car le propriétaire n'est pas diversifié.

2. Notions expliquées (définitions simples)
- Bêta unlevered (sans effet de levier) : Mesure du risque systématique d'une entreprise en excluant l'impact de la dette (dette financière).
- Bêta levered (avec effet de levier) : Bêta ajusté pour tenir compte de la structure financière (dette/fonds propres) de l'entreprise.
- Coût des capitaux propres (Cost of Equity) : Le taux de rendement exigé par les actionnaires, calculé souvent via le MEDAF (Modèle d'Évaluation des Actifs Financiers) : Taux sans risque + (Bêta × Prime de risque des actions).
- Différentiel d'inflation : Méthode pour convertir un coût du capital d'une devise à une autre (par exemple du dollar au real brésilien) en utilisant l'inflation attendue dans les deux pays.
- Bêta comptable : Alternative pour les actifs non cotés consistant à régresser les variations de bénéfices/résultats de l'entreprise par rapport à un indice de marché (souvent jugé inefficace et lissant les données).
- Bêta total : Ajustement du bêta de marché par la racine carrée du $R^2$ de la régression, pour refléter le risque total (et non seulement le risque de marché) pertinent pour les propriétaires de petites entreprises non diversifiées.

3. Chiffres, taux, plafonds et règles fiscales cités
- Vale (entreprise minière/fer): 
  - Répartition des activités en 4 segments (Métaux & Mines 16.65%, Minerai de fer 76.20%, Engrais 5.39%, Logistique 1.76%).
  - Coût d'équité global en USD ou converti en Real brésilien (avec inflation de 9% au Brésil et 2% aux US -> Coût d'équité en $R = 18.87%$).
- Tata Motors (automobile) : 
  - Bêta unlevered estimé à 0.8601 (sur 76 entreprises). Ratio D/E de 41.41%, taux marginal d'impôt de 32.45%.
  - Taux sans risque (en Roupies) de 6.57%, coût des capitaux propres = 14.49%.
- Baidu (internet/recherche) : 
  - Bêta unlevered estimé à 1.30 (sur 42 entreprises). Taux marginal d'impôt de la Chine = 25%. Coût des capitaux propres en $R = 12.91%$.
- Deutsche Bank :
  - Division en deux métiers : banque commerciale et banque d'investissement. Taux sans risque de 1.75% (taux euro risk-free) et ERP (prime de risque) de 6.12%.
- Bookscape (librairie indépendante non cotée) :
  - Ratio dette/fonds propres de la librairie pris à la médiane du secteur : 21.41%. Taux d'impôt marginal : 40%.
  - Bêta levered = 0.8558. Taux sans risque = 2.75% (bon du Trésor US), prime de risque = 5.5%. Coût des capitaux propres = 7.46%.
  - Ajustement pour le risque total (Total Beta) avec un $R^2$ de 50.99% (ou 0.5099) : Bêta total = $0.8558 / \sqrt{0.5099} = 1.6783$. Nouveau coût des capitaux propres = 11.98%.
- Règles fiscales et légales : Aucune règle fiscale précise n'est donnée comme un plafond fiscal national fixe applicable universellement ; les taux d'imposition cités sont des hypothèses ou des taux marginaux propres aux exemples (ex: 32.45% pour Tata Motors, 25% pour Baidu, 40% pour Bookscape). **À vérifier à la source officielle** pour toute application fiscale réelle.

4. Conseils concrets, limites et risques
- Privilégier les bêtas "bottom-up" (basés sur les pairs et la ventilation des activités) plutôt que la régression historique d'une seule entreprise, surtout si l'entreprise est multi-activités ou change de profil.
- Pour les entreprises non cotées (petites entreprises familiales), le propriétaire est souvent non diversifié : utiliser le "Bêta total" (en divisant le bêta de marché par la racine carrée du $R^2$) pour capturer tout le risque spécifique de l'entreprise, ce qui augmente le coût des capitaux propres exigé.
- Limite : Les bêtas comptables basés sur les bénéfices lissent artificiellement la réalité et ne doivent pas être privilégiés.
- Risque : Appliquer un bêta de marché standard à une entreprise privée ou non diversifiée sous-estime le risque réel perçu par son unique propriétaire.

5. Produits, applications ou entreprises cités
- Entreprises citées à titre pédagogique / études de cas : Vale, Disney, Tata Motors, Baidu, Deutsche Bank, Reddit, Bloomberg, JP Morgan, Bookscape, CVS, Dwayne Reade.
- S'agit-il de publicité ? Non, ce sont des cas d'étude universitaires présentés par le professeur Aswath Damodaran. Aucun produit commercial n'est vendu ou promu.
