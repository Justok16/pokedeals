# Séance 5 : (Étudiants en évaluation financière) Suite sur les taux sans risque et premiers pas su...

Vidéo : https://youtu.be/Pe7yV1-7iw8 · durée 1:17:00 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

# Fiche de connaissances : Implied Risk Premium Tests & Risk-Free Rates

## 1. Sujet et thèse principale
* **Sujet :** L’estimation du taux sans risque (*Risk-Free Rate*) et de la prime de risque sur actions (*Equity Risk Premium* ou ERP) à travers différentes zones géographiques et devises, notamment en tenant compte de l’inflation, des spreads souverains et de l'exposition des entreprises multinationales.
* **Thèse principale :** Pour évaluer correctement un investissement international, le taux sans risque doit être estimé dans la devise des flux de trésorerie prévus, et la prime de risque doit refléter la réalité opérationnelle et géographique de l’entreprise (où elle opère), plutôt que de se fier uniquement à des moyennes historiques biaisées ou au pays d’incorporation.

---

## 2. Notions expliquées
* **Taux sans risque (*Risk-Free Rate*) :** Le rendement théorique d’un investissement sans risque de défaut (généralement basé sur les obligations d’État). Il doit être aligné sur la devise des flux de trésorerie évalués.
* **Spread de défaut souverain (*Default Spread*) :** La différence entre le taux d’intérêt d’une obligation émise par un gouvernement en devise étrangère et le taux des obligations souveraines des États-Unis (US T-Bond).
* **Prime de risque sur actions (*Equity Risk Premium* - ERP) :** Le rendement supplémentaire exigé par les investisseurs pour investir dans des actions par rapport à un actif sans risque.
* **Moyenne arithmétique vs géométrique :** Deux méthodes pour calculer les rendements historiques. L'arithmétique tend à surestimer les rendements futurs à long terme, tandis que la géométrique est plus conservative.
* **Biais de survie (*Survivorship Bias*) :** Biais statistique qui consiste à n'étudier que les marchés qui ont réussi (ex. les actions américaines au XXe siècle), ce qui surestime la prime de risque historique.
* **Approche par volatilité (*Equity Volatility-Based Approach*) :** Méthode pour estimer l'ERP d'un pays en multipliant la prime de risque américaine par le ratio des écarts-types (volatilité) du marché boursier du pays par rapport au marché américain.

---

## 3. Chiffres, taux, plafonds et règles fiscales citées
*(Attention : Ces chiffres datent de janvier 2024 ou de données historiques présentées dans la conférence et doivent impérativement être vérifiés auprès de sources financières officielles avant toute décision d'investissement).*

* **Exemple de la multinationale suisse (02:30) :**
  * Taux sans risque : 0,5 % en francs suisses, 1 % en euros, 2,5 % en USD, 6 % en roupies indiennes.
* **Exemple de l'Inde (janvier 2024) (10:50) :**
  * Taux des obligations en roupies : 7,18 %
  * Spread de défaut pour une notation Baa3 : 2,39 %
  * Taux sans risque net en roupies : 4,78 % (via l'approche de déduction du spread).
* **Exemple du Brésil (janvier 2024) (15:10) :**
  * Taux des obligations en USD : 5,75 %
  * Taux sans risque USD (T-Bond) : 3,88 %
  * Spread de défaut du gouvernement : 1,87 %
  * Spread CDS (Credit Default Swap) : 1,81 %
  * Spread basé sur la notation (Ba2) : 3,28 %
* **Prime de risque historique aux États-Unis (1928-2023) (07:12) :**
  * Rendement des actions : ~8,32 % (arithmétique) / 6,50 % (géométrique)
  * Rendement des T-Bonds : ~3,88 %
  * ERP historique : ~4,40 % à 7 % selon la période et la méthode.
* **Taux d'inflation et de croissance (exemples théoriques) :**
  * Taux d'inflation égyptien (historique cité) : 15 %
  * Taux d'inflation USD : 1,5 %
* **Exemples de notations souveraines et spreads (janvier 2024) :**
  * Singapour : Noté Triple A (AAA), considéré comme l'une des rares références étatiques stables en Asie.
  * Laos / Sri Lanka : Exemples de pays à risques accrus ou en défaut de gouvernance récente.

---

## 4. Conseils concrets, limites et risques
* **Ne jamais utiliser de taux sans risque « pondérés » ou « moyennés »** entre plusieurs devises (ex. moyenner le taux suisse, américain et indien n'a aucun sens économique).
* **Éviter de se fier uniquement aux primes historiques à court terme** (ex. 1 an), car la volatilité est trop forte (erreur type trop élevée). Préférer des horizons longs (50 ou 100 ans) tout en gardant en tête les biais inhérents.
* **Ne pas estimer le risque d'un pays uniquement par son pays d'incorporation :** Une entreprise européenne réalisant 90 % de son chiffre d'affaires dans des pays émergents à hauts risques ne doit pas utiliser le taux sans risque européen pur.
* **Risque de change et d'inflation :** L'inflation dicte les écarts de taux sans risque entre les monnaies. Des devises à forte inflation affichent des taux nominaux élevés, mais cela n'augmente pas la valeur réelle des flux futurs si l'inflation est correctement intégrée.

---

## 5. Produits, applications ou entreprises cités
* **Entreprises et marques mentionnées à titre d'illustration pédagogique :**
  * *Nestlé* (multinationale suisse)
  * *Coca-Cola* (analyse de la répartition géographique des revenus)
  * *Ambev* et *Embraer* (exemples brésiliens pour illustrer l'exposition aux risques pays par le chiffre d'affaires)
  * *Lehman Brothers* (mentionné pour la crise financière de 2008 et l'effondrement du marché des CDS).
* **Outils / Sources de données mentionnés :**
  * *Terminaux Bloomberg* (mentionné pour l'accès aux spreads CDS via la commande `SOVR`).
  * *Fonds monétaire international (FMI)* et bases de données macroéconomiques mondiales.
* **S'agit-il de publicité ?** Non. Il s'agit d'un cours universitaire magistral (probablement du Professeur Aswath Damodaran de la Stern School of Business de l'Université de New York). Aucun produit commercial n'est vendu ou promu.
