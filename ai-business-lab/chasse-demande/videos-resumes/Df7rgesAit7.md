# Df7rgesAit7 — reel Instagram @henriexploria (envoyé le 22/11)

## Tri pour DIG16 (22/11)

- **Réserve** : effets sonores (bruitages) posés automatiquement sur une vidéo montée par Claude. Outils cités : Openverse (bibliothèque de sons sous licences libres, réelle), « Earshot » et « real-sfx » (dépôts NON trouvés sur GitHub le 22/11 : noms à confirmer, l'auteur ne les donne qu'en message privé contre un commentaire).
- Rien installé : nos vidéos « Le conseil DIG16 » ont une voix et pas de bruitages ; à ressortir pour un film de lancement.
- Chiffre « 5 millions de sons » : affirmé par l'auteur, non vérifié.

Légende : henriexploria Commente "SFX" et je t’envoie les outils et le prompt directement en message privé View all 1,588 comments
Durée : 48 s

Voici les informations récapitulées d'après la vidéo :

---

### 1) Idée principale
Améliorer et automatiser l'ajout d'effets sonores (SFX) dans les montages vidéo réalisés par l'IA **Claude** grâce à l'enchaînement de 3 outils gratuits et d'un prompt spécifique, afin d'éviter le rendu « son IA bâclé ».

---

### 2) Outils, sites, skills ou méthodes présentés

* **Claude** *(IA / Agent)* : L'assistant/agent IA qui effectue le montage et orchestre le processus grâce au prompt.
* **Openverse** *(Outil N°1)* : Donne accès à une bibliothèque de sons gratuits que l'agent Claude peut rechercher et télécharger tout seul.
* **Earshot** *(Outil N°2)* : Sert de système d'évaluation sonore à Claude (qui ne peut pas entendre). Il génère et teste les sons, choisit celui qui fonctionne le mieux ou en génère un nouveau de zéro si aucun ne convient.
* **real-sfx** *(Outil N°3)* : Analyse le montage vidéo pour repérer chaque moment nécessitant un effet sonore (ex. un *whoosh* quand un élément apparaît) et le positionne exactement au bon endroit.
* **Le Prompt** *(Méthode)* : Une série d'instructions fournies à Claude pour automatiser et enchaîner l'utilisation de ces trois outils.

---

### 3) Ce que l'auteur dit de leur prix
L'auteur affirme que cette stack de 3 outils permet de régler le problème **gratuitement** (les sons d'Openverse sont également qualifiés de gratuits).

---

### 4) Chiffres cités par l'auteur
* **3** (outils dans la stack).
* **5 millions** (nombre de sons gratuits accessibles sur Openverse).

---

### 5) Application pour un entrepreneur solo (vente de sites web à des artisans)
D'après ce qui est présenté dans la vidéo, cet entrepreneur peut :
* **Créer des vidéos de présentation ou démos dynamiques** pour les sites de ses clients artisans (ou pour sa propre communication/prospection) en animant des éléments visuels et en y ajoutant automatiquement des effets sonores professionnels.
* **Automatiser le montage sonore** sans avoir besoin de compétences particulières en montage vidéo/audio (« nul en montage vidéo »), en s'appuyant uniquement sur Claude, le prompt et la stack d'outils présentés.
## Complément du 22/11 : fiche PDF de l'auteur (envoyée par l'utilisateur)

La fiche (3 pages) ne donne **aucun lien** vers « Real SFX » ni « Earshot » ; elle précise seulement que les trois outils doivent être « connectés dans la config » de Claude (donc des connecteurs ou skills à installer, non identifiés). Elle contient la méthode, à retenir pour un futur film avec bruitages :
1. lister les moments qui méritent un son (apparition d'un texte, coupe franche, clic), avec leur minutage ; ignorer ce que la voix ou la musique couvre déjà ;
2. chercher 3 sons candidats par moment (moins de 2 secondes), noter la licence de chacun ;
3. écouter et choisir : le son colle à l'image, il est propre, il ne fait pas « bon marché » ; sinon en créer un autre ;
4. placer au minutage exact, toujours moins fort que la voix, varier les sons, un seul son si deux moments sont à moins d'une demi-seconde ; mieux vaut trop peu que trop ;
5. réécouter le tout ; 6. tableau final : minutage, rôle, origine et licence de chaque son, moments laissés sans son.

Faisable chez nous sans ces outils : sons d'Openverse (licence lue son par son) et contrôle par notre relais (écoute par Gemini), montage par ffmpeg.
