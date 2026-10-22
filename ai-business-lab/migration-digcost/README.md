# Déménagement de DigCost vers un compte séparé

> ✅ **TERMINÉ le 23/09/2026.** Site en ligne sur **https://digcost.github.io/**,
> publié par le compte `digcost` (dépôt `digcost/digcost.github.io`) ; source
> `Justok16/digcost` **privée** ; publication vérifiée après passage en privé
> (Publication #2, succès). Clé : lecture seule, dépôt `digcost` seul, sans
> expiration.

**Décidé le 23/09/2026 par l'utilisateur**, après les audits externes.

## Pourquoi

Le compte `Justok16` relie publiquement DigCost à tous les autres projets de
l'utilisateur, et l'historique public de `pokedeals` contient son adresse
personnelle. Rendre `pokedeals` privé n'est pas possible : ses tâches
planifiées (plus de 400 exécutions par jour) épuiseraient en quelques jours le
quota de 2 000 minutes par mois d'un dépôt privé gratuit, et PokéDeals
s'arrêterait. La coupure se fait donc de l'autre côté.

## Architecture visée

| Élément | Où | Visibilité |
|---|---|---|
| Code source du site | `Justok16/digcost` | **privé** (aucune tâche planifiée, aucun quota en jeu) |
| Publication | nouveau compte, dépôt `<compte>.github.io` | public, ne contient que `publication.yml` |
| Accès du second au premier | clé à grain fin, lecture seule, sur `digcost` uniquement | secret du dépôt de publication |

Le dépôt public ne contient que le fichier de publication : la source et la
clé sont des secrets, invisibles dans le fichier et dans les journaux.
Une publication par heure ; un commit mensuel automatique empêche GitHub de
désactiver les tâches planifiées d'un dépôt inactif.

## Étapes (utilisateur, ~1 h)

1. ✅ Compte créé le 23/09 : **`digcost`** → site futur **https://digcost.github.io/**
2. ✅ Sur `Justok16` : créer une clé à grain fin, lecture seule, limitée à `digcost`
✅ 3. Sur le nouveau compte : créer le dépôt `<compte>.github.io`
✅ 4. Y coller `publication.yml` dans `.github/workflows/`
✅ 5. Ajouter les secrets `SOURCE_REPO` et `SOURCE_TOKEN`, régler Pages sur « GitHub Actions »
✅ 6. Lancer la publication, vérifier le site
7. ✅ `Justok16/digcost` passé en privé. ✅ Search Console (propriété validée, sitemap envoyé) et liens de l'email de bienvenue beehiiv corrigés

## Côté Claude

✅ Préparé sur la branche `nouvelle-adresse` de `Justok16/digcost` (non
fusionnée : sur `main`, elle casserait l'adresse actuelle). **À fusionner dans
`main` au moment de l'étape 6**, pas avant. Build vérifié : aucune trace de
`justok16` dans le site publié, robots.txt désormais à la racine.

Liste d'origine :

- `_config.yml` : `url` et `baseurl` (une ligne chacune)
- `README.md` du site : ne plus nommer l'ancienne adresse ni le compte
- Vérifier qu'aucune page publiée ne mentionne `Justok16`
- Build de contrôle avec `./apercu.sh`

## Ce qui ne s'efface pas

Ce qui a déjà été vu, archivé, ou envoyé aux IA auditrices (le prompt d'audit
contenait les liens). Le dossier stratégique reste dans `pokedeals` jusqu'à sa
propre migration (`MIGRATION.md`).

## Conséquences pour la maintenance

- **Pousser sur `main` de `Justok16/digcost` suffit** : la publication récupère
  la source chaque heure (minute 17). Délai de mise en ligne : jusqu'à 1 h.
- Le suivi des builds ne passe plus par `Justok16/digcost` (Pages y est
  désactivé, dépôt privé) mais par les exécutions « Publication » du compte
  `digcost`, que la session Claude ne voit pas forcément : **en cas de doute,
  demander une capture à l'utilisateur.**
- L'ancienne adresse `justok16.github.io/digcost` ne répond plus.
