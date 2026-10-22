# 4 Composants NextJS que tu dois installer !

Vidéo : https://youtu.be/AHGqOknBLHs · durée 7:57 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de présenter quatre composants clés implémentés dans l'application Next.js « nowts.app » pour améliorer l'expérience utilisateur, notamment la gestion des alertes de dialogue, des abonnements Stripe, des notifications de recherche, et des formulaires avec gestion des modifications non sauvegardées.
2)
- nowts.app : application/plateforme (non précisé si payant ou gratuit) présentée comme un boilerplate / collection de composants pour SaaS Next.js.
- DialogProvider / useDialogStore : composant/store (gratuit/inclus) pour gérer et afficher dynamiquement des fenêtres de dialogue (confirmation, suppression) accessibles partout dans l'application.
- createSearchParamMessageUrl : fonction/utilitaire (gratuit/inclus) pour injecter des messages (succès, erreur) dans les URLs et gérer les notifications de type « toast ».
- FormUnsavedBar / useWarnIfUnsavedChanges : composant et hook (gratuit/inclus) pour détecter et avertir l'utilisateur en cas de modifications non sauvegardées dans un formulaire avant de quitter la page.
3) Astuces :
- Utiliser un store global pour ouvrir et fermer des fenêtres de dialogue (comme une confirmation de suppression) sans multiplier le code UI dans chaque page.
- Passer des messages d'erreur ou de succès via les paramètres d'URL pour afficher des toasts de manière robuste après une redirection.
- Mettre en place un mécanisme global de détection des changements de formulaire non enregistrés pour empêcher la perte de données lors de la navigation.
4) Chiffres :
- Plan Pro de l'application mentionné à 49 $ / mois (affirmé par l'auteur).
