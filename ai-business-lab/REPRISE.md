# REPRISE — état d'avancement

> **Ce fichier est le point d'entrée après toute interruption** (fin de tokens,
> coupure, session en veille, conteneur recyclé). Consigne permanente de
> l'utilisateur : **reprendre le travail dès que possible, sans attendre qu'il
> relance.**
>
> Il est versionné, donc il survit à la mort du conteneur — contrairement à
> tout ce qui n'est que dans `/home/user`.
>
> **Dernière mise à jour : 23/09/2026, 06h40**

---

## Consignes de travail de l'utilisateur

- **Reprendre le travail dès que possible** après toute interruption, sans
  attendre qu'il relance.
- **Toujours donner le lien DIRECT de la page** quand on lui demande d'aller
  quelque part — jamais la page d'accueil d'un site à charge pour lui de
  chercher. Quand un lien direct n'existe pas (recherche INPI, recherche de
  domaine chez un registrar), le dire explicitement et indiquer exactement quoi
  taper une fois sur place.
- Faire **absolument tout** ce qui est à portée, ne revenir vers lui que si
  c'est absolument nécessaire.
- **Économiser les tokens — ils lui coûtent de l'argent.** Trois règles, posées
  le 21/09/2026 après une refonte visuelle faite en trois passes :
  1. **Sur un sujet subjectif** (design, ton, nom), poser **une** question de
     direction avant de produire. Une question coûte cent fois moins que trois
     itérations.
  2. **Messages de commit courts.** Le raisonnement va dans les fichiers du
     dossier, qui sont durables et relus ; le dupliquer dans l'historique git
     est un pur gaspillage.
  3. **Réponses courtes.** Livrer le résultat et le lien, pas le récit du
     travail. Il voit les fichiers.

---

## Où en est le projet

### Instantané du 23/09/2026, matin — lire ceci EN PREMIER

**Cinq audits reçus et contre-lus** (`audit-externe/00-synthese.md` d'abord).
Verdict unanime : MODIFIER.

**Décisions de l'utilisateur (23/09)** : distribution publique acceptée
(30-45 min/jour, 7 jours) ; identité donnée en privé aux organismes qui
paient ; ~10 €/an de domaine dès le premier euro ; **déménagement de DigCost
vers un compte GitHub séparé** — ✅ **FAIT le 23/09** : site sur
**https://digcost.github.io/**, source privée. Voir `migration-digcost/README.md`.
✅ Liens de l'email de bienvenue beehiiv corrigés (23/09). ✅ Search Console :
propriété `https://digcost.github.io/` validée, sitemap envoyé (23/09).
Demande d'indexation refusée par Google (« erreur, réessayez ») : même
incident que le 22/09, à retenter plus tard, non bloquant.

**Règle d'arrêt révisée** (`14-regle-de-kill.md`) : décision avancée au
**06/10** sur trois signaux (distribution, affiliation, retours marchands).

**Recommandation retirée** : ne jamais rendre `pokedeals` privé (quota
Actions, PokéDeals s'arrêterait).

**Restent à faire** : captures Shopify (grille /fr/tarifs, conditions 5.5,
5.6, 15.2, page affiliation) ; calculateur étendu à Grow/Advanced avec seuil
de changement de formule ; candidature affiliation ; brouillons de réponses
publiques pour la distribution ; mentions légales et confidentialité.

### Instantané du 23/09/2026, nuit

**Trois audits externes reçus** (DeepSeek, Grok, ChatGPT), contre-lus dans
`audit-externe/02` à `04`. Verdict unanime : **MODIFIER**. Mistral : partie 1
reçue seulement, en attente de la partie 2. **Synthèse et décisions à faire
quand tous les retours sont là.**

Corrigé le 23/09 : affirmations non sourcées du site, bug du calculateur
(double comptage en mode prestataire externe), incohérence 952/1 012 €,
balises canoniques, erreur de calcul du levier patrimoine (0,8 à 2, pas 10),
alias d'adresse de test exposés, fin d'essai beehiiv = ~05/10. **EmpCo
déclassée** (hors sujet pour le site, 0 abonné).

**Le constat central** : Shopify prévient ses marchands 30 jours avant de
changer ses frais, et son affiliation ne paie qu'une prime unique pour un
**nouveau** marchand. Le lecteur que le site retient n'a pas besoin de
l'alerte et ne rapporte rien. **Modèle pris en tenaille.**

**Décisions qui appartiennent à l'utilisateur** : anonymat (le compte GitHub
relie publiquement tous ses projets ; rendre privés les dépôts autres que
`digcost`), mentions légales vs pseudonyme, test de distribution (poster le
calculateur dans des espaces publics sans message privé), cible et modèle
d'argent, et la question « pourquoi A4b et pas A2 » face à l'objectif
« maximum d'argent ».

**Captures attendues** : https://www.shopify.com/fr/tarifs ,
https://www.shopify.com/legal/terms (sections 5.5, 5.6, 15.2),
https://help.shopify.com/en/affiliates/earnings — pour confirmer la grille
Grow/Advanced et le HT déjà enregistrés « à confirmer » dans `_data/`.

### Instantané du 22/09/2026, soir

| Élément | État |
|---|---|
| Site | En ligne, build vert (`18a1cb1`). 4 URL en indexation prioritaire, sitemap accepté. |
| Bloc d'inscription | Réécrit pour le marchand **déjà installé** (contre-expertise, faille n° 1). |
| Email de bienvenue | ✅ **Fonction native** beehiiv (`Settings → Emails → Welcome email`), testé de bout en bout. L'automatisation payante est **désactivée**, pas supprimée. |
| Logo beehiiv | ✅ Carré (`digcost/assets/logo/digcost-carre-email.png`) : beehiiv recadre en carré centré. |
| Adresse du pied de page | ✅ Tranchée : champ vide côté publication, adresse = celle de beehiiv. On laisse vide (anonymat). |
| **Inscrits** | **0 vrai inscrit** au 22/09, 20h15. Règle : **total affiché − 1** (le propriétaire reste abonné comme copie de contrôle). Filtre pour tout voir : `Signup date: is after 01/09/2026`. |

**Prochaine action de l'utilisateur (prévue le 23/09, sur PC)** : captures
complètes, notes de bas de page comprises, de https://www.shopify.com/fr/pricing
et https://www.shopify.com/pricing. Débloque **HT/TTC** (écart possible de 20 %
sur le calculateur) et les **frais fixes Grow/Advanced**. À réception :
corriger le calculateur, ajouter les relevés dans `digcost/_data/`
(on ajoute, on n'écrase jamais), compléter l'entrée US du 22/09 dans
`resumes_automatiques.yml`.

**Échéances** : 27/09 EmpCo (dimanche) · ~02/10 fin de l'essai beehiiv —
vérifier que l'email natif part toujours · 12/10 J+21.

**Projet** : AI Business Lab — construire à partir de zéro, à budget nul, un
portefeuille de business numériques automatisés par IA sur le marché
francophone. **Aucun lien avec PokéDeals**, qui n'héberge ce dossier que
temporairement.

**Verticale retenue** : les **e-commerçants français** (décision du 21/09/2026,
sur le critère posé par l'utilisateur : revenu maximal, marché stable ou
porteur). Les artisans du bâtiment ont été écartés — marché en recul.

**Forme retenue** (révisée le 21/09/2026 après le test 01) : **B2 (comparateur
SEO) en point d'entrée** + **A4b (newsletter sans cadence forcée)** en capture
+ D1 (contenus courts, test jetable), monétisés par **affiliation récurrente**.

---

## Ce qui est fait

- [x] Étude de marché datée et sourcée (`01-etude-marche.md`)
- [x] Portefeuille de 15 concepts noté et classé, + 1 concept externe (F1) entré pour comparaison (`02-portefeuille-concepts.md`)
- [x] Contre-épreuve sous grille « revenu maximal » (`outils/criteres-max-revenu.yaml`)
- [x] Plan d'exécution et plan des 90 jours (`03-plan-execution.md`)
- [x] Niche Radar, tableau de bord, monétisation/risques, agents, roadmap, budget (`04` à `09`)
- [x] Modèles réutilisables (`modeles/`)
- [x] Moteur de classement + 10 tests, vert en CI (`outils/`)
- [x] Kit de lancement de la verticale (`lancement/`)
- [x] Les 6 premiers numéros rédigés intégralement (`lancement/numeros/`)
- [x] Les 31 scripts de contenus courts rédigés (`lancement/contenus/`)
- [x] Deux passages du Niche Radar exécutés (`opportunites/`) — le second a sorti
      la directive EmpCo, applicable au 27/09/2026
- [x] Comparateur : 12 pages rédigées — méthodologie, page pilier, fiches plateformes, comparatifs, protocole IA, pages obligations (`lancement/comparateur/`)
- [x] Journal des vérifications réglementaires ouvert (`lancement/verifications.md`)
- [x] Arborescence autonome préparée (`.gitignore`, `.github/workflows/tests.yml`, chemins racine)

---

## TEST 01 — FAIT le 21/09/2026, et il a changé le plan

**Premier test réel du projet.** Le numéro 1 a été mis devant l'utilisateur avec
une question fermée. Réponse : *« Non, trop ennuyeux, trop juridique et
personnellement j'évite ce genre de newsletters qui polluent nos boîtes mail. »*

**Ce qui en est sorti** — fiche complète : `11-journal-des-tests.md`.

1. Un **critère manquant** dans la grille : `tenue_dans_la_duree` (poids 2.0).
   Dix-huit critères notaient le marché, aucun ne notait ce que le format exige
   de l'opérateur semaine après semaine.
2. **Le concept n'est PAS tué** : même en poussant l'aversion au maximum, A4
   (78.1) reste devant B2 (74.7). Céder ici aurait été flatter contre les
   chiffres.
3. **La cadence hebdomadaire est tuée.** Variante **A4b** (envoi quand une
   échéance tombe) : **79.7, 1ᵉʳ sur 17**.
4. **Le comparateur devient le point d'entrée**, la newsletter la couche de
   capture. Aucun contenu rédigé n'est perdu : même recherche, deux sorties.

**Ne pas rouvrir la verticale** : rien dans ce retour n'attaque le marché des
e-commerçants. Le rouvrir serait une réaction, pas une décision.

## TEST 02 — FAIT le 21/09/2026, il tranche ce que le test 01 laissait ouvert

La page pilier du comparateur a été présentée au **même lecteur**. Réponse :
*« C'est déjà plus plaisant et on est dans le concret. »*

Le test 01 laissait une alternative non tranchée : le rejet portait-il sur le
**format** (l'email) ou sur l'**angle** (le droit) ? Si c'était l'angle, il
fallait rouvrir la verticale entière. **Le test 02 l'écarte** : le même lecteur
accepte le même sujet dès qu'il est abordé par les chiffres.

**Règle éditoriale adoptée — le coût passe avant l'obligation :**

1. Titre et accroche parlent d'**argent**, jamais d'une obligation.
2. L'obligation arrive en second, comme **cause du coût**, pas comme menace.
3. Un **chiffre calculé** dans les trois premières lignes — un calcul que le
   lecteur peut refaire, pas seulement un fait.

**Conséquence appliquée** : ordre d'envoi révisé et six numéros retitrés
(`lancement/numeros/README.md`). Le numéro 4 passe en tête — **mais ses liens
d'affiliation doivent en être retirés** s'il part en premier, et renvoyer vers
la page du comparateur qui les porte.

**Limite des deux tests, à répéter à chaque reprise** : le lecteur n'est **pas**
e-commerçant. Deux tests sur un non-client ne font pas une audience. Ce qu'ils
valident, c'est la tenue de l'opérateur — pas le marché.

---

## CHANGEMENT DE CAP DU 21/09/2026 — objectif patrimoine

L'utilisateur a confirmé que **devenir riche était sa seule vraie volonté**. La
fonction objectif change : on optimise désormais la **valeur patrimoniale de
l'actif**, pas le revenu. Troisième grille : `outils/criteres-patrimoine.yaml`.
Analyse complète : `13-strategie-patrimoine.md`.

**Le constat central, et il faut le garder en tête à chaque reprise** : aucun
des 17 concepts ne dépasse **85/100** même en supposant tout son potentiel
réalisé. **Le choix du concept n'est pas le levier.** Ne pas perdre de temps à
rouvrir le classement.

**Les trois leviers réels, mesurés :**

1. **La langue.** Le français seul coûte **+3.8 à +7.7 points** à chaque concept
   du haut de tableau. C'est le facteur le plus déplaçable du dossier, et il ne
   coûte rien tant que rien n'est publié. **L'anglais passe au mois 6**, et le
   site est structuré pour l'accueillir dès la première page (`/fr/`, `/en/`).
2. **La destination.** E1 micro-SaaS passe 8ᵉ → 4ᵉ sous cette grille. Un
   logiciel B2B se revend 3-5× son revenu **annuel**, un site de contenu 30-45×
   son revenu **mensuel** — facteur ~10. Le média devient le **canal**, pas le
   produit. Journal des questions de lecteurs à tenir dès le premier contact :
   c'est lui qui désignera le SaaS.
3. **Le temps passé dans le jeu.** Aucune grille ne le mesure, et c'est le plus
   déterminant. Le test 01 a déjà signalé le risque ici.

**Enseignement tombé en écrivant la grille** : l'affiliation est une bonne
source de revenu et un **mauvais actif patrimonial** (dépendance à un tiers,
aucune relation contractuelle avec le client final, forte décote à la revente).
Elle finance la phase 1, elle ne construit pas le patrimoine. Poids 1.5.

**Ce que ce cap coûte, et c'est écrit** : premier euro plus tard, probabilité
d'échec plus élevée, horizon 4-5 ans au lieu de 24 mois. Le résultat médian
reste **zéro**. `12-peut-on-devenir-riche.md` n'est **pas** révisé.

---

## NOM ARRÊTÉ ET SITE CONSTRUIT — 21/09/2026

**Nom retenu : `DigCost`.** En place dans tous les fichiers (13 occurrences
remplacées). « Dig » seul avait été proposé puis écarté : `dig.com`, `dig.fr`,
`dig.io`, `getdig.com` et `usedig.com` résolvent tous, et surtout « Dig » seul
est **inchercheable** — or depuis le virage patrimoine le SEO est toute
l'acquisition.

**Site construit** dans `site/` : GitHub Pages, **aucune étape de build**, 0 €.
Page pilier (le coût réel), méthode de classement, accueil FR, structure
anglophone en place. Détail et procédure : `site/README.md`.

### ✅ SITE EN LIGNE — dépôt créé et rempli le 21/09/2026

**Dépôt : `Justok16/digcost`**, site à la racine, `baseurl: "/digcost"`.
**Adresse : https://justok16.github.io/digcost/** dès activation de Pages par
l'utilisateur (Settings → Pages → Deploy from a branch → `main` + `/ (root)`).

`ai-business-lab/site/` ne contient **plus les fichiers**, seulement un pointeur :
deux copies d'un même site divergent toujours. **`digcost` est la seule source
de vérité du site.** Le journal des vérifications, lui, reste ici — il contient
ce qui n'est PAS vérifié, et ça n'a pas à être public.

### ✅ LES DEUX VÉRIFICATIONS SONT LEVÉES

1. **Les tarifs** — **FAIT le 21/09/2026**, sur la grille officielle de
   l'éditeur, par captures d'écran de l'utilisateur. **Deux chiffres sur trois
   étaient faux** (Basic 25 → 27 €, Grow 66 → **79 €**, soit 20 % d'écart).
   Sans cette étape, la première page publiée du projet aurait été fausse.
   C'est la justification rétrospective de toute la règle R3.
   Reste mineur : prix **mensuels** sans engagement, et mention **HT/TTC**.
2. **Le nom** — le site est publié sous l'adresse **gratuite GitHub**, donc
   aucun domaine n'a été acheté et aucun risque n'a été pris. La disponibilité
   de `digcost.com`/`.fr` et l'antériorité **INPI** (classes 35/41) restent à
   confirmer **avant tout achat de domaine**, pas avant publication.

### Design validé le 21/09/2026 — ne pas le refaire sans raison

Trois itérations ont été nécessaires. Les deux premières ne corrigeaient que des
détails ; **le problème était structurel**, et le retour de l'utilisateur était
juste : colonne unique de 46 rem, tout au même poids, du blanc du haut en bas.

**Ce qui a débloqué** : bannière sombre sur deux colonnes (sombre dans les
**deux** thèmes), bandeau de chiffres pleine largeur, **passage de la page à
74 rem** en gardant le texte à 44 rem, et panneaux de données sombres insérés
dans le contenu clair. C'est l'élargissement et le contraste entre plans qui ont
fait l'essentiel — pas la couleur.

**Leçon de méthode** : quand un retour dit « pas assez moderne », chercher
d'abord la **structure** (largeur, hiérarchie, contraste de plans) avant la
couleur ou la typographie. J'ai perdu deux allers-retours à faire l'inverse.

**Palette validée par script**, jamais à l'œil (guide dataviz) : `#0f8f62`
clair, `#2bbd8a` sombre, `#3fd6a4` et `#9aa8a2` sur la surface de bannière
`#0a0f0d`. **La bannière est une surface distincte du thème sombre** et a son
propre contrôle de contraste. Le vert vif `#1baf7a` a été **écarté** à 2,74:1,
sous le seuil de 3:1.

### Limite connue, écrite pour ne pas être redécouverte

Les liens internes sont en chemins **absolus** (`/fr/methode/`). Ils cassent si
le site est servi sous `github.io/<dépôt>/`. Correctif dans `site/README.md` :
soit un domaine propre, soit `baseurl` + préfixage des liens. Le site est écrit
pour vivre **à la racine d'un domaine**.

### Ne pas porter les 13 pages du comparateur maintenant

La page pilier et la méthode suffisent à tester si le trafic vient. Les
suivantes s'ajoutent quand on sait que le site a des lecteurs.

---

## PRIORITÉ N° 1 — faire juger le produit, pas l'administratif

**Ajouté le 21/09/2026, après comparaison avec une exécution externe du même
prompt.** Le reproche est fondé et il est consigné ici pour ne pas être oublié :
ce dossier a produit 7 400 lignes et **n'a obtenu aucun signal de la réalité**,
pendant que l'exécution concurrente faisait réagir l'utilisateur en quelques
heures sur un livrable concret.

Ce qui a été demandé à l'utilisateur jusqu'ici était **administratif** (créer un
dépôt). Ce qu'il fallait lui demander, c'est de **juger le produit**.

**Donc, avant toute autre demande** : lui faire lire
`lancement/numeros/numero-01.md` — trois minutes, aucun compte, aucun outil — et
répondre à *« est-ce que je m'abonnerais à ça ? »*.

Le chemin complet jusqu'au premier envoi est dans **`PREMIER-ENVOI.md`**.

**Règle de conduite pour les reprises suivantes** : ne pas produire de contenu
supplémentaire. Le stock couvre sept semaines. Tant que rien n'est publié, écrire
un huitième numéro a une valeur **nulle**, et cette phrase est arithmétique.

---

## EN COURS — sortir le projet dans son propre dépôt

**Bloqué sur une action de l'utilisateur.** L'application GitHub de la session
**ne peut pas créer de dépôt** (`403 Resource not accessible by integration`).

### Ce que l'utilisateur doit faire (une seule fois)

Créer sur github.com un dépôt **vide** nommé **`ai-business-lab`** — sans
README, sans `.gitignore`, sans licence (sinon la première poussée est refusée).
Visibilité privée de préférence.

### Ce qu'il faut faire dès que ce dépôt existe (sans rien redemander)

1. `list_repos` → confirmer que `Justok16/ai-business-lab` apparaît.
2. `add_repo` avec `access: "push"`.
3. Reconstruire l'arborescence autonome (voir `MIGRATION.md`, tout y est), puis
   pousser sur `main`.
4. Vérifier que la CI du nouveau dépôt passe (job `scoring` → 10 tests).
5. **Seulement après une poussée réussie**, nettoyer `pokedeals` :
   - supprimer `ai-business-lab/` ;
   - retirer le job `scoring_strategie` de `.github/workflows/tests.yml` ;
   - retirer la section `ai-business-lab/` du `README.md` racine et la ligne
     correspondante dans l'arborescence ;
   - pousser sur `claude/ai-business-portfolio-strategy-96yf4g`.
6. Fermer la **PR #118** avec un commentaire renvoyant vers le nouveau dépôt.

**Règle de sécurité** : ne jamais supprimer `ai-business-lab/` de `pokedeals`
tant que le contenu n'a pas été poussé ailleurs **avec succès**. Tant que le
nouveau dépôt n'existe pas, cette branche est le **seul endroit durable** où ce
travail existe.

---

## À FAIRE ensuite (ne dépend de personne)

- [x] ~~Rédiger les 4 premiers numéros de la newsletter en entier~~ — fait le
      21/09/2026, dans `lancement/numeros/`. Prêts à envoyer **après levée des
      marqueurs `[VÉRIFIER]`** sur source officielle.
- [x] ~~Rédiger les premières pages du comparateur~~ — fait le 21/09/2026, dans
      `lancement/comparateur/` : méthodologie publiée, page pilier chiffrée
      (le calcul complet du coût réel d'une boutique), 3 fiches plateformes,
      et plan détaillé des 6 pages restantes.
- [x] ~~Rédiger les pages restantes du comparateur~~ — fait le 21/09/2026.
      Douze pages au total dans `lancement/comparateur/`.
- [ ] **DÉPEND DE L'UTILISATEUR** : exécuter le protocole de test des outils d'IA
      (`lancement/comparateur/05-outils-ia-protocole.md`). Il exige un **vrai
      catalogue produit** et l'usage réel des outils — une session Claude ne peut
      pas le faire à sa place, et surtout ne doit pas l'inventer : toute la valeur
      de cette page tient au fait que les résultats sont réels.
      **Ne pas reprendre cette tâche automatiquement.**
- [ ] **DÉPEND DE L'UTILISATEUR** : ouvrir les textes sur Légifrance et EUR-Lex
      (bloqués par le proxy réseau ici) pour clore les `[À CONFIRMER]` restants.
- [x] ~~Faire tourner le Niche Radar une première fois~~ — fait le 21/09/2026,
      2 fiches dans `opportunites/`, toutes deux classées INTÉGRER.
- [x] ~~Numéro 5 (e-reporting) et sa page de comparateur~~ — fait le 21/09/2026.
- [x] ~~Deuxième passage de Niche Radar~~ — fait le 21/09/2026. **Il a sorti le
      signal le plus urgent du projet** : la directive (UE) 2024/825 « EmpCo »,
      applicable le **27/09/2026**, qu'aucun des cinq numéros ne couvrait.
      Numéro 6 rédigé, il passe devant le numéro 5 dans l'ordre d'envoi.
      Correction de méthode consignée : **balayer les échéances UE avant les
      échéances FR** à chaque passage.
- [ ] **Prochaine tâche par défaut** : refaire un passage de Niche Radar, en
      commençant par les échéances **européennes**. Le stock de contenu est
      suffisant pour sept semaines de publication — produire davantage n'a pas
      de valeur tant que rien n'est publié. Le travail restant dépend de
      l'utilisateur : créer le dépôt, ouvrir les textes officiels, exécuter le
      protocole de test IA, puis **publier**.
- [ ] **DÉPEND DE L'UTILISATEUR — URGENT, échéance 27/09/2026** : vérifier la
      directive **EmpCo (UE) 2024/825** avant d'envoyer le **numéro 6**. Trois
      lectures, dix minutes : dossier législatif DDADUE (état d'avancement),
      fiche DGCCRF sur l'écoblanchiment, directive sur EUR-Lex. Ces trois
      sources sont **bloquées par le proxy réseau** ici — y compris
      economie.gouv.fr, senat.fr et assemblee-nationale.fr. Détail dans
      `opportunites/2026-09-21-directive-empco-2024-825.md`.
- [x] ~~Comparaison avec l'exécution ChatGPT du même prompt~~ — faite le
      21/09/2026, dans `10-comparaison-chatgpt.md`. Son concept (« Marge
      Claire », Vinted) a été noté dans le moteur sous l'id **F1** : **42,5**,
      dernier sur 16, et il ne remonte pas dans la première moitié même avec
      sept corrections favorables. **Ne pas rouvrir ce point sans donnée
      nouvelle.** Trois apports de son travail ont été intégrés : règles R-A,
      R-B et R-C du Niche Radar, et la règle éditoriale « persona et sujets
      sensibles ».
- [ ] **DÉPEND DE L'UTILISATEUR** : vérifier l'accessibilité numérique (EAA) en
      source officielle avant toute publication — les sources divergent sur les
      sanctions, et EUR-Lex/Légifrance sont bloqués ici.
- [~] Vérifier chaque fait réglementaire sur sa **source officielle** (règle R3).
      **Commencé le 21/09/2026**, journal dans `lancement/verifications.md` :
      rétractation en ligne, TVA OSS/IOSS et calendrier de facturation
      électronique **vérifiés** ; DSA **partiellement** — la qualification d'une
      boutique affichant des avis n'a pas pu être établie, le numéro 3 a donc
      été réécrit pour n'affirmer aucune obligation. **Sanction de la fonction
      de rétractation levée le 21/09/2026** : art. L242-13 c. consom., 15 000 €
      (personne physique) / 75 000 € (personne morale) + prolongation du délai
      de 12 mois. Légifrance et EUR-Lex restent **bloqués par le proxy réseau**
      de cet environnement : ces textes-là doivent être ouverts manuellement
      avant publication.

---

## Décisions déjà prises — ne pas rouvrir sans raison nouvelle

| Décision | Motif |
|---|---|
| Projet indépendant de PokéDeals | Consigne explicite de l'utilisateur |
| Audience professionnelle, pas grand public | RPM FR 5-12 € en B2B contre 0,50-2,50 $ sur les formats faceless saturés |
| E-commerçants FR | Seule verticale testée qui combine marché en croissance (+7 %) et affiliation récurrente (Shopify 20 % sur 4 ans) |
| Artisans du bâtiment écartés | Marché en recul : 13 trimestres de baisse |
| Chaîne faceless divertissement écartée | Dernière du classement, y compris sous la grille « revenu maximal » |
| Angle « outils, vrais prix, obligations » | Le créneau e-commerce est saturé de vendeurs de méthodes ; c'est le seul angle défendable |
| Aucune promesse de revenus | Différenciation **et** protection juridique. Vaut aussi **envers l'utilisateur** : voir `12-peut-on-devenir-riche.md`, jamais révisé à la hausse pour encourager |
| Objectif reformulé | « Devenir riche » n'est pas exploitable. Cible de travail : **1 500 €/mois en 24 mois sans présence quotidienne** |
| Revendeurs Vinted écartés | Noté F1 dans le moteur : **42,5**, dernier sur 16, robuste à sept corrections favorables |
| Aucun titre professionnel revendiqué | Règles des plateformes sur les personas IA + protection juridique (`10-comparaison-chatgpt.md` §7) |

---

## Blocages connus

| Blocage | Nature | Levée |
|---|---|---|
| Création de dépôt GitHub | Droit manquant de l'app (403) | Action utilisateur, ci-dessus |
| Faits réglementaires en niveau 2/3 | Méthode | Vérification sur source officielle avant publication |

---

## Suivi automatique en place

- **Routine horaire** `Reprise automatique — AI Business Lab`
  (`trig_01NJayY6F8bQrnofRiia7i1i`) : réveille cette session toutes les heures,
  lit ce fichier, reprend ce qui peut l'être, et **reste silencieuse** si tout
  est bloqué côté utilisateur.
- **Abonnement aux événements de la PR #118** : CI et commentaires de revue.

---

## Chaine de publication du site — etat au 21/09/2026

**Le site `digcost` est rendu par GitHub Pages avec le paquet `github-pages`,
qui fige Jekyll 3.10 et une liste precise de greffons.** Ce n'est pas le
Jekyll le plus recent. Construire en local avec une version plus recente
donne un apercu qui valide du code que la production refuse — c'est pire
qu'aucun apercu, parce qu'il inspire une confiance injustifiee.

**Toujours verifier avec `./apercu.sh` a la racine du depot `digcost`.**
Il construit avec les versions de production, sous le vrai prefixe d'URL, et
liste les pages publiees.

### Deux pannes reelles, le meme jour, la meme cause

1. **Le site a ete gele pendant deux commits.** Un filtre
   `where_exp: "p", "p.permalink and p.sitemap != false"` dans `sitemap.xml`
   est refuse par Jekyll 3 (`and` n'y est pas supporte). Le build de
   production echouait ; le site restait servi par la derniere version
   valide, donc **rien ne semblait casse cote visiteur**. Detecte seulement
   parce que GitHub a envoye un courriel d'echec.
2. **Une note technique interne etait publiee comme page du site.** Le
   greffon `jekyll-readme-index`, actif en production et absent en local,
   transformait `assets/logo/README.md` en page publique, inscrite au
   sitemap. Corrige par `readme_index: enabled: false`.

### Regle retenue

**Un build vert en local ne prouve rien si l'outillage differe de la
production.** C'est exactement ce que DigCost reproche aux comparatifs : un
chiffre — ou une version — repris de seconde main vieillit sans prevenir, et
personne ne s'en apercoit.

### Etat du site au 21/09/2026, 22h40

| Page | Adresse |
|---|---|
| Accueil | `/` |
| Calculateur de cout reel | `/fr/calculateur/` |
| Page pilier | `/fr/prix-shopify-cout-reel/` |
| Methode | `/fr/methode/` |
| Anglais | `/en/` |

L'ancienne adresse `/fr/cout-reel-boutique/` redirige. Le formulaire beehiiv
est integre sur trois pages via `_includes/capture.html`, avec repli si le
script tiers est bloque. `sitemap.xml`, `robots.txt` et le fichier de
validation Search Console sont en ligne.
