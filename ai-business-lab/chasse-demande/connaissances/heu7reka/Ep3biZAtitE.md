# ⚡ Pourquoi fixer le prix sur la centrale la plus chère ? Comprendre le modèle

Vidéo : https://youtu.be/Ep3biZAtitE · durée 1:12:47 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

# Fiche de connaissances : Le marché de l'électricité (et ses limites économiques)

## 1. Sujet et thèse principale
* **Sujet :** Le fonctionnement du marché de l’électricité en Europe (marché de gros, marché SPOT, merit order, coûts fixes vs. coûts variables, marché de capacité et subventions/AOLT).
* **Thèse principale :** Le système de marché de l’électricité européen prétend optimiser la sélection des centrales par le coût marginal (via le *merit order*), mais il présente des limites structurelles majeures (absence de prise en compte correcte des coûts fixes, volatilité extrême des prix liée aux énergies fossiles et risque de manipulation). L'auteur démontre, à travers les modèles mathématiques (notamment inspirés de Marcel Boiteux), que la tarification au coût marginal ne permet de rembourser l'ensemble des coûts (fixes et variables) du parc qu'à la stricte condition d'être « au creux de la vague » (lorsque la demande est parfaitement calibrée sur l'optimal). En dehors de cela, cela génère soit des profits excessifs pour certaines technos (comme le nucléaire lors des pics), soit des situations intenables pour le marché.

---

## 2. Notions expliquées (définitions simples)
* **Marché SPOT :** Marché de gros où s'achète et se vend l'électricité à court terme.
* **Coût fixe :** Coûts engagés une fois pour toutes (construction de la centrale, salaires, maintenance, intérêts de la dette, dividendes), indépendants de la quantité produite à court terme.
* **Coût variable :** Coûts qui dépendent directement de la quantité produite (essentiellement les combustibles : charbon, gaz, uranium, etc.).
* **Merit Order :** Classement des centrales de production d'électricité par ordre croissant de leurs coûts variables (du moins cher au plus cher) pour répondre à la demande.
* **Pay as clear :** Mode de fixation du prix où toutes les centrales retenues sont payées au prix de la dernière centrale appelée (celle fixant le prix marginal).
* **Pay as bid :** Mode de fixation où chaque centrale est payée au prix qu’elle a déclaré.
* **Coût marginal :** Coût de production d'une unité supplémentaire d'électricité (sur le marché SPOT, il correspond au coût variable de la dernière centrale appelée).
* **STEP (Station de Transfert d'Énergie par Pompage) :** Installation hydraulique de stockage d'énergie par pompage d'eau vers un bassin supérieur.
* **ARENH (Accès Régulé à l'Électricité Nucléaire Historique) :** Dispositif français obligeant EDF à revendre une partie de son électricité nucléaire historique à ses concurrents à un prix administré (*non précisé dans le détail chiffré récent*).
* **Marché de capacité :** Marché additionnel récompensant la disponibilité des capacités de production pour garantir la sécurité d'approvisionnement en période de pic.
* **AOLT (Appels d’Offre de Long Terme) :** Appels d'offres pour soutenir le développement de certaines filières de production (ex. renouvelables).
* **Effacement :** Action pour un consommateur (industriel ou particulier) de réduire ou de couper sa consommation d'électricité à la demande du réseau en échange d'une compensation financière.
* **Missing money :** Problème économique où les revenus du marché SPOT ne suffisent pas à couvrir les coûts fixes des investissements dans de nouvelles capacités de production.
* **Hypothèse d'information parfaite / de la centrale (dé)gonflable :** Modèles théoriques permettant de simuler l'optimisation d'un parc de production en fonction des variations de la demande et des coûts.

---

## 3. Chiffres, taux, plafonds et règles cités (avec années)
* *Exemple fictif (technologies A, B, C) :* Centrale A (10 €/MWh), B et C (100-150 €/MWh).
* *Exemple de STEP fictif :* 300 MWh effacés/stockés à 500 €/MWh pour un coût total de 385 000 €.
* *Exemple chiffré de simulation (partie théorique avec Marcel Boiteux) :*
  * Centrale nucléaire : Coût fixe 300 000 €/MW/an, Coût variable 10 €/MWh.
  * Centrale à gaz : Coût fixe 60 000 €/MW/an, Coût variable 50 €/MWh (puis 1 000 €/MWh en pointe selon les exemples).
  * Effacement : 3 000 €/MWh.
* *Consommation en France (2020, source RTE citée) :*
  * Consommation totale : ~445,8 TWh (*non précisé pour l'année exacte dans certains graphiques, mais mentionné pour 2019 à 470 TWh et 2020*).
  * Heures de consommation : 8 760 heures par an.
  * Puissance du parc installé en France (2020) : Nucléaire ~44 241 MW (44,2 GW) ; Gaz ~36 419 MW (36,4 GW). *(À vérifier à la source officielle RTE).*
* *Facture globale de l'électricité en France (2020, simulation) :* ~22,796 milliards d'euros pour 445,8 TWh, soit un prix moyen de ~51,13 €/MWh.
* *Prix des capacités sur le marché (données graphiques RTE citées) :*
  * Années 2017 à 2022 : forte volatilité (ex. pic notable en 2021 autour de 35 000-40 000 €/MW, puis baisse en 2022). *(À vérifier à la source officielle RTE).*
* *AOLT 2020-2026 :* Prix garanti proposé pour les batteries/effacements autour de 20 000 €/MW.
* *AOLT 2021-2027 / 2022-2028 :* Prix garantis autour de 30 000 €/MW.
* *Exemple de la centrale de Landivisiau (Cycle Combiné Gaz) :*
  * Projet : 2012, Construction : 2019-2022, Mise en service : mars 2022.
  * Puissance : 446 MW.
  * Acteurs : Siemens (construction), Total (exploitation).
  * Capacité garantie : 94 000 €/MW sur 20 ans. *(À vérifier à la source officielle).*

---

## 4. Conseils concrets et leurs limites ou risques
* **Comprendre la complexité du marché :** Ne pas écouter simpliste les discours affirmant que « sans le marché, on aurait des black-outs » ou inversement que « le marché fixe le juste prix ». Les interconnexions européennes existaient avant le marché unifié de gros.
* **Limites du modèle de tarification marginale (*Pay as clear*) :** Il enrichit artificiellement certaines technologies (comme le nucléaire ou l'éolien/solaire dont les coûts variables sont très faibles) lors des pics de prix dictés par les énergies fossiles (gaz/charbon).
* **Risque systémique :** L'incapacité du marché SPOT à couvrir les investissements de long terme (coûts fixes) nécessite des rustines (marché de capacité, subventions AOLT, ARENH), ce qui complexifie et politise l'ensemble du système énergétique.

---

## 5. Produits, applications ou entreprises cités
* **EDF :** Mentionné comme acteur historique (monopole d'État avant l'ouverture à la concurrence, puis opérateur soumis au marché et à l'ARENH). *(Pas de publicité, mention institutionnelle/historique).*
* **Enron :** Mentionné comme exemple historique de manipulation de marché (aux États-Unis dans les années 2000). *(Pas de publicité).*
* **Siemens et Total :** Mentionnés pour la construction et l'exploitation de la centrale à cycle combiné gaz de Landivisiau. *(Pas de publicité).*
* **Utip et Tipeee :** Mentionnés par le créateur de la vidéo comme plateformes de soutien financier participatif de sa chaîne. *(Publicité pour le financement de la chaîne de l'auteur).*
