# Vidéo verticale « Le test du pouce » (09/10/2026)

- `test-du-pouce.mp4` : 18,1 s, 1080 × 1920, H.264 + AAC, −15,4 LUFS (2,9 Mo). Pour Reel Instagram et Facebook,
  Short YouTube, TikTok, statut WhatsApp. Campagne : `62-campagne-test-du-pouce.md` ; idée notée dans `46` (vidéo DBQqB8eqpFI).
- Texte (`texte.txt`) : « Prenez votre téléphone. Tapez votre métier et votre ville. Vous êtes où ? Pas là ? Ou votre
  numéro ne s'appelle pas d'un geste ? Je refais gratuitement votre page d'accueil. Le test du pouce, sur Dig seize point F R. »
  Écran final : dig16.fr/test-du-pouce, « Faites le test en 30 secondes ».
- Voix « Algieba » (`gemini-3.8-flash-tts`, choisie par l'utilisateur le 08/10), via `api/voix` du relais : `voix-Algieba.wav`.
  Musique originale (`../dig16-presentation/musique.py`), baissée sous la voix.
- Rien d'inventé : recherche « menuisier cognac » et numéro « 05 •• •• •• •• » fictifs ; démo « Atelier Végétal » (fictive)
  avec le bas masqué (sa note et ses avis de maquette ne doivent pas apparaître dans une publicité).
- Refaire : `python3 fabriquer.py` (débuts de phrase repérés automatiquement dans la voix ; ALERTE si polices non chargées,
  si le nombre de phrases change ou si un texte sort de la marge). Images de contrôle dans `controle/` (non versionnées).
- **Comme toute la campagne : rien ne se publie avant la validation de l'entreprise** (identité visible, `50` § 2).
