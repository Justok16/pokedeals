# Dot plots : Comment vraiment voir ce que font vos utilisateurs

Vidéo : https://youtu.be/e5-6rEwzxLs · durée 13:50 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) Sujet et thèse principale :
Sujet : L’utilisation des analyses de cohortes et du « dot plot » pour comprendre le comportement des utilisateurs.
Thèse principale : S’appuyer uniquement sur des métriques agrégées (comme le nombre total d’utilisateurs ou de l’activité globale) est trompeur. Pour savoir si les utilisateurs gardent et utilisent vraiment un produit, il faut analyser le comportement individuel dans le temps à l'aide de cohortes de rétention et, surtout, de graphiques de type « dot plot » (graphiques de points).

2) Notions expliquées :
- Cohort retention curves (courbes de rétention par cohorte) : Graphiques permettant de séparer les utilisateurs par groupes (par exemple, selon leur mois d'inscription) et de suivre leur taux de rétention au fil du temps (mois +0, +1, +2...).
- Fréquence, intensité et pacing : La manière dont les utilisateurs interagissent avec le produit (à quelle fréquence, avec quels types d'actions et à quel rythme).
- Données agrégées : Des chiffres globaux (comme le nombre total d'utilisateurs actifs) qui masquent la réalité individuelle.
- Dot plot (graphique à points) : Représentation visuelle sous forme de grille où chaque ligne est un utilisateur (ou un client) et chaque colonne représente une période (par exemple un jour de la semaine). Un point (ou un symbole) indique qu’une action spécifique a été réalisée par cet utilisateur à ce moment-là. Cela permet d'identifier visuellement des patterns comportementaux (ex. : utilisateurs en semaine vs utilisateurs le week-end, taux de désabonnement, utilisateurs réguliers vs utilisateurs intermittents).
- DAU (Daily Active Users / Utilisateurs actifs quotidiens) : Nombre d'utilisateurs uniques actifs par jour. Un graphique DAU agrégé peut stagner ou baisser globalement sans montrer que certains utilisateurs sont en réalité extrêmement fidèles tandis que d'autres abandonnent très vite.

3) Chiffres, taux, plafonds et règles fiscales :
- Aucun chiffre précis, taux, plafond ou règle fiscale n'est cité dans cette vidéo.

4) Conseils concrets et limites ou risques :
- Ne pas se fier uniquement aux métriques globales et agrégées (qui peuvent donner une fausse impression de croissance constante alors que le produit perd ses utilisateurs).
- Créer un « dot plot » (grille utilisateurs/jours) pour visualiser les actions individuelles et repérer des tendances invisibles dans les moyennes (ex. : segmentation des usages entre semaine et week-end, identification rapide des utilisateurs qui ne reviennent jamais après le premier jour).
- Encoder l'état des utilisateurs (ex. : type d'appareil, pays, première utilisation) à l'aide de symboles ou de couleurs pour affiner l'analyse comportementale.
- Limite : Les graphiques à points (« dot plots ») deviennent complexes à lire ou ingérables manuellement lorsque la base d'utilisateurs grandit considérablement (nécessite d'échantillonner ou d'automatiser la visualisation pour des milliers ou millions d'utilisateurs, bien que le principe reste conceptuellement transposable à l'échantillonnage).

5) Produits, applications ou entreprises cités :
- Spotify (mentionné comme exemple hypothétique d'application musicale pour illustrer le suivi d'événements comme « écouter une chanson » ou « rejoindre une playlist publique »).
- GitHub (mentionné pour sa visualisation sous forme de matrice de contributions annuelle en carrés verts, apparentée à un principe de grille temporelle).
- Aucun produit ou application n'est présenté comme une publicité de l'auteur ; il s'agit d'exemples conceptuels ou pédagogiques.
