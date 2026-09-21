# Lancement — verticale choisie : **les e-commerçants français**

> Décision prise le 21/09/2026, sur le critère que vous avez fixé : **maximiser
> le revenu, à condition que le marché soit stable ou porteur**, sans exclure
> aucun secteur pour une autre raison.
>
> Votre refus des artisans est d'ailleurs cohérent avec ce critère et je l'ai
> intégré : ce marché est **en recul** (13 trimestres consécutifs de baisse,
> 3 619 défaillances au T2 2026). Il ne passait pas votre condition.

---

## Ce que dit le calcul, avant de parler d'intuition

J'ai rejoué le classement des 15 concepts avec une grille pondérée **presque
uniquement sur l'argent et la solidité du marché** (valeur commerciale 5,
revenu récurrent 5, durabilité 5, affiliation 4, croissance 4, revente 3) :

```bash
cd ai-business-lab/outils
python scorer.py --criteres criteres-max-revenu.yaml
```

| Grille de référence | Grille « revenu maximal » |
|---|---|
| 1. A4 Newsletter de veille (81.4) | 1. **A2 IA appliquée à un métier (82.3)** |
| 2. A2 IA appliquée à un métier (78.9) | 2. A3 Création d'entreprise (82.0) |
| 3. A1 Facture électronique (78.3) | 3. A4 Newsletter de veille (81.4) |
| … | … |
| 13. D2 Chaîne finance (61.4) | **11. D2 Chaîne finance (64.5)** |

**Le résultat le plus utile est celui qui ne bouge pas.** Même en optimisant
presque exclusivement l'argent, la chaîne finance — qui a pourtant **le meilleur
RPM mesuré du marché français (8-15 €)** — reste 11ᵉ sur 15. Parce qu'un RPM
élevé ne compense pas une concurrence maximale et un cadre juridique strict.
Autrement dit : **il n'existe pas de raccourci que le classement cacherait.**

La forme retenue est donc **A2 + A4 + B2** : un média d'expertise sur les outils
d'un métier, diffusé par une newsletter, monétisé par un comparateur.

Reste à choisir le métier. Il doit être : solvable, équipé en logiciels
d'abonnement, sur un marché **en croissance**, et accessible en ligne.

---

## Le métier retenu : e-commerçants français

### Le marché est stable et en croissance — votre condition

**[DONNÉE]** FEVAD, chiffres 2026 :
- **196,4 milliards d'euros** de ventes en ligne, **+7 % sur un an** ;
- **158 200 sites e-commerce actifs**, **+7 % sur un an** ;
- 50,1 Md€ au T1 2026, **+4,7 %** sur un an ;
- panier moyen 62 €, la croissance venant désormais de la **fréquence d'achat**
  plus que du panier.

**[DONNÉE]** Marché du numérique français : **74,3 Md€ en 2026, +4,3 %**, l'IA
en étant le principal moteur. **22 % des petites entreprises françaises
utilisent déjà l'IA générative**, et la grande majorité manque d'accompagnement.

**[OPINION]** C'est exactement la configuration recherchée : un marché qui
grossit, une population qui grossit **plus vite que le marché lui-même** (158 200
sites, +7 %), et un besoin déclaré et non servi.

### L'audience achète des logiciels par abonnement — donc l'affiliation est récurrente

**[DONNÉE]** Programme partenaire Shopify : **20 % de commission récurrente** sur
l'abonnement mensuel des marchands référés, avec des revenus récurrents sur
4 ans — là où l'affiliation simple plafonne à 150 $ par recommandation.
Brevo : récompense par client référé, versements mensuels automatisés via
PartnerStack, **cookie de 90 jours** ; tarifs à partir de 25 €/mois pour
5 000 contacts.

**[ESTIMATION]** Sur un abonnement Shopify à ~30 €/mois, 20 % récurrents = **6 €
par mois et par marchand**. **100 marchands actifs ≈ 600 €/mois récurrents**, qui
continuent de tomber sans publier davantage. Ajoutez les outils satellites
(email, logistique, comptabilité, IA) et le même lecteur rapporte deux à quatre
fois plus.

### Il y a une vraie matière de veille hebdomadaire

**[DONNÉE]** Ce qui bouge pour un e-commerçant français :
- **TVA** : seuil de 10 000 € pour les ventes B2C dans l'UE, guichets OSS/IOSS,
  responsabilité des marketplaces, cas du dropshipping importé ;
- **Droit de rétractation** : depuis le **19/06/2026**, obligation de fournir un
  mécanisme simplifié permettant au consommateur d'exercer sa rétractation
  **directement en ligne** (bouton dédié) ;
- **DSA** : applicable depuis le 17/02/2024 à tout fournisseur de service
  intermédiaire — y compris un site qui publie des avis clients ;
- **Facturation électronique** : plateformes agréées, calendrier 2026-2027 ;
- **Outils et IA** : le fil le plus régulier, et celui qui porte la monétisation.

### La valeur commerciale est élevée

**[DONNÉE]** RPM France : **5-12 €** en business/entrepreneuriat, **5-10 €** en
tech/logiciel (6-12 € en B2B) — contre 2-5 € en divertissement. Sponsoring de
newsletter B2B : **150 à 800 € l'insertion**. Les éditeurs d'outils e-commerce
sont nombreux, solvables et habitués à payer pour de l'acquisition.

---

## Les deux signaux négatifs, écrits noir sur blanc

**1. La masse des e-commerçants a peu de budget.**
**[DONNÉE]** 1 % des acteurs génèrent **78 %** du chiffre d'affaires du secteur ;
**69 % des sites réalisent moins de 100 000 € de CA annuel**.
→ *Conséquence assumée* : la cible n'est pas « les gros ». C'est justement cette
masse de petites boutiques, pour qui un outil à 30 €/mois est une décision
réfléchie — donc quelqu'un qui **cherche activement un comparatif avant
d'acheter**. C'est une bonne nouvelle pour le comparateur, une mauvaise pour le
produit cher.

**2. Le créneau est saturé de vendeurs de formations.**
« E-commerce » et « dropshipping » sont parmi les sujets les plus exploités du
web francophone, souvent par des gens qui gagnent leur vie en vendant la méthode
plutôt qu'en vendant des produits.
→ *Conséquence assumée* : **l'angle n'est pas « gagner de l'argent en ligne ».**
C'est **« les outils, les vrais prix, les obligations »** : tests réels, tarifs
constatés, échéances légales. C'est précisément ce que les vendeurs de formation
ne font pas, et c'est ce qui rend la position défendable.

**3. La croissance ralentit** : +4,7 % au T1 2026 contre +8,3 % au T1 2025. Le
marché reste porteur, mais il n'accélère plus. À surveiller trimestriellement ;
si la croissance passe sous zéro deux trimestres de suite, la verticale est à
réexaminer — c'est votre propre critère.

---

## Ce qui est décidé

| Élément | Décision |
|---|---|
| **Verticale** | E-commerçants français, en priorité les sites de moins de 100 k€ de CA |
| **Concept principal** | A4 — newsletter hebdomadaire |
| **Monétisation n°1** | Affiliation **récurrente** sur les outils (Shopify 20 % récurrent, Brevo, satellites) |
| **Monétisation n°2** | B2 — comparateur d'outils avec prix réels |
| **Acquisition (test)** | D1 — 30 contenus courts, jetables |
| **Angle** | Les outils, les vrais prix, les obligations. **Jamais** « comment devenir riche en ligne » |
| **Promesse** | 5 minutes par semaine pour ne rien rater et ne pas payer trop cher |
| **Nom provisoire** | *La Fiche Produit* — **à vérifier** (domaine + antériorité INPI) avant toute communication |

---

## Plan des 30 premiers jours

### Jours 1-7 — préparation, rien de public
1. Compte beehiiv + **page d'inscription seule** en ligne.
2. S'inscrire au **programme partenaire Shopify** et aux programmes satellites :
   [`04-affiliation.md`](04-affiliation.md).
3. Mettre en place la veille : [`01-sources-de-veille.md`](01-sources-de-veille.md).
4. Écrire les **4 premiers numéros** : [`02-newsletter.md`](02-newsletter.md).
5. Vérifier le nom (domaine + INPI), rédiger les mentions légales.

### Jours 8-30 — publication
6. **1 numéro par semaine**, sans exception, même à 12 abonnés.
7. **Pages du comparateur**, déjà rédigées : [`comparateur/`](comparateur/) — méthode et critères dans [`03-comparateur.md`](03-comparateur.md).
8. **1 contenu court par jour** : [`05-contenus-courts.md`](05-contenus-courts.md).

### Seuils écrits à l'avance (J+60)
- **H1** : ≥ 300 inscrits et ≥ 40 % d'ouverture.
- **H5** : ≥ 3 % de clics sortants et ≥ 1 conversion d'affiliation payante.
- **H4** : ≥ 3 vidéos > 10 000 vues et ≥ 100 inscrits attribués.
En dessous : on applique la règle de KILL, le jour même.

---

## Une chose à dire clairement sur l'objectif

Vous avez répondu trois fois « ce qui rapporte le plus, je veux devenir riche ».
C'est un objectif légitime, et il oriente réellement les choix ci-dessus — c'est
pour ça que la grille « revenu maximal » existe désormais dans le dépôt.

Mais aucun de ces concepts ne produit de la richesse en 12 mois, et je ne vous
promets aucun rendement. Ce qu'ils peuvent produire, dans le meilleur des cas :
**un actif à revenu récurrent**. La richesse éventuelle vient ensuite de deux
mécanismes, pas des vues : la **récurrence qui s'empile** (100 marchands référés
qui paient tous les mois sans travail supplémentaire) et la **revente de l'actif**
à un multiple de son bénéfice, à 3-5 ans. C'est exactement ce que pondère la
grille — `revenu_recurrent` et `revente_actif` — et c'est pourquoi elle écarte
les formats faceless les plus « faciles », qui ne produisent ni l'un ni l'autre.

---

## Sources

- [FEVAD — Chiffres clés e-commerce 2026](https://www.fevad.com/chiffres-cles-ecommerce-2026/)
- [FEVAD — E-commerce au 1ᵉʳ trimestre 2026](https://www.fevad.com/e-commerce-au-1er-trimestre-2026-croissance-globalement-preservee-malgre-un-environnement-incertain/)
- [ecommerce-nation — Bilan FEVAD : marché à 196,4 milliards d'euros](https://www.ecommerce-nation.fr/chiffres-cles-ecommerce-france-2026-fevad/)
- [Bpifrance — 7 secteurs porteurs en 2026](https://bigmedia.bpifrance.fr/nos-dossiers/7-secteurs-porteurs-en-2026-pour-la-creation-de-son-entreprise-ou-investir-et-innover)
- [Speed Ecom — Shopify Partner 2026 : guide du programme partenaire](https://speed-ecom.eu/blog/devenir-partenaire-shopify-avantages-collaboration-et-guide-complet-pour-rejoindre-programme/)
- [AffyList — Brevo affiliate program 2026](https://affylist.com/products/brevo)
- [Haas Avocats — E-commerce & plateformes : les obligations juridiques en 2026](https://www.haas-avocats.com/e-commerce-plateformes-les-obligations-juridiques-en-2026/)
- [PrestaShop — 2026 : quelles évolutions réglementaires pour le e-commerce](https://prestashop.com/blog/legal/2026-what-regulatory-changes-are-coming-for-ecommerce/)
- [Keobiz — TVA e-commerce 2026 : règles et obligations](https://www.keobiz.fr/le-mag/tva-e-commerce/)
- [donneespersonnelles.fr — DSA : obligations des plateformes en ligne](https://www.donneespersonnelles.fr/dsa-obligations-plateformes)
- [fluxnote — YouTube CPM France 2026](https://fluxnote.io/guides/youtube-cpm-france-2026)
- [Nénuphar Studio — Sponsoring de newsletter : combien facturer](https://www.nenuphar-studio.com/le-sponsoring-de-newsletter-combien-facturer-selon-la-taille-de-sa-liste)

> **Avertissement de méthode** : les faits réglementaires cités proviennent de
> sources secondaires spécialisées. Avant publication, chacun doit être
> revérifié sur sa source officielle (Légifrance, service-public.fr,
> impots.gouv.fr, Commission européenne). C'est la règle R3 du registre des
> risques.
