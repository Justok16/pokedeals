# Checklist de contrôle SEO — création ou refonte DIG16

Cette checklist complète le contrôle automatique des redirections. Elle doit être remplie avec le client et les accès réellement disponibles ; le script ne réalise pas ces vérifications.

## Avant la mise en ligne

- [ ] Confirmer le périmètre : simple changement d'hébergement sans changement d'URL, ou migration avec changement d'URL.
- [ ] Inventorier les URL existantes utiles : sitemap, Search Console, analytics et, si disponibles, journaux serveur et liens entrants importants.
- [ ] Associer chaque ancienne URL à sa destination réellement équivalente.
- [ ] Marquer explicitement les pages supprimées sans équivalent ; ne pas les rediriger automatiquement vers l'accueil.
- [ ] Vérifier le contenu des nouvelles pages, les liens internes et les liens canoniques auto-référents.
- [ ] Contrôler `robots.txt`, les directives `noindex`, les balises `canonical`, `hreflang` si le site en utilise, et le sitemap XML.
- [ ] Vérifier que les propriétés et variantes pertinentes de l'ancien et du nouveau site sont validées dans Google Search Console.
- [ ] Préparer un plan de retour arrière et sauvegarder les règles de redirection / la configuration avant modification.

## Au lancement

- [ ] Activer des redirections HTTP permanentes côté serveur, de préférence 301 ou 308.
- [ ] Éviter les chaînes : rediriger directement chaque ancienne URL vers sa destination finale.
- [ ] Vérifier qu'aucune ancienne URL n'entre dans une boucle.
- [ ] Éviter les redirections non pertinentes vers la page d'accueil ; utiliser 404 ou 410 quand le contenu n'a réellement pas d'équivalent.
- [ ] Lancer `migration_audit.py` sur le CSV de correspondances et analyser toutes les lignes FAIL, ERROR et WARNING.
- [ ] Vérifier manuellement les cas sensibles et un échantillon de pages représentatif sur ordinateur et mobile.

## Après la mise en ligne

- [ ] Mettre à jour les liens internes pour viser directement les nouvelles URL.
- [ ] Soumettre le nouveau sitemap dans Search Console.
- [ ] Pour un changement de domaine/sous-domaine, examiner l'outil de changement d'adresse Search Console (pas requis pour un simple passage HTTP vers HTTPS ou un changement de chemin sur le même domaine).
- [ ] Surveiller les erreurs 404/5xx, les redirections inattendues, les pages exclues et l'indexation dans Search Console.
- [ ] Comparer les tendances de trafic des anciennes et nouvelles URL.
- [ ] Conserver les redirections aussi longtemps que possible ; Google recommande généralement au moins un an.
- [ ] Archiver le CSV, le rapport, les corrections effectuées et la date du contrôle.

## Règles Google utilisées

Google recommande les redirections permanentes côté serveur (notamment 301/308), d'éviter les chaînes et de viser directement la destination finale. Si une chaîne est inévitable, Google conseille de la garder courte (idéalement au plus trois sauts et moins de cinq). Google déconseille de rediriger en masse des URL sans rapport vers une même page d'accueil ; le traitement de ces cas peut être celui d'une soft 404. Google recommande de conserver les redirections le plus longtemps possible, généralement au moins un an.

Source officielle : [Google Search Central — Site Moves and Migrations](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).
