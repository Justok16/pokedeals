# Session 9: Betas - Drivers and Determinants

Vidéo : https://youtu.be/B2pvG3hbvac · durée 1:22:25 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-25
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

# Fiche de connaissances : Déterminants du Bêta et Levier Financier

## 1. Sujet et thèse principale
* **Sujet :** L'évaluation et les déterminants du bêta (mesure de l'exposition au risque macroéconomique) d'une entreprise, ainsi que l'impact du levier opérationnel et financier.
* **Thèse principale :** Le bêta d'une entreprise ne provient pas uniquement de services ou de régressions passées, mais de choix stratégiques fondamentaux : le type de produit/service (cyclique vs non cyclique, discrétionnaire vs non discrétionnaire), le levier opérationnel (coûts fixes vs variables) et le levier financier (niveau d'endettement). L'utilisation de bêtas « bottom-up » (recalculés par activité et désendettés) est préférable aux bêtas de régression « top-down » (rétrospectifs et bruités).

---

## 2. Notions expliquées (définitions simples)
* **Bêta :** Mesure de la sensibilité de la demande (ou des mouvements) d'une entreprise par rapport au marché/macroéconomie. Ce n'est pas une mesure de volatilité, mais de mouvement conjoint avec le marché.
* **Élasticité de la demande :** Sensibilité de la demande des clients pour un produit face aux variations économiques (les produits à forte élasticité ont des bêtas plus élevés).
* **Entreprises cycliques :** Entreprises dont l'activité suit de près les cycles macroéconomiques (ex. automobile, acier, construction), caractérisées par des bêtas plus élevés.
* **Produits discrétionnaires :** Biens ou services que les consommateurs peuvent retarder ou différer en cas de difficultés financières (ex. produits de luxe, voyage), entraînant des bêtas plus élevés.
* **Levier opérationnel :** Proportion des coûts totaux d'une entreprise qui sont des coûts fixes. Des coûts fixes élevés amplifient la volatilité des bénéfices (EBIT) suite à une variation des revenus.
* **Levier financier :** Proportion de dettes dans le capital de l'entreprise. L'emprunt crée des frais d'intérêts (coûts fixes), ce qui rend les bénéfices des actionnaires (équité) plus volatils et augmente le bêta des capitaux propres.
* **Désendettement du bêta (*Unlevering Beta*) :** Processus mathématique permettant de retirer l'effet de l'endettement d'un bêta pour isoler le risque inhérent à l'activité de l'entreprise (*Asset Beta*).
* **Bêta *Bottom-up* :** Méthode consistant à estimer le bêta d'une entreprise à partir des bêtas désendettés de ses différentes activités (pondérés par leur valeur d'entreprise ou chiffre d'affaires), puis à ré-endetter le tout selon la structure cible de l'entreprise.

---

## 3. Chiffres, taux, plafonds et règles fiscales cités
* **Période d'analyse pour Disney (exemples chiffrés) :**
  * Régression historique analysée de 1987 à 2013.
  * Bêta de régression (léveré) pour Disney : **1.25** (période 2008–2013).
  * Ratio d'endettement moyen de Disney sur la période : **19.44 %**.
  * Taux d'imposition marginal (*tax rate*) utilisé pour Disney : **36.1 %** (taux fédéral de 35 % + étatique/local ; *à vérifier à la source officielle*).
  * Bêta désendetté (*unlevered beta*) calculé pour Disney : **1.11** (ou **1.08** selon les étapes de calcul).
* **Exemple de la fusion Disney / Cap Cities (1996) :**
  * Disney (Acquéreur) : Dette = 3,186 milliards de dollars, Valeur de marché des actions = 31,100 milliards, ratio D/E = 0.10, bêta actions = **1.15**.
  * Cap Cities (Cible) : Dette = 615 millions, Valeur de marché des actions = 18,500 milliards, ratio D/E = 0.03, bêta actions = **0.95**.
  * Bêta désendetté combiné : **1.026**.
  * Si Disney avait financé l'opération 100 % par actions (18.5 milliards) : ratio D/E post-fusion = 7.7 %, nouveau bêta levé = **1.08**.
  * Si Disney avait emprunté 10 milliards et émis 8.5 milliards d'actions : ratio D/E post-fusion = 34.82 %, nouveau bêta levé = **1.25**.
* **Statistiques sectorielles (exemples cités) :**
  * Moyenne du levier opérationnel dans l'industrie du divertissement : **1.15**.
  * Bêtas désendettés médians pour les divisions de Disney (données 2013) :
    * *Media Networks* : **1.0024** (Valeur = 66,579B, proportion = 49.27 %).
    * *Parks & Resorts* : **0.6677** (Valeur = 45,683B, proportion = 33.81 %).
    * *Studio Entertainment* : **1.0068** (Valeur = 18,234B, proportion = 13.49 %).
    * *Consumer Products* : **0.6034** (Valeur = 2,951B, proportion = 2.18 %).
    * *Interactive* : **1.0085** (Valeur = 1,683B, proportion = 1.24 %).
* **Règles fiscales :**
  * Les charges d'intérêts sur la dette sont déductibles fiscalement (effet du bouclier fiscal représenté par le facteur `(1 - t)` dans la formule de désendettement). (*À vérifier à la source officielle*)

---

## 4. Conseils concrets et leurs limites ou risques
* **Conseil :** Préférer l'utilisation d'un bêta *bottom-up* plutôt qu'un bêta de régression (*top-down*). Les régressions sont passées, bruitées (grandes erreurs standard) et impossibles à calculer pour des entreprises privées ou de nouvelles divisions.
* **Conseil :** Toujours commencer par désendetter les bêtas comparables (*unlevering*), calculer une moyenne pondérée par la valeur d'entreprise (ou les revenus), puis ré-lever (*lever*) le bêta final selon la structure financière propre de l'entreprise cible ou sa division.
* **Limite / Risque :** Le choix de l'allocation de la dette totale d'un conglomérat à ses divisions peut s'avérer délicat. L'auteur suggère d'allouer la dette en fonction des actifs identifiables (*identifiable assets*), mais prévient qu'isoler le levier par division reste un exercice d'approximation.
* **Limite / Risque :** Utiliser des moyennes sectorielles comporte un risque si les comparables choisis s'écartent trop de la réalité de l'entreprise analysée (ex. inclure des entreprises « *tetering on the edge of disaster* » comme des compagnies aériennes ou des studios en difficulté).

---

## 5. Produits, applications ou entreprises cités
* **Entreprises et marques citées (exemples pédagogiques) :**
  * *Disney* (et ses divisions : *Media Networks*, *Parks & Resorts*, *Studio Entertainment*, *Consumer Products*, *Interactive*).
  * *Cap Cities / ABC* (cible de rachat par Disney en 1996).
  * *Kroger* vs *Whole Foods* (comparaison sur le levier opérationnel et la nature des produits d'épicerie).
  * *Southwest Airlines* vs autres compagnies aériennes (gestion des coûts fixes et des couvertures de carburant).
  * *Airbnb* (exemple d'introduction en bourse en novembre 2020 et de résilience face à la crise hôtelière).
  * *Salesforce*, *Pixar*, *Star Wars*, *Miramax / Harvey Weinstein*, *Six Flags*, *Midwestern Cedar*, *King World*, *Nielsen*.
* **Outils / Bases de données cités :**
  * *S&P Capital IQ* (mentionnée comme source pour télécharger les données financières et calculer les bêtas, la capitalisation boursière, la dette, etc.).
* **Précision :** Tous ces noms d'entreprises et bases de données sont utilisés **à titre pureté pédagogique et d'illustration** par l'intervenant (Aswath Damodaran) dans le cadre de ses cours universitaires de finance d'entreprise ; il ne s'agit en aucun cas de placements publicitaires.
