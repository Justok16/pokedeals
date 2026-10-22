# Comment protéger un portefeuille actions avec les Turbos et les Warrants ?

Vidéo : https://youtu.be/jgWwLsh6Z5A · durée 21:14 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale** :
- **Sujet** : L'utilisation des warrants et des turbos à des fins de couverture de portefeuille.
- **Thèse principale** : Les produits dérivés à effet de levier (warrants et turbos) permettent de protéger efficacement un portefeuille contre la baisse des marchés ou de réaliser des opérations de "cash extraction" sans vendre ses titres sous-jacents.

2) **Notions expliquées (définitions simples)** :
- **Produits dérivés (Warrants, Turbos)** : Instruments financiers à effet de levier permettant d'amplifier les variations d'un actif sous-jacent.
- **Turbo** : Produit à effet de levier caractérisé par une barrière désactivante (si touchée, le produit est radié et le capital investi est perdu).
- **Turbo classique** : Strike (prix d'exercice) et barrière désactivante identiques, avec une échéance définie.
- **Turbo illimité** : Sans échéance, avec un strike et une barrière désactivante distincts. Le remboursement à l'échéance (ou désactivation) dépend de la valeur résiduelle.
- **Turbo Best (Unlimited Best)** : Strike et barrière identiques, sans échéance, s'ajustant quotidiennement aux taux d'intérêt et dividendes.
- **Warrant** : Produit optionnel caractérisé par une valeur temps et une valeur intrinsèque, avec une échéance et une parité définies.
- **Put** : Option de vente qui prend de la valeur quand le sous-jacent baisse (utilisé en couverture).
- **Call** : Option d'achat qui prend de la valeur quand le sous-jacent hausse.
- **Strike (Prix d'exercice)** : Prix auquel le sous-jacent peut être acheté (Call) ou vendu (Put).
- **Parité** : Nombre de warrants ou turbos nécessaires pour obtenir une unité du sous-jacent.
- **Delta** : Sensibilité du prix du produit dérivé par rapport à la variation du sous-jacent (ex: delta de 0,50 signifie que le produit bouge de 0,50€ pour 1€ de variation du sous-jacent).
- **Couverture classique** : Utilisation de puts pour compenser la perte en capital d'un portefeuille d'actions lors d'une baisse des marchés.
- **Cash Extraction** : Vente de titres en portefeuille pour récupérer des liquidités tout en maintenant une exposition acheteuse via l'achat de calls (ou l'inverse).

3) **Chiffres, taux, plafonds et règles fiscales** :
- Exemples chiffrés présentés dans la vidéo :
  - Portefeuille de référence : 50 000 €.
  - Indice de référence : CAC 40 à 5 300 points (Bêta proche de 1).
  - Exemple 1 (Put Warrant) : Prix d'exercice 5 200, parité 200, delta 0,41, cours du warrant 0,60 €.
  - Scénario 1 (CAC 40 perd 10% à 4 770 points) : Perte du portefeuille = 4 776 € ; gain sur les puts = 10 580 € (valeur du portefeuille final avec couverture : 53 044 €, soit un gain de 6,08%).
  - Scénario 2 (CAC 40 gagne 5% à 5 565 points) : Perte sur les puts = 2 760 € ; gain du portefeuille global (après couverture) = 2 362 € (valeur finale : 49 602 €, soit -0,8%).
  - Scénario 3 (CAC 40 stable à 5 300 points) : Perte de valeur temps sur les puts = 2 760 € (-5,5% du portefeuille).
  - Exemple 3 (Cash Extraction) : 60 actions Kering à 308 € = 18 480 € ; achat de 1 200 call turbos (Turbo Call 333WZ, strike 275, parité 20, cours 1,63 €) pour un coût de 1 956 €.
- Aucune règle fiscale spécifique n'est mentionnée avec un taux ou un plafond légal précis.

4) **Conseils concrets, limites et risques** :
- **Conseils** :
  - Choisir des puts "at-the-money" (proches de la monnaie) avec un delta proche de 0,40 / 0,50 et une échéance de 4 à 6 mois pour une couverture classique.
  - Ajuster le nombre de warrants ou de turbos achetés en fonction de la valeur du portefeuille, de la parité et du delta.
  - Couper sa position de couverture en cas de franchissement de résistance ou alléger les puts dans la baisse pour éviter une sur-couverture au delta trop élevé.
- **Limites et risques** :
  - Risque de perte totale du capital investi sur les turbos si la barrière désactivante est touchée.
  - Risque de perte de valeur temps (érosion) sur les warrants en cas de stagnation ou de hausse du marché.
  - Coût de la couverture en l'absence de baisse des marchés (prime payée à fonds perdu).

5) **Produits, applications ou entreprises cités** :
- **Commerzbank** : Partenaire et émetteur de produits dérivés (publicité / mention dans la présentation).
- **ZoneBourse** : Organisateur du webinaire (produit de l'auteur).
- **CAC 40** : Indice boursier sous-jacent de référence.
- **Kering** : Action sous-jacente utilisée pour l'exemple de cash extraction.
- **Produits spécifiques cités** : Put Warrant 313BZ, Turbo Call 333WZ.

---
