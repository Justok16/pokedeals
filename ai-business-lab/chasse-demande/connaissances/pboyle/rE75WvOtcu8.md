# Il faut qu'on parle de Leopold

Vidéo : https://youtu.be/rE75WvOtcu8 · durée 41:28 · résumé Gemini (gemini-3.5-flash) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances en finances personnelles et gestion des risques :

### 1) Sujet et thèse principale
* **Sujet :** L'analyse de la chute du fonds spéculatif thématique « Situational Awareness », géré par Leopold Aschenbrenner (24 ans), qui a perdu environ les deux tiers de ses 45 milliards de dollars d'actifs sous gestion en quelques semaines durant l'été 2024.
* **Thèse principale :** L'utilisation d'un effet de levier massif sur des investissements thématiques très volatils et concentrés (comme l'intelligence artificielle), sans couverture réelle, est une stratégie mathématiquement vouée à l'échec. Même si la thèse fondamentale de départ (l'essor à long terme de l'IA) s'avère correcte, la volatilité combinée au levier détruit mécaniquement la performance à cause du phénomène de « traînée de volatilité » (*volatility drag*) et des appels de marge.

---

### 2) Notions expliquées
* **Hedge fund Long/Short (Fonds d'arbitrage acheteur/vendeur) :** Stratégie qui consiste à acheter des actions jugées sous-évaluées (positions longues) et à vendre à découvert des actions jugées surévaluées (positions courtes) pour s'affranchir des mouvements globaux du marché et ne dépendre que de la qualité de sa sélection de titres.
* **Couverture (Hedging) :** Technique de gestion des risques consistant à associer des actifs financiers pour neutraliser l'impact des fluctuations indésirables du marché.
* **Effet de levier (Leverage) :** Utilisation de capitaux empruntés pour augmenter la taille d'une position financière afin d'amplifier les gains potentiels (ce qui amplifie également les pertes).
* **Traînée de volatilité (Volatility Drag) :** Impact mathématique négatif de la volatilité sur le taux de croissance composé réel d'un portefeuille par rapport à son rendement moyen arithmétique simple.
* **Appel de marge (Margin Call) :** Exigence d'un courtier ou d'un prêteur demandant à l'investisseur d'apporter des liquidités ou des garanties supplémentaires lorsque la valeur des actifs achetés à crédit baisse sous un certain seuil.

---

### 3) Chiffres, taux, formules et règles cités
* **Pertes du fonds :** Une chute brutale de **67 %** de la valeur des actifs en juillet 2024.
* **Effet de levier :** Le fonds utilisait un effet de levier d'environ **4 à 5 fois** son capital (jusqu'à 400 % d'exposition).
* **Exemple mathématique du lancer de pièce :** 
  * Pile : gain de 50 %. Face : perte de 40 %. Le rendement arithmétique moyen espéré est de +5 % par lancer.
  * Si l'on commence avec 100 $ : après un gain (+50 % = 150 $) et une perte (-40 % = 90 $), le capital réel tombe à 90 $ (perte réelle de 10 %). Après un deuxième cycle similaire, le capital descend à 81 $.
* **Formule du taux de croissance composé ($g$) :**
  * $g \approx \mu - \frac{\sigma^2}{2}$
  * Où $\mu$ est le rendement moyen arithmétique espéré et $\sigma$ représente la volatilité. Le terme $\frac{\sigma^2}{2}$ correspond à la traînée de volatilité.
* **Exemple chiffré de l'impact du levier (4x) :**
  * *Sans levier* : Pour un rendement thématique espéré ($\mu$) de 15 % et une volatilité ($\sigma$) de 40 %, le taux de croissance composé réel ($g$) est de : $15\% - \frac{0,4^2}{2} = 15\% - 8\% = 7\%$.
  * *Avec levier (4x)* : Le rendement espéré devient $4 \times 15\% = 60\%$. La volatilité quadruple à 160 %. La traînée de volatilité passe à $\frac{1,6^2}{2} = 128\%$. Le taux de croissance composé réel ($g$) plonge alors à $60\% - 128\% = -68\%$ par an.
* **Règles légales citées :** Aux États-Unis, les courtiers n'autorisent pas les mineurs (moins de 18 ans) à ouvrir des comptes sur marge ou à découvert car ils ne peuvent pas légalement s'engager par contrat (*à vérifier à la source officielle*).

---

### 4) Conseils concrets et risques associés
* **Ne pas appliquer de levier sur des actifs hautement volatils :** L'effet de levier doit être réservé aux actifs très peu volatils pour optimiser de faibles rendements. L'appliquer sur des actions technologiques ou de croissance démultiplie la traînée de volatilité de façon quadratique (au carré du levier).
* **Se méfier des fausses couvertures (couvertures corrélées) :** Acheter des fabricants de puces IA tout en vendant à découvert des éditeurs de logiciels applicatifs n'est pas une couverture. Les deux côtés du pari dépendent en réalité du même thème (l'adoption de l'IA). Si le secteur ralentit, les deux jambes du portefeuille perdent de l'argent simultanément.
* **Prendre en compte le risque de ruine :** Le rendement théorique moyen (la moyenne arithmétique) est souvent faussé à la hausse par une minorité de scénarios exceptionnels (la "bulle de succès"). Le rendement médian (celui que subira la majorité des investisseurs) s'établit bien plus bas, souvent en territoire négatif lors d'oscillations extrêmes.
* **La liquidité protège de la panique :** Les actifs non liquides (comme les parts dans des start-ups non cotées telles qu'Anthropic) ne subissent pas d'évaluation quotidienne du marché, ce qui évite les appels de marge immédiats et les liquidations forcées au pire moment.

---

### 5) Produits, applications et entreprises cités
* **Zocdoc :** Application de recherche de médecins et de prise de rendez-vous en ligne (mentionnée dans le cadre d'un **partenariat publicitaire rémunéré**).
* **Livres de Patrick Boyle :** *Derivatives for the Trading Floor* et *Statistics for the Trading Floor* (il s'agit des **produits de l'auteur** de la vidéo).
* **Hedge funds et banques d'affaires cités :** Citadel (Ken Griffin), Jane Street, Millennium Management, Blackstone, Sequoia Capital, Greenoaks Capital, Goldman Sachs, JPMorgan Chase, Bank of America, AQR Capital Management (Cliff Asness).
* **Sociétés citées :** Stripe, OpenAI, FTX, Anthropic, SK Hynix, SanDisk, Bloom Energy, Adobe, Samsung.
