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
7. Classement : métier (bâtiment, auto, restauration, beauté, gîtes…),
   salariés, ancienneté, RGE, entreprise récente ; pénalité pour les
   grandes entreprises (souvent déjà une agence) ; exclusion des
   entreprises en procédure collective.
