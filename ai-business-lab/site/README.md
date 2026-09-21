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

## Activer le site (2 minutes, une fois les vérifications faites)

1. Dépôt → **Settings** → **Pages** ;
2. *Source* : **Deploy from a branch** ;
3. Branche : celle qui porte ce dossier ; répertoire : **`/ai-business-lab/site`**
   si l'option est proposée, sinon voir « Limite connue » ci-dessous ;
4. **Save**. Le site est en ligne en 1 à 2 minutes.

## ⚠️ Limite connue — les liens internes et le préfixe d'URL

GitHub Pages sert un dépôt de projet sous `https://<compte>.github.io/<dépôt>/`.
Les liens internes de ce site sont écrits en **chemins absolus**
(`/fr/methode/`), donc ils **casseront** sous un tel préfixe.

Deux solutions, au choix :

| Situation | Ce qu'il faut faire |
|---|---|
| **Domaine propre** (`digcost.fr`) ou dépôt servi à la racine | Rien. Les liens fonctionnent tels quels |
| Adresse `github.io/<dépôt>/` | Ajouter `baseurl: "/<dépôt>"` dans `_config.yml` **et** préfixer les liens internes des fichiers Markdown |

Le site a été écrit pour vivre **à la racine d'un domaine** — c'est sa
destination. La forme `github.io/<dépôt>/` est un moyen de le voir en ligne
gratuitement, pas la version finale.

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
