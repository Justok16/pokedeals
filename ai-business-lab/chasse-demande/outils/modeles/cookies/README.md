# Bandeau cookies tarteaucitron.js (prêt le 03/11/2026)

Demande de l'utilisateur du 03/11 (« TOUT »). tarteaucitron.js 1.37.0 (MIT, dépôt AmauriC/tarteaucitron.js, publié le
15/10/2026 ; paquet et README lus le 03/11/2026). **À n'installer que si le site client dépose des traceurs soumis à
consentement** (carte Google, vidéo YouTube, publicité, mesure d'audience non exemptée). dig16.fr n'en a pas besoin
(mesure Metricool sans cookie).

## Mise en place
1. `sh outils/modeles/cookies/recuperer.sh <dossier_du_site>` : copie la version figée (fichiers minifiés + français)
   dans `<site>/tarteaucitron/` ; le site reste autonome (pas de script chargé depuis un autre domaine).
2. Coller `config.html` dans le `<head>` de chaque page, adapter `privacyUrl`, puis déclarer les services utilisés
   (ex. `tarteaucitron.user.googlemapsKey`, `(tarteaucitron.job = tarteaucitron.job || []).push('youtube');`) d'après le
   README de la version.
3. Réglages choisis (valeurs du README 1.37.0) : consentement jamais automatique (`highPrivacy: true`), bouton « Tout
   refuser » aussi visible que « Tout accepter » (`DenyAllCta` / `AcceptAllCta`), bandeau au milieu, icône de gestion
   en bas à droite. La règle exacte de la CNIL est relue à la source au moment de la pose.
4. Contrôles : `sh outils/unlighthouse/audit.sh`, essai « Tout refuser » (aucune carte ni vidéo chargée) puis
   « Tout accepter », sur téléphone et PC.
