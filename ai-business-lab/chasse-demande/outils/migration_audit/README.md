# DIG16 Migration Audit 0.4.5

Outil local de contrôle des redirections HTTP lors d'une refonte ou migration de site. Python standard library uniquement : aucune dépendance à installer.

## Ce que l'outil contrôle

- suit manuellement les redirections HTTP (301, 302, 303, 307, 308) jusqu'à la destination finale ;
- vérifie la destination finale contre la colonne `new_url` ;
- signale les redirections temporaires, les chaînes, boucles, destinations incorrectes, erreurs HTTP, réponses sans `Location` et redirections absentes ;
- utilise `HEAD`, avec repli sur `GET` lorsque le serveur répond 405 ou 501 ;
- détecte les CSV séparés par virgule, point-virgule ou tabulation ; ignore les lignes vides ;
- signale les lignes invalides, les correspondances dupliquées et les anciennes URL associées à plusieurs nouvelles URL ;
- considère les redirections HTTPS vers HTTP comme un échec bloquant ;
- signale les chaînes de redirections ; une chaîne de 5 sauts ou plus est un échec bloquant (Google recommande idéalement 3 sauts maximum et moins de 5) ;
- bloque par défaut les adresses IP non publiques (boucle locale, réseau privé, link-local, etc.) ; résout chaque hôte une seule fois par saut et épingle la connexion à l’adresse IP validée ;
- ignore les proxys définis dans les variables d’environnement afin que le contrôle IP s’applique à la connexion directe ; conserve la vérification TLS du nom d’hôte d’origine ;
- produit un CSV UTF-8 avec BOM, séparé par des points-virgules (ouverture simple dans Excel français).

## Limites

La protection réseau vise les destinations non publiques et réduit le risque SSRF ; elle ne remplace pas un pare-feu ou une politique de sécurité réseau. Le DNS est résolu avant chaque saut et l’IP vérifiée est celle utilisée pour la connexion, ce qui évite une seconde résolution au moment de se connecter. Le mode proxy système est volontairement désactivé. Le délai de requête ne garantit pas une durée maximale de résolution DNS sur tous les systèmes.

Ce n'est pas un crawler SEO complet. Il ne contrôle pas le contenu, les balises canonical, les liens internes, le sitemap, robots.txt, hreflang, l'indexation Google, les performances, ni la pertinence métier des redirections. Une réponse `HEAD` peut différer d'une réponse `GET` sur certains serveurs. Les règles de pare-feu, CDN, géolocalisation, authentification ou proxy peuvent modifier les réponses. Vérifier les cas signalés manuellement avant toute modification en production.

L'outil effectue des requêtes HTTP(S) vers les URL fournies dans le CSV. N'utiliser que sur des sites et URL que vous êtes autorisé à contrôler. Il ne crée et ne modifie aucune redirection sur le serveur.

## Prérequis

- Windows 10/11 ou environnement compatible ;
- Python 3.11+ (Python 3.10 a atteint sa fin de support le 1er octobre 2026) accessible avec la commande `py` ou `python` ;
- accès réseau aux sites audités.

Aucune bibliothèque tierce n'est requise. L’archive contient `MANIFEST.sha256` pour vérifier l’intégrité des fichiers après extraction (par exemple avec `Get-FileHash` sous PowerShell).

## Utilisation Windows

1. Extraire l'archive ZIP.
2. Ouvrir `exemple_correspondances.csv` et remplacer les URL de démonstration par les correspondances réelles ; conserver les colonnes `old_url` et `new_url`.
3. Glisser le fichier CSV sur `LANCER_AUDIT.bat`, ou exécuter dans PowerShell :

```powershell
py -3 .\migration_audit.py .\exemple_correspondances.csv -o .\rapport_migration.csv
```

Options : `--timeout 12`, `--max-redirects 10`, `--version` et `--allow-private-hosts` (uniquement pour un environnement de préproduction maîtrisé ; ne pas activer pour des URL non fiables).

Le code de sortie vaut 0 si aucun échec bloquant n'est détecté, 1 si au moins un échec est trouvé, 2 en cas d'erreur d'entrée/sortie. Une ligne strictement dupliquée est conservée dans le rapport comme avertissement, sans nouvelle requête réseau. Les avertissements (par exemple chaîne de plusieurs redirections) sont distincts des échecs.

## Intégration continue

Le workflow GitHub Actions du dossier `.github/workflows/` exécute la compilation et les tests sur Windows et Ubuntu, avec Python 3.11 à 3.15. Les actions officielles sont épinglées sur leurs SHA complets, vérifiés sur les pages de versions amont et Dependabot surveille leurs mises à jour chaque semaine. Il ne lance aucun audit réseau externe.

## Tests

Sous Windows, `TESTER.bat` exécute la vérification de version Python, la compilation, les 50 tests et la construction/vérification d’une archive temporaire. En ligne de commande :

```powershell
py -3 -m py_compile .\migration_audit.py .\build_release.py
py -3 -m unittest discover -s tests -v
```

## Construire une archive vérifiée

Le script `build_release.py` génère un ZIP déterministe, régénère `MANIFEST.sha256`, vérifie chaque fichier inclus, puis crée le fichier externe `.sha256` pour l’archive. Il exclut les caches Python, les environnements virtuels et les répertoires de build. Le ZIP doit être créé hors du dossier source :

```powershell
py -3 .\build_release.py --output ..\dig16_migration_audit.zip
```

Le script vérifie automatiquement l’archive et son manifeste avant de terminer.

La suite comprend 50 tests : les tests HTTP utilisent un serveur local éphémère et les tests de release vérifient le ZIP, le manifeste SHA-256, l’exclusion des fichiers temporaires, la reproductibilité, la détection des archives et sommes de contrôle altérées, les fichiers SHA-256 mal formés et les membres ZIP dupliqués, et la cohérence des numéros de version. Aucun site tiers n’est sollicité par la suite.

## Procédure SEO à garder en parallèle

Voir `CHECKLIST_MIGRATION_SEO.md` pour la checklist de préparation, de mise en ligne et de surveillance.

Avant mise en ligne : inventorier les URL utiles, établir et relire les correspondances, vérifier les liens internes, canonical, sitemap, robots/noindex et hreflang. Après mise en ligne : exécuter l'audit, corriger les redirections en chaîne et les destinations erronées, puis contrôler Search Console et les journaux serveur. Ne pas rediriger en masse des URL supprimées vers la page d'accueil sans équivalence réelle.
