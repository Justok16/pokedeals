# 62 — Campagne « Le test du pouce » (préparée le 08/10/2026, budget 0 €)

Demande de l'utilisateur (08/10) : « une campagne de pub exceptionnelle qui attirera l'attention des prospects
au maximum ». Elle s'ajoute à `50-campagne-lancement.md` (démarchage, visites, recommandation) et à
`61-plan-publicite.md` (supports, profils, 24 publications) : même offre, mêmes règles, **une idée centrale**
qui relie tout.

## 1. L'idée

> **« Prenez votre téléphone. Tapez votre métier et votre ville. Vous êtes où ? »**

Le prospect fait lui-même le test, en 30 secondes, et **constate seul** le problème : il n'apparaît pas, ou
son site s'ouvre mal sur un téléphone, ou son numéro ne s'appelle pas d'un geste. Personne ne lui dit que
son site est mauvais : il le voit. Ensuite, une seule proposition, déjà sur le site : **« Je refais votre
page d'accueil gratuitement. Vous décidez ensuite. »**

Pourquoi ça attire l'attention :

- **Il agit** (il sort son téléphone) au lieu de lire une publicité de plus ;
- **c'est vrai et vérifiable** : aucun chiffre inventé, aucun concurrent nommé ni critiqué ;
- **c'est personnel** : le résultat est le sien, dans sa ville, aujourd'hui ;
- **la suite est sans risque** pour lui : la démo est gratuite et il décide après l'avoir vue.

## 2. Les supports (prêts, à la charte `60`)

**Signature visuelle (version 2, 08/10)** : une **empreinte de pouce dorée** (`outils/marque/empreinte.py`, dessin
fixe) est le seul élément fort de la campagne ; tout le reste reste sobre (encre, laiton, ivoire). On la retrouve
immense sur la première publication et la story, posée dans la place vide « Et vous ? », pressée sur le nom
(ondes), et discrète sur l'affiche. Contrôles automatiques : marges, chevauchements, polices, QR.

Générés par `python3 outils/marque/campagne_pouce.py`, dans `supports/campagne-pouce/` :

| Fichier | Usage |
|---|---|
| `pouce-1.png` à `pouce-5.png` (1080 × 1350) | Série de 5 publications, à publier dans l'ordre (carrousel Instagram ou 5 publications Facebook) : 1 « Prenez votre téléphone », 2 « Vous êtes où ? », 3 « Touchez votre nom », 4 avant/après (exemple fictif), 5 l'offre. La publication « 15 entreprises » a été retirée à la demande de l'utilisateur (08/10) : ne plus utiliser cet argument dans la campagne. |
| `pouce-story.png` (1080 × 1920) | Story Instagram et Facebook, statut WhatsApp de l'utilisateur |
| `affiche-pouce.pdf` (A4) | Vitrines des commerces qui acceptent, panneaux d'affichage des supermarchés et des mairies, salle d'attente ; QR vers dig16.fr testé |
| `planche-publications.png` | Aperçu de la série (contrôle) |

Version de l'affiche avec le nom et le SIREN : générée en privé (`DIG16_IDENTITE` + `DIG16_SORTIE`) le jour de
l'immatriculation, jamais dans ce dépôt.

## 3. Le déroulé (à partir de la validation de l'entreprise, jamais avant : L34-5 CPCE, art. 20 LCEN)

| Moment | Action | Qui |
|---|---|---|
| Jour J | Profils créés (`61` § 2), affiche remplie générée, signature email avec SIREN | Claude prépare, l'utilisateur crée les comptes |
| Semaine 1, lundi | Carrousel des 5 visuels sur Facebook et Instagram + story ; partage dans 2 ou 3 groupes locaux de commerçants et d'artisans **qui autorisent la publicité** (lire leur règlement avant) | Utilisateur publie (Metricool : programmation) |
| Semaine 1 | **10 messages « Je vous ai cherché »** (§ 4.1) aux prospects prioritaires dont le test donne vraiment un « non » | Claude prépare, utilisateur envoie |
| Semaines 1 et 2 | **Tournée de l'affiche** : 10 commerces de passage (boulangerie, presse, garage, supérette), mairie, panneaux des supermarchés ; demander toujours l'accord | Utilisateur |
| Semaine 2 | Visites avec le test fait **devant le prospect**, sur son téléphone (§ 4.2) | Utilisateur |
| Semaine 3 | Story « Le test du pouce » rediffusée ; publication « Vous avez fait le test ? » (§ 4.4) | Utilisateur |
| Chaque vendredi | Bilan : démos demandées, rendez-vous, refus (tableau privé `50` § 8) | Claude |

## 4. Les textes prêts

### 4.1 Email « Je vous ai cherché » (premier contact, professionnel, en rapport avec son activité)

Règle d'or : **le test est fait le jour même** par Claude ou l'utilisateur, sur un téléphone, et la phrase
décrit **exactement** ce qui a été vu. Si le prospect sort bien et que son site est bon : on ne lui écrit pas.

> **Objet :** Je vous ai cherché sur mon téléphone
>
> Bonjour [Prénom Nom],
>
> Ce matin, j'ai fait un petit test : sur mon téléphone, j'ai tapé « [métier] [ville] », comme le ferait un
> client. [Constat exact, par exemple : « Votre entreprise n'apparaît pas dans les premiers résultats. » /
> « Votre site s'affiche en tout petit sur l'écran et le numéro ne s'appelle pas en le touchant. »]
>
> Je m'appelle [Prénom], je crée des sites internet pour les artisans et commerçants de Charente (DIG16).
> Je vous propose de refaire **gratuitement** la page d'accueil de votre entreprise, pour que vous voyiez
> la différence sur votre téléphone. Vous décidez ensuite, sans engagement.
>
> Je peux vous la montrer en 5 minutes, chez vous ou par téléphone. Cela vous dit ?
>
> [Prénom Nom] — DIG16 · [téléphone] · dig16.fr
> [Prénom Nom] EI · SIREN [numéro] · [adresse]
> Vous ne souhaitez plus recevoir de message de ma part ? Répondez simplement « STOP ».

### 4.2 Visite (en personne, 1 minute)

> « Bonjour, [Prénom], je fais des sites internet pour les artisans du coin. Je vous prends trente secondes :
> vous avez votre téléphone ? Tapez “[son métier] [sa ville]”… Vous vous voyez ? [Laisser regarder.]
> Si vous voulez, je refais votre page d'accueil gratuitement et je reviens vous la montrer. Vous décidez
> après. Je vous laisse cette affiche : le QR code mène à mon site. »

Si la réponse est non : merci, au revoir, noté comme refus définitif (`50` § 2).

### 4.3 Appel (ouverture)

> « Bonjour, [Prénom] de DIG16, à [ville]. Je vous appelle parce que j'ai cherché “[métier] [ville]” sur mon
> téléphone ce matin et [constat exact]. Je refais gratuitement la page d'accueil des entreprises du coin
> pour qu'elles voient la différence. Je peux vous préparer la vôtre ? »

### 4.4 Légendes des publications

- **Carrousel (semaine 1)** : « Le test du pouce 👍 30 secondes, votre téléphone, votre métier et votre
  ville. Vous êtes où ? Faites le test, puis glissez jusqu'au bout. Un “non” ? Je refais votre page
  d'accueil gratuitement : dig16.fr »
- **Story** : « Faites le test du pouce maintenant 👇 Réponse en 30 secondes. »
- **Semaine 3** : « Vous avez fait le test du pouce ? Dites-moi en commentaire ce que vous avez trouvé
  (sans nommer personne 🙂). Et si le résultat ne vous plaît pas : dig16.fr »
- **Groupes locaux** : « Bonjour à tous, je viens de lancer DIG16 en Charente : des sites internet pour
  artisans et commerçants. Petit test gratuit à faire sur votre téléphone : tapez votre métier et votre
  ville… vous êtes où ? Si le résultat ne vous plaît pas, je refais votre page d'accueil gratuitement pour
  que vous voyiez la différence. Bonne journée ! »

## 5. Garde-fous (vérifiés, sans exception)

- **Rien avant l'immatriculation** : identité, SIREN et téléphone visibles partout (`50` § 2).
- **Professionnels seulement**, jamais de particuliers ; jamais les secteurs exclus (`CLAUDE.md`).
- **Constat exact et du jour** dans chaque message personnalisé ; jamais « votre site est nul » ni critique
  d'un concurrent ; aucun chiffre inventé (aucun pourcentage de clients, aucune durée « 3 secondes »).
- **Démos personnalisées** : montrées en direct, jamais envoyées, et avec ses photos ou son logo seulement
  après son accord (décision du 05/10).
- **Affiches** : uniquement avec l'accord du commerçant ou sur les panneaux prévus pour ça ; jamais d'affichage
  sauvage.
- Un « STOP » ou un refus = plus jamais recontacté.

## 6. Ce qu'on mesure (sans inventer de taux)

Démos demandées (formulaire, appels, messages), démos montrées, rendez-vous, signatures, refus, d'où vient
chaque demande (affiche, réseaux, email, visite). Tableau privé (`50` § 8). Bilan chaque vendredi ; on garde
ce qui fait venir des demandes, on arrête le reste.
