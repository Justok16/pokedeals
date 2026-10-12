# Les cours de bourse sont-ils truqués ? (et si oui comment s’en apercevoir)

Vidéo : https://youtu.be/i1yzA1SZEMw · durée 12:37 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale** : Présentation et explication de la **loi de Benford** (ou loi des nombres anormaux), appliquée à différents jeux de données de la vie réelle (cours boursiers, populations, données du *New York Times*). La thèse principale est que, contre toute intuition d'une répartition uniforme, le chiffre 1 apparaît beaucoup plus fréquemment (environ 30 % du temps) comme premier chiffre significatif dans de nombreux ensembles de données naturelles et financières, ce qui en fait un outil puissant pour détecter des anomalies ou des fraudes.

2) **Notions expliquées** :
- **Loi de Benford** : Loi mathématique décrivant la fréquence d'apparition du premier chiffre non nul (de 1 à 9) dans de nombreuses séries de données statistiques. Le chiffre 1 apparaît le plus souvent (~30%), et le chiffre 9 le moins souvent (~5%).
- **Effet d'échelle** : Propriété mathématique selon laquelle la loi de Benford est indépendante de l'unité de mesure choisie (par exemple, que l'on exprime des prix en dollars ou en euros, la proportion des premiers chiffres reste la même).
- **Détection de fraude** : Utilisation de la loi de Benford pour identifier des falsifications de comptes ou de données financières (les fraudeurs générant des chiffres "au hasard" ou de manière non naturelle violent généralement cette distribution).

3) **Chiffres, taux, plafonds et règles fiscales** :
- **Fréquences théoriques de la loi de Benford** :
  - Chiffre 1 : ~30,1 %
  - Chiffre 2 : ~17,6 %
  - Chiffre 3 : ~12,5 %
  - Chiffre 4 : ~9,7 %
  - Chiffre 5 : ~7,9 %
  - Chiffre 6 : ~6,7 %
  - Chiffre 7 : ~5,8 %
  - Chiffre 8 : ~5,1 %
  - Chiffre 9 : ~4,6 %
- **Exemples chiffrés présentés** :
  - Expérience sur les 15 premières pages du *New York Times* (213 données) : respecte globalement la décroissance de la loi de Benford.
  - S&P 500 (cours boursiers des 500 plus grandes entreprises américaines) analysé sur Excel : le chiffre 1 apparaît à environ 33 % du temps, le chiffre 2 à 14,7 %, etc., ce qui corrobore la loi de Benford.
- *Règle fiscale / légale* : Non applicable (sujet purement mathématique et statistique).

4) **Conseils concrets, limites et risques** :
- **Conseils** : Pour tester la loi de Benford sur vos propres données (ex. tableur Excel), vous pouvez extraire le premier chiffre (fonction GAUCHE ou LEFT) et compter les occurrences (NB.SI ou COUNTIF) pour comparer la distribution obtenue à la courbe théorique de Benford.
- **Limites / Risques** : La loi de Benford ne s'applique pas si les données possèdent des contraintes d'échelle strictes (par exemple, des tailles d'humains en centimètres qui commencent toutes par 1 ou 2, ou des données limitées dans une plage étroite). Des arrondis systématiques (ex. dividendes arrondis par des entreprises) ou des comportements fiscaux spécifiques peuvent également créer des écarts qui ne signifient pas nécessairement une fraude.

5) **Produits, applications ou entreprises cités** :
- **Outils logiciels** : Excel (pour le traitement et l'analyse statistique des données).
- **Sources de données** : *New York Times*, S&P 500, données démographiques (comtés américains).
- *Nature* : Vulgarisation scientifique et mathématique (aucun produit commercialisé ou promu).

---
