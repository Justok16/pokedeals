# Chaîne de recherche de prospects (sites internet pour artisans)

Méthode reproductible pour n'importe quel département. Les **résultats**
(noms, téléphones) sont privés : ils vont dans le Google Drive « Dig »,
jamais dans ce dépôt.

1. `registre.py <dép>` : établissements actifs des métiers visés, via
   l'API publique Recherche d'entreprises (relais Vercel, cookie `cj.txt`).
2. `devine_sites.py <dép>` : pour chaque entreprise, teste les domaines
   probables (`nom.fr`, `nom.com`, `nom-commune.fr`) et vérifie que la
   page mentionne la commune ou le code postal.
3. Annuaire **RGE de l'ADEME** (gratuit, sans clé) : téléphone et site
   déclarés par les artisans RGE :
   `https://data.ademe.fr/data-fair/api/v1/datasets/liste-des-entreprises-rge-2/lines?size=1000&qs=code_postal:<dép>*`
4. **OpenStreetMap** (Overpass, via le relais) : commerces avec
   téléphone et site.
5. **Sites SoLocal** : sous-domaines `*.site-solocal.com` devinés, et
   sites sur le domaine du client repérés par la mention SoLocal ; la
   date de dernière mise à jour vient du `sitemap.xml` (`<lastmod>`).
6. **Vérification une par une** (recherche web) avant toute mise en liste
   d'appels : sur un échantillon du 26/09/2026, environ **1 entreprise
   « sans site » sur 2** avait en réalité un site sous un autre nom.
   **Téléphones** (leçon du 29/09/2026) : un numéro venant de l'annuaire RGE
   ou d'OpenStreetMap est rapproché par adresse et peut appartenir à une
   autre entreprise (même bâtiment, même zone). Chaque numéro est vérifié à
   la source (PagesJaunes, page Facebook, site de la commune) avant la mise
   en liste. Pour repérer les doublons avec les listes déjà remises, comparer
   les numéros sur leurs 9 derniers chiffres (« +33 5 45… » = « 05 45… »),
   et vérifier aussi les procédures collectives au BODACC.
   Quand l'entreprise a un site (même ancien), méthode gratuite et la plus
   sûre : chercher le numéro sur ce site (accueil puis pages contact et
   mentions légales), en essayant aussi `http://` car beaucoup de vieux
   sites n'ont pas de certificat. Sur 65 fiches revérifiées ainsi le
   29/09/2026 : 61 confirmées, 3 numéros remplacés par celui du site,
   1 fiche retirée (site en fait tenu à jour). Attention aux faux positifs :
   une suite de chiffres dans le code d'une page (identifiant de police
   Wix, par exemple) n'est pas un numéro affiché.
7. Classement : métier (bâtiment, auto, restauration, beauté, gîtes…),
   salariés, ancienneté, RGE, entreprise récente ; pénalité pour les
   grandes entreprises (souvent déjà une agence) ; exclusion des
   entreprises en procédure collective.
8. **Chiffre de demande** (depuis le 30/09/2026) : pour chaque prospect retenu,
   OpenRush `research_keywords` (graine « <métier> <commune> », pays France,
   langue French, mode `suggestions`) donne le nombre de recherches Google
   mensuelles et le coût d'un clic publicitaire. Argument d'appel : « chaque
   mois, environ N personnes cherchent <métier> à <commune> ; sans site, vous
   n'apparaissez pas ». Donnée d'estimation (confiance 0,7 selon l'outil) :
   toujours dire « environ », jamais un chiffre exact. Ce chiffre va dans la
   fiche privée, pas dans ce dépôt.

## Améliorations du 30/09/2026 (skill « prospecting », guide local-prospecting, licence MIT)

1. **Encadré « Les 3 à appeler en premier »** en tête de chaque nouvelle liste : une phrase par
   prospect qui nomme le manque et le signal (ex. « aucun site (vérifié par nom exact + commune) ;
   RGE valable ; 10 à 19 salariés »).
2. **Degré de confiance** par fiche : élevé (2 sources ou plus concordantes), moyen (1 source +
   indices cohérents), faible (à confirmer au premier appel).
3. **Ne pas viser que les plus grosses entreprises** : celles de 2 à 5 salariés sont souvent moins
   démarchées. Le classement par taille reste, mais l'encadré des 3 premiers mélange les tailles.
Rappels déjà en place et confirmés par ce guide : pas d'extraction en masse de Google Maps
(conditions d'utilisation), recherche du nom exact avant de conclure « sans site », doublons exclus.

- `reprise_site.py` (09/10/2026) : lit poliment quelques pages de l'ancien site d'un prospect (robots.txt respecté, pause entre pages) et en tire une fiche privée (nom, description, téléphones, horaires, villes, années, titres de sections = services probables, photos et logo probables) pour préparer sa page d'accueil refaite plus vite. Contenu du client seulement ; photos et logo dans une démo uniquement avec son accord ; sortie dans un dossier privé, jamais dans le dépôt.
