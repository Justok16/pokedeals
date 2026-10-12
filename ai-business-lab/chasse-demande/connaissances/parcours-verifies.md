# Parcours vérifiés dans les applis (guidage pas à pas de l'utilisateur)

Créé le 11/10/2026 après la remarque de l'utilisateur : des indications de menus données de mémoire étaient
fausses (menus renommés, options disparues), ce qui lui a fait perdre du temps.

## Méthode obligatoire avant de guider l'utilisateur dans une appli ou un site

1. **Le faire soi-même d'abord** si un connecteur ou un outil le permet (Metricool, Gmail, Drive, Vercel, GitHub…).
   L'utilisateur n'agit que pour ce qui exige son compte ou son identité.
2. **Chercher ici** si le parcours a déjà été vérifié (tableau ci-dessous). Si oui, le donner tel quel.
3. Sinon, **lire la page d'aide officielle actuelle** de l'éditeur (recherche web, date de la page) avant d'écrire
   les étapes, et citer le lien. Ne jamais décrire un menu de mémoire.
4. **Un écran à la fois** quand le parcours n'est pas vérifié : demander une capture de l'écran de départ, donner
   seulement la ou les 2 prochaines touches, puis attendre la capture suivante. Dire clairement « je n'ai pas vu
   cet écran, envoie-moi une capture si ça ne correspond pas ».
5. **Prévoir l'alternative** dès le départ (ex. « si l'option n'existe pas, on passe par X »).
6. **Vérifier le résultat soi-même** quand c'est possible (API, page publique), sans conclure trop vite : une
   absence d'erreur n'est pas une preuve (leçon Threads/Metricool du 11/10).
7. **Consigner ici** chaque parcours confirmé par une capture de l'utilisateur, avec la date.

## Parcours confirmés (captures de l'utilisateur)

| Appli | But | Parcours exact | Vu le |
|---|---|---|---|
| Metricool (appli Android) | Voir / changer la marque active | Rond du logo de la marque **en bas à droite** → liste « Marques » (⚙️ à droite de chaque marque) | 11/10/2026 |
| Metricool (appli Android) | Relier un réseau | Rond en bas à droite → ⚙️ de la marque → « Paramètres des marques » → **Connexions** → « Connecter » sur la ligne du réseau | 11/10/2026 |
| Metricool (appli Android) | Piège | L'appli peut être ouverte sur une **autre marque/compte** (« Marque vide ») : toujours vérifier le nom de la marque avant de connecter | 11/10/2026 |
| Metricool (API) | Piège | `getBrandSettings` n'affiche que Facebook/Instagram dans `networksData` ; une publication acceptée sur un réseau ne prouve pas qu'il est relié | 11/10/2026 |
| Instagram (Android) | Lien cliquable dans la bio | Modifier le profil → **Liens** → Ajouter un lien → Ajouter un lien externe (le texte de la bio n'est jamais cliquable) | 11/10/2026 |
| Instagram (Android) | Piège | « Nom » (affiché) ≠ « Nom d'utilisateur » (identifiant `dig16fr`, à ne jamais changer) ; ancien identifiant récupérable 14 jours | 11/10/2026 |
| Threads (Android) | Ajouter le profil DIG16 | S'ouvre sur le compte personnel ; profil DIG16 ajouté depuis le compte Instagram `dig16fr` ; Modifier le profil : Nom, Bio, Centres d'intérêt, Liens, Confidentialité | 11/10/2026 |
| TikTok (Android) | Changer le nom | Modifier le profil → Nom : **bloqué 7 jours** après la création du compte | 11/10/2026 |
| TikTok (Android) | Compte professionnel | **N'existe plus** dans Paramètres → Compte ; seul « Deviens un compte Entreprise vérifié » (documents exigés). Metricool accepte le **compte personnel** (1re ligne TikTok de Connexions) | 11/10/2026 |
| TikTok (Android) | Mot de passe | Paramètres et confidentialité → Compte → **Mot de passe** (code envoyé par e-mail) | 11/10/2026 |
| YouTube | Commentaire épinglé sur un Short | Ouvrir le Short → bulle 💬 à droite → écrire → ⋮ du commentaire → Épingler | 11/10/2026 |
| YouTube Studio | Avertissement règlement | Bandeau en haut : formulation « mise en garde » + formation de 7 questions (expire en 90 jours) | 11/10/2026 |
| Metricool (appli Android) | Relier la fiche Google | Connexions → ligne « Google Business Profile » → Connecter (fiche « Dig16 » reliée) | 12/10/2026 |
| Metricool (appli Android) | Relier YouTube | Connexions → ligne « YouTube, Connecter un canal » → chaîne « DIG16 » | 12/10/2026 |
| X (navigateur, inscription) | Piège | `dig16fr` déjà pris ; `dig16charente` disponible ; le **Nom refuse tout chiffre** à l'inscription (« Erreur lors de la validation du nom », trouvé par l'utilisateur) : s'inscrire avec un nom sans chiffre puis le changer dans Modifier le profil | 12/10/2026 |
