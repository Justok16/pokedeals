# 63 — Kit de branchement : réseaux sociaux et autres supports (préparé le 08/10/2026)

Demande de l'utilisateur (08/10) : « que tout soit prêt à se brancher sur les réseaux sociaux et autres supports ».
Tout le contenu est prêt ; le jour de la validation de l'entreprise, l'utilisateur **crée les comptes** (identité,
téléphone, double authentification : lui seul peut le faire) et **les relie à Metricool** ; Claude programme
ensuite les 8 semaines de publications en une fois.

## 1. Ce qui est prêt

| Élément | Où |
|---|---|
| Textes des profils (nom, identifiant, catégorie, bio courte, description longue) | `61-plan-publicite.md` § 2 et Drive « DIG16 – Fiche Google et réseaux » |
| Photo de profil, couvertures et bannières (Facebook, LinkedIn, Google, YouTube) | `supports/reseaux/` |
| 27 publications sur 8 semaines : textes, visuels, textes alternatifs, version Bluesky | `supports/publications/` (`calendrier.csv` pour un tableur, `calendrier.json` pour Metricool, un PNG par publication, `planche.png`) — générés par `outils/marque/publications.py` |
| Campagne « Le test du pouce » : carrousel de 5 visuels, story, affiche A4 | `supports/campagne-pouce/`, `62-campagne-test-du-pouce.md` |
| Vidéo de présentation (33 s) | `site-dig/video/presentation-v6.mp4` |
| Signature des emails | `supports/signature-email.html` (remplie en privé le jour J) |
| Communiqué de presse | Drive « DIG16 – Communiqué nouvelle entreprise » |

Deux publications restent **manuelles** (« premier client », « bilan des deux mois ») : elles exigent un fait
réel et l'accord écrit du client ; elles ne sont jamais programmées automatiquement.

## 2. Ordre de branchement le jour J (environ 1 h 30 pour l'utilisateur)

Partout : nom **DIG16 — Sites internet en Charente**, identifiant **dig16fr**, lien **https://dig16.fr**, email
**contact@dig16.fr**, téléphone du site. Textes : copier depuis le document Drive (une ligne = un champ).

| # | Support | Ce que fait l'utilisateur | Images à mettre | Relier à Metricool |
|---|---|---|---|---|
| 1 | **Fiche Google** (Google Business Profile) | Créer l'établissement « Concepteur de sites Web », **entreprise de services avec zone desservie, adresse masquée** ; demander la vérification | `avatar-1080.png` (logo), `couverture-google.png` | Oui (« Google Business Profile ») |
| 2 | **Page Facebook** | Créer la page depuis son compte personnel (catégorie : conception de sites web) ; bio courte, description, lien | `avatar-1080.png`, `couverture-facebook.png` | Oui |
| 3 | **Instagram** professionnel | Créer `dig16fr`, passer en compte professionnel, le **lier à la page Facebook** | `avatar-1080.png` | Oui |
| 4 | **LinkedIn** | Profil personnel à jour, puis **page entreprise** DIG16 | `avatar-1080.png`, `banniere-linkedin.png` | Non : l'offre gratuite de Metricool n'inclut pas LinkedIn (`61`) ; publication à la main avec `calendrier.csv` |
| 5 | **YouTube** | Chaîne `@dig16fr` ; mettre la vidéo de présentation (non destinée aux enfants) | `avatar-1080.png`, `banniere-youtube.png` | Facultatif |
| 6 | **Bluesky, Threads** | Compte `dig16fr` (Threads se crée depuis Instagram) | `avatar-1080.png` | Oui |
| 7 | **TikTok, Pinterest** | Compte `dig16fr` ; Pinterest : un tableau « Sites d'artisans » | `avatar-1080.png` | Plus tard (vidéos nécessaires) |

Lien de connexion des réseaux dans Metricool (marque déjà créée, aucun réseau relié au 08/10) :
https://app.metricool.com/brands/connections?blogId=7154026

## 3. Les autres supports

| Support | Action | Qui |
|---|---|---|
| **Bing Places** | Importer la fiche Google (une fois vérifiée) | Utilisateur, 10 min |
| **Apple Business Connect** | Créer la fiche (mêmes textes) | Utilisateur |
| **PagesJaunes, 118712** | Fiche de base ; gratuité **[à vérifier sur leurs sites]** avant toute inscription | Utilisateur |
| **Google Search Console, Bing Webmaster Tools** | Ajouter dig16.fr, puis le sitemap `https://dig16.fr/sitemap.xml` | Utilisateur valide la propriété, Claude guide |
| **Signature email** | Coller la version remplie dans Gmail (ordinateur) et la version texte dans l'application | Utilisateur, 2 min |
| **Affiches A4** | Imprimer la version remplie (coût à soumettre) et la tournée des commerces (`62` § 3) | Utilisateur |
| **Presse, mairie, communauté de communes, CCI** | Envoyer le communiqué | Utilisateur envoie, Claude prépare les messages |

## 4. Ce que Claude fait dès que les comptes sont reliés

1. `getBrandSettings` (Metricool) : vérifier les réseaux reliés et le fuseau horaire.
2. Fixer le **jour J** = premier lundi après la validation ; date de chaque publication = jour J + `decalage_jours`
   (heure du calendrier, ou la meilleure heure donnée par `getBestTimeToPostByNetwork`).
3. Programmer chaque publication « auto » de `calendrier.json` avec `createScheduledPost` : images par leur adresse
   publique (champ `images`), textes alternatifs, `texte_bluesky` pour Bluesky, type « publication » pour la fiche
   Google, stories en type STORY sans texte. Une erreur d'un réseau est corrigée sans changer le sens du texte.
4. Contrôler la liste avec `getScheduledPosts`, puis envoyer à l'utilisateur le récapitulatif (date, réseau, titre).
Quota : l'offre gratuite de Metricool permet 20 publications par mois (lu le 05/10, `61` § 3) ; le calendrier
   en compte 15 sur les 4 premières semaines et 10 sur les 4 suivantes. Qu'une publication envoyée sur plusieurs
   réseaux compte pour une seule est **[à vérifier dans Metricool]** ; sinon, garder Facebook, Instagram et la fiche
   Google, et publier le reste à la main.
5. Chaque vendredi : mesurer ce qui fait venir des demandes (`50` § 8) ; aucun taux inventé.

Les images sont servies depuis le dépôt public (adresse « raw.githubusercontent.com » de la branche de travail ;
vérifiée le 08/10). Si la branche change, régénérer `calendrier.json` (variable `BRUT` du générateur).

## 5. Garde-fous

Rien avant la validation de l'entreprise (identité visible : L34-5 CPCE, art. 20 LCEN) ; aucune publication
« premier client » sans accord écrit ; aucun chiffre inventé ; groupes Facebook : seulement ceux qui autorisent la
publicité ; un compte par réseau, au nom de DIG16, mots de passe chez l'utilisateur seulement (jamais dans le dépôt
ni dans la conversation).
