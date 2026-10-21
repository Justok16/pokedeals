# Vidéo YouTube CCUSpJkAfgU : « Motion graphics 3D avec Claude et Three.js » (envoyée le 21/10/2026)

Source : https://youtu.be/CCUSpJkAfgU, transcription vidIQ (anglais) lue en entier le 21/10/2026. Passage publicitaire
(« Applied AI Mastermind », payant) ignoré.

Principe : la vidéo est une page web animée (Three.js pour la 3D, « shaders » pour reflets, lueurs, particules),
filmée image par image dans un navigateur invisible (60 images/s), puis assemblée. **C'est exactement notre méthode**
(`videos/conseils/fabriquer.py`, `videos/lancement/fabriquer.py`), mais en 2D plate aujourd'hui.

| Conseil | Décision DIG16 |
|---|---|
| Three.js + shaders pour un rendu 3D « haut de gamme » (verre dépoli, particules, reflets) | 🟡 **À essayer** sur les vidéos « Le conseil DIG16 » 11 à 15 (prévues début novembre) : essai de 10 s proposé à l'utilisateur avant tout changement de style |
| La caméra se déplace entre les éléments (vrai espace 3D, pas un diaporama) | 🟡 Idem |
| Décrire chaque scène avec ses temps précis | ✅ Déjà le cas (tableau des phrases et des écarts dans `fabriquer.py`) |
| Demander un rendu « professionnel et sobre », proposer 3 idées en texte avant de produire | ✅ À reprendre pour les prochaines vidéos |
| **Boucle de vérification** : textes trop petits, éléments qui se chevauchent, avant d'envoyer | ✅ Déjà en place (planches de contrôle, `44`) ; à étendre aux scènes 3D |
| Coût : quasi nul avec l'abonnement (≈ 37 000 jetons pour 15 s selon la vidéo, non vérifié) | ✅ Budget 0 € respecté ; aucun modèle vidéo payant (SeeDance, etc.) |
| Garder le mouvement réduit possible | ⚠️ Règle DIG16 : pas de 3D sur les sites clients sans version « mouvement réduit » ; dans les vidéos, textes lisibles au téléphone (taille minimale de `44`) |
