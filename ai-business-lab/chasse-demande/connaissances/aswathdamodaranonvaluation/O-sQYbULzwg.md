# Session 19 : Clôture de la tarification

Vidéo : https://youtu.be/O-sQYbULzwg · durée 1:23:39 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-22
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances en finances personnelles basée sur la vidéo :

---

# Fiche de connaissances : Évaluation relative (Valorisation par les multiples et régressions)

## 1. Sujet et thèse principale
* **Sujet :** L’évaluation relative (pricing) et l’utilisation des multiples de valorisation (P/E, P/BV, EV/EBITDA, P/S) complétés par des régressions multiples pour contrôler les différences fondamentales entre entreprises (croissance, risque, rentabilité).
* **Thèse principale :** L'évaluation relative n'est pas une science exacte mais un jeu de prix dicté par le marché. Ne jamais mélanger valorisation intrinsèque (DCF) et pricing relatif. Utiliser de grands échantillons et des régressions statistiques permet d'ajuster les multiples aux fondamentaux (croissance, risque), mais attention au bruit statistique (non-linéarité, non-stationnarité, multicollinéarité).

---

## 2. Notions expliquées (Définitions simples)
* **Évaluation relative (Pricing) :** Estimer la valeur d'une entreprise en comparant son prix à celui d'autres entreprises comparables (les "comps") sur la base de multiples (ex: P/E, P/BV).
* **Multiple P/E (Price-to-Earnings) :** Ratio du cours de l'action sur le bénéfice par action (bénéfices).
* **Multiple P/BV (Price-to-Book Value) :** Rapport entre la valeur boursière (prix) et la valeur comptable des capitaux propres.
* **Multiple EV/EBITDA :** Valeur d'entreprise divisée par l'excédent brut d'exploitation (EBITDA), indicateur de rentabilité avant intérêts, impôts, dépréciations et amortissements.
* **Multiple P/S (Price-to-Sales) :** Rapport entre la capitalisation boursière (ou prix) et le chiffre d'affaires.
* **R-carré ($R^2$) :** Pourcentage de la variation du multiple expliqué par les variables indépendantes (croissance, risque, etc.) dans une régression.
* **Multicollinéarité :** Corrélation forte entre les variables indépendantes (ex: croissance et risque) dans une régression multiple, pouvant fausser les coefficients.

---

## 3. Chiffres, taux, plafonds et règles cités
* **Exemple Zlyloft :** Valeur intrinsèque (DCF) = 10 $/action ; Cours en bourse = 15 $/action ; Multiple P/E sectoriel (pricing) = 20 $/action.
* **Exemples de régressions (données historiques de l'intervenant) :**
  * Échantillon de banques européennes (2010) : Régression P/BV expliquée par le ROE et l'écart-type du cours (risque), $R^2$ = 79%.
  * Échantillon de plus grandes entreprises américaines (janvier 2010 et janvier 2022) : Régression P/BV sur le ROE, la croissance et le risque (bêta).
  * Exemples d'entreprises technologiques (Amazon en l'an 2000, réseaux sociaux en octobre 2013).
* *Règle fiscale/légale :* Aucune règle fiscale ou légale spécifique n'est citée dans cette vidéo académique de finance d'entreprise. (*À vérifier à la source officielle* pour toute application réglementaire en vigueur).

---

## 4. Conseils concrets et leurs limites ou risques
* **Conseil 1 : Ne jamais mélanger prix et valeur.** Ne combinez pas une valorisation intrinsèque (DCF) avec des multiples de marché pour faire une moyenne. Le prix dépend de ce que paie le marché.
* **Conseil 2 : Bien choisir son échantillon de comparables.** Plus la sélection est étroite ("juste comme vous"), plus l'échantillon est petit et qualitatif ; plus elle est large, plus il faut utiliser des techniques statistiques (régressions) pour contrôler les différences de risque et de croissance.
* **Conseil 3 : Vérifier les statistiques des régressions ($t$-statistiques, $R^2$).** Ne gardez pas de variables non significatives qui ajoutent du bruit au modèle. Attention aux intercept négatifs et à la multicollinéarité.
* **Limite / Risque :** Le pricing reflète l'exubérance ou la décote du marché à un instant T (erreurs de marché, bulles sectorielles comme les valeurs technologiques en 2000 ou les réseaux sociaux en 2013). Un titre peut être "bon marché" en relatif tout en étant structurellement surévalué par rapport à sa valeur intrinsèque.

---

## 5. Produits, applications ou entreprises cités
* **Entreprises et actions citées (exemples pédagogiques) :**
  * Zlyloft Inc. (fictif)
  * Coca-Cola, Anheuser-Busch, Brown-Forman, Coors, PepsiCo, Boston Beer, Whitman, Hansen Natural (secteur des boissons)
  * Indosat, Telebras, Telefonica, Telkom, Cable & Wireless, Telekomunikasi, etc. (secteur télécoms)
  * Bayerische Hypo- und Vereinsbank, Commerzbank, Deutsche Bank, Intesa Sanpaolo, BBVA, Santander, Société Générale, Royal Bank of Scotland, Barclays, Unicredit, Lloyds (banques européennes)
  * Ryder System, KLLM (transport/camionnage)
  * Whole Foods, Sprouts, Kroger (grande distribution)
  * Facebook, LinkedIn, Twitter, Yelp, Groupon, OpenTable, Zillow, TripAdvisor (réseaux sociaux / internet)
  * General Motors, Ford, Chrysler, Nokia, ExxonMobil, Google (Alphabet), Infospace, Genta, Tesla.
* **Précision :** Il s'agit d'exemples académiques présentés dans le cadre d'un cours universitaire de finance (Aswath Damodaran). **Ce ne sont pas des conseils en investissement ni de la publicité commerciale.**
