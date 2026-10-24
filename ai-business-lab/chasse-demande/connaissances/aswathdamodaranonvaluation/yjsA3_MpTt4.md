# Session 13: Incremental Cashflows and Dealing with Uncertainty

Vidéo : https://youtu.be/yjsA3_MpTt4 · durée 1:21:34 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-24
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé demandé de la vidéo, structuré comme une fiche de connaissances en finances personnelles (et d'entreprise) :

---

# Fiche de connaissances : Évaluation de projets et analyse des flux de trésorerie (Corporate Finance)

## 1. Sujet et thèse principale
* **Sujet :** L'évaluation de projets d'investissement en entreprise, l'analyse des flux de trésorerie incrémentaux, le traitement des coûts (sunk costs, coûts alloués), ainsi que les méthodes d'actualisation (NPV, IRR) et la gestion de l'incertitude.
* **Thèse principale :** L'évaluation financière d'un projet doit se baser uniquement sur les flux de trésorerie futurs et **incrémentaux** (ce qui change si on prend le projet par rapport à si on ne le prend pas), en évitant les biais psychologiques (coûts irrécupérables) et en maintenant une stricte cohérence dans les monnaies et taux d'actualisation utilisés.

---

## 2. Notions expliquées (définitions simples)
* **Cash-flows incrémentaux (Incremental Cash Flows) :** Flux de trésorerie additionnels générés directement et uniquement par l'acceptation d'un projet. Règle de décision : comparer « avec projet » versus « sans projet ».
* **Coûts irrécupérables (Sunk Costs) :** Dépenses déjà engagées dans le passé et impossibles à récupérer, quel que soit le choix d'accepter ou de rejeter le projet. Ils ne doivent **pas** être inclus dans l'analyse.
* **Coûts alloués (Allocated Costs) :** Frais généraux (G&A) répartis artificiellement entre les départements ou projets. Seule la part incrémentale (qui change réellement) doit être prise en compte.
* **Actualisation (Discounting) :** Ramener des flux de trésorerie futurs à leur valeur actuelle pour tenir compte de la valeur temporelle de l'argent.
* **Valeur résiduelle / de liquidation (Salvage Value) :** Produit attendu de la revente de l'ensemble des actifs d'un projet à la fin de sa vie (ex : fermeture du parc).
* **Valeur terminale (Terminal Value) :** Valeur actualisée de tous les flux de trésorerie futurs se produisant après une période de prévision explicite (en supposant souvent une croissance à long terme).
* **NPV (Net Present Value / Valeur Actuelle Nette) :** Somme des valeurs actuelles de tous les flux de trésorerie du projet, y compris l'investissement initial, actualisés au coût du capital. Règle : accepter si $\text{NPV} > 0$.
* **IRR (Internal Rate of Return / Taux de Rentabilité Interne) :** Taux d'actualisation qui rend la valeur actuelle nette (NPV) exactement égale à zéro. Règle : accepter si $\text{IRR} > \text{coût du capital (hurdle rate)}$.
* **Parité de pouvoir d'achat (Purchasing Power Parity - PPP) :** Théorie utilisée pour prévoir les taux de change futurs en fonction des différences d'inflation entre deux pays.

---

## 3. Chiffres, taux, plafonds et règles fiscales citées
* **Taux d'impôt (Rio Disney Theme Park) :** $36{,}1\%$ (mentionné comme taux d'imposition pour le projet).
* **Taux d'impôt (Vale Iron Ore Mine) :** $34\%$ de taux d'imposition corporatif pour ce projet.
* **Coût du capital (Disney / Rio) :** $8{,}46\%$ (utilisé comme taux d'actualisation de base).
* **Inflation :**
  * Brésil : $9\%$
  * États-Unis : $2\%$
  * Différentiel d'inflation (Brésil vs US) : environ $7\%$ de dépréciation annuelle du Real par rapport au dollar.
* **Règles fiscales et légales :** *À vérifier à la source officielle* pour toute application en situation réelle (les règles fiscales et comptables locales varient selon les juridictions et les lois en vigueur).

---

## 4. Conseils concrets et leurs limites ou risques
* **Règle des deux questions pour les coûts :** Toujours se demander « Qu'arrive-t-il si je prends le projet ? » et « Qu'arrive-t-il si je ne le prends pas ? ». Si la réponse est identique, le coût n'est pas incrémental.
* **Piège des coûts irrécupérables :** Ne pas se laisser influencer psychologiquement par l'argent déjà dépensé dans le passé (biais d'engagement ou coût sunk).
* **Cohérence monétaire (Règle de consistance) :** Si les flux sont en dollars, le taux d'actualisation doit être en dollars ; si les flux sont nominaux (ou réels), le taux doit l'être également. Mélanger les monnaies sans parité détruit la précision de l'évaluation.
* **Limites de l'IRR :** L'IRR suppose implicitement que les flux intermédiaires sont réinvestis au taux de l'IRR lui-même (ce qui est souvent irréaliste pour des projets à très haut rendement), contrairement à la NPV qui suppose un réinvestissement au coût du capital.
* **Incertitude et simulations :** Plutôt que de s'appuyer sur des chiffres uniques (point estimates), utiliser des simulations (type Monte-Carlo) pour obtenir une **distribution** de probabilités de la NPV et identifier les risques de pertes (ex : $12\%$ de chance d'avoir une NPV négative).

---

## 5. Produits, applications ou entreprises cités
* **Disney / Disney+ / Mandalorian / WandaVision / Avengers :** Exemples utilisés pour illustrer l'évaluation de parcs à thèmes (Rio) et la rentabilité de séries de streaming (mentionnés à des fins pédagogiques, pas de placement publicitaire).
* **Netflix :** Cité comme principal concurrent dans le secteur du streaming et de la production de contenu.
* **Microsoft / Activision :** Mentionné comme exemple d'acquisition dont la capitalisation boursière a chuté le jour de l'annonce en raison d'une perception de surpaiement par les investisseurs.
* **Tableau (Logiciel) :** Cité comme entreprise de visualisation de données.
* **Crystal Ball :** Logiciel complémentaire d'Excel utilisé pour réaliser des simulations de Monte-Carlo et analyser des distributions de probabilité (présenté par l'auteur comme un outil pédagogique et professionnel utile).
