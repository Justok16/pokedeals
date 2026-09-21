# Site DigCost — comment le mettre en ligne

Site statique rendu par **GitHub Pages**, sans aucune étape de build : ni npm,
ni générateur à installer. GitHub lit les fichiers Markdown et produit le HTML.

**Coût : 0 €.**

---

## ⛔ Ne pas activer Pages tout de suite

Deux vérifications doivent être faites **avant** la mise en ligne. Elles ne
prennent pas dix minutes, mais publier sans elles décrédibiliserait le site dès
sa première page.

### 1. Les tarifs de la page pilier

Toute la valeur de `fr/cout-reel-boutique.md` tient à l'exactitude de ses
chiffres. Ils ont été relevés le **26/08/2026** sur des sources secondaires, et
**les grilles changent plusieurs fois par an**.

À recontrôler sur les pages tarifaires officielles des éditeurs :

- les trois paliers d'abonnement ;
- le taux de frais de transaction **avec** la solution de paiement intégrée ;
- le taux de frais de plateforme **sans** elle (le « 2 % sur Basic »).

Un tarif faux se vérifie en trente secondes par un lecteur. C'est le seul type
d'erreur dont ce site ne se remettrait pas.

### 2. La disponibilité du nom

`digcost.com` et `digcost.fr` **ne résolvent pas** en DNS — mais un domaine peut
être déposé sans être hébergé. Ce n'est donc **pas** une preuve de
disponibilité.

À confirmer chez un registrar, plus l'absence d'antériorité **INPI** en classes
35 et 41.

**Tant que ce n'est pas confirmé**, publier sous l'adresse gratuite GitHub, pas
sous un domaine acheté.

---

## Activer le site

### ⚠️ Contrainte GitHub Pages à connaître d'abord

En mode « Deploy from a branch », GitHub Pages ne sert que **la racine du dépôt**
ou **`/docs`**. Il n'est **pas** possible de désigner un dossier quelconque comme
`ai-business-lab/site`.

Conséquence : ce dossier ne peut pas être publié tel quel depuis `pokedeals`.
Il doit vivre **à la racine de son propre dépôt** — ce qui est de toute façon sa
destination.

### La marche à suivre

1. Créer sur github.com un dépôt **vide** nommé **`digcost`** — sans README,
   sans `.gitignore`, sans licence.
2. Y pousser **le contenu de ce dossier à la racine** (pas le dossier lui-même).
3. Dépôt → **Settings** → **Pages** → *Source* : **Deploy from a branch**,
   branche `main`, répertoire **`/ (root)`** → **Save**.
4. Renseigner `baseurl: "/digcost"` dans `_config.yml`.
5. En ligne sous `https://<compte>.github.io/digcost/` en 1 à 2 minutes.

### Le préfixe d'URL est géré, il n'y a rien à réécrire

Tous les liens internes passent par le filtre Jekyll **`relative_url`**. Changer
la seule ligne `baseurl` dans `_config.yml` suffit à déplacer le site :

| Où le site est servi | `baseurl` |
|---|---|
| `digcost.fr` (domaine propre) | `""` |
| `<compte>.github.io` (dépôt nommé `<compte>.github.io`) | `""` |
| `<compte>.github.io/digcost/` | `"/digcost"` |

Aucun lien Markdown n'est à toucher dans aucun de ces cas.

---

## Ce que contient le site aujourd'hui

| Fichier | Page |
|---|---|
| `index.md` | Accueil FR |
| `fr/cout-reel-boutique.md` | **Page pilier** — le calcul du coût réel |
| `fr/methode.md` | Méthode de classement (publiée avant les fiches, délibérément) |
| `en/index.md` | Structure anglophone en place, contenu à venir au mois 6 |
| `_layouts/default.html` | Gabarit unique |
| `assets/style.css` | Feuille de style, thème clair et sombre |

## Pourquoi `/fr/` et `/en/` dès maintenant

Décision du 21/09/2026 (voir [`../13-strategie-patrimoine.md`](../13-strategie-patrimoine.md)) :
la contrainte francophone coûte **+3,8 à +7,7 points** à chaque concept du haut
de tableau sous la grille patrimoine. C'est le facteur le plus déplaçable du
dossier — et il ne coûte rien à préparer **tant que rien n'est publié**.

Restructurer les URL d'un site déjà indexé coûte cher en référencement. Le faire
avant la première page ne coûte rien. D'où ces deux dossiers, aujourd'hui.

## Les 13 pages restantes

Elles sont rédigées dans [`../lancement/comparateur/`](../lancement/comparateur/)
et se portent ici au même format : un en-tête `---` avec `title`, `description`,
`permalink`, `lang` et `verifie`, puis le corps en Markdown.

**Ne pas toutes les porter d'un coup.** La page pilier et la méthode suffisent à
tester si le trafic vient. Les suivantes s'ajoutent une fois qu'on sait que ce
site a des lecteurs — sinon c'est du travail sans valeur, exactement ce que
`../REPRISE.md` interdit.
