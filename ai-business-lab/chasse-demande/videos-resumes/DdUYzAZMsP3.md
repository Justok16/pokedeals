# Reel Instagram DdUYzAZMsP3 (@dryxio.us, envoyé par l'utilisateur le 17/11/2026) — « 10 outils SEO »

Lu le 17/11 par `outils/resumer_reel_instagram.py` (vidéo 27 s, Gemini via le relais, modèles de secours).

## Résumé

### 2) Outils et méthodes présentés (noms exacts et rôles)

1. **Google Search Console** : Voir ce qui marche déjà sur le site.
2. **Keyword Planner** : Récupérer des données de mots-clés.
3. **Google Trends** : Voir ce qui va exploser (identifier les tendances de recherche).
4. **AnswerThePublic** : Voir ce que les gens cherchent vraiment.
5. **Ubersuggest** : Trouver toutes les astuces (d'optimisation / de mots-clés).
6. **Screaming Frog** : Réparer ce qui est cassé sur le site (audit d'erreurs techniques).
7. **PageSpeed Insights** : S'assurer que le site n'est pas lent.
8. **Rich Results Test** : Vérifier la mise en forme pour apparaître en extrait enrichi dans les résultats Google.
9. **Yoast SEO** (affiché *Yoast SEO*, prononcé *Yoast*) : Nettoyer toutes les pages du site.
10. **Google Business Profile** : Être bien classé dans sa zone géographique (référencement local).

---

Prix : non dits dans la vidéo. L'auteur propose d'envoyer « 10 liens et prompts » en message privé (non demandé).

## Tri pour DIG16 (17/11)

- **Déjà en place** : Search Console (via OpenSEO, statistiques du lundi), fiche Google (Business Profile), vitesse et affichage téléphone contrôlés à chaque mise en ligne (`test_pages.py`, `controle_global.py`), données structurées présentes sur le site.
- **Appliqué le 17/11** : nouveau contrôle `donnees_structurees()` dans `outils/test_pages.py` (équivalent local du « Rich Results Test ») : chaque bloc JSON-LD doit être valide, avec `@context` schema.org et `@type` ; 8 blocs du site : OK.
- **En réserve** (gratuité à relire à la source le jour de l'usage) : Google Trends et Keyword Planner (mots-clés de chaque site client), AnswerThePublic (questions réelles pour la FAQ d'un client), Screaming Frog (audit technique d'un ancien site de prospect avant refonte).
- **Écarté** : Yoast SEO (extension WordPress : nos sites ne sont pas sous WordPress) ; Ubersuggest (doublon d'OpenSEO, déjà relié).
