# Changelog

## 0.4.5 — 4 novembre 2026

- Synchronisation du numéro de version entre la constante CLI, le README, le changelog et le journal de vérification.
- Le constructeur de release rejette les membres de fichiers ZIP dupliqués.
- Vérification stricte du fichier SHA-256 externe : format hexadécimal de 64 caractères, nom d'archive attendu et empreinte exacte.
- Ajout de tests couvrant les sidecars mal formés, les noms d'archive incohérents et les entrées ZIP en double.
- Le workflow CI construit et vérifie une archive sur chaque combinaison Windows/Ubuntu et Python 3.11–3.15 après les tests unitaires.
- Le test de cohérence vérifie aussi le nombre de tests documenté.
- Protection contre l’écrasement du CSV source via un chemin alternatif ou un lien physique (hard link), avec test de régression.

## 0.4.4 — 4 novembre 2026

- Correction de la constante `VERSION` du programme, qui n'était pas synchronisée avec le README et le journal de vérification.
- Ajout d'un constructeur de release déterministe (`build_release.py`) : manifeste SHA-256, contrôle du ZIP, vérification du fichier externe `.sha256` et exclusion des caches/environnements virtuels.
- Ajout de tests de release couvrant la reproductibilité, l'intégrité, l'exclusion des fichiers temporaires, le rejet d'une sortie dans le dossier source et la cohérence des métadonnées de version.
- Le workflow CI construit et vérifie aussi une archive après les tests.
- Correction du SHA-256 externe qui ne correspondait pas au ZIP de la version précédente ; ajout d’un test de release pour prévenir toute désynchronisation.
- `TESTER.bat` exécute désormais le contrôle Python, la compilation, les tests et un build de vérification complet, depuis son propre dossier même s’il est lancé par double-clic ailleurs.
- Ajout d’un test vérifiant que la somme de contrôle externe détecte une archive altérée.

## 0.4.3 — 4 novembre 2026

- Réconciliation du numéro de version entre le code, le README et le journal de vérification.
- Lecture CSV stricte : colonnes supplémentaires et guillemets mal formés signalés sans exception non gérée.
- Neutralisation des cellules du rapport pouvant être interprétées comme des formules dans un tableur.
- Refus d'exécuter le CLI avec Python antérieur à 3.11.
- Matrice CI Windows/Linux sur Python 3.11 à 3.15 ; actions GitHub épinglées sur leurs SHA complets vérifiés.
- Ajout de six tests de régression et suppression d'une assertion dupliquée.

## 0.4.2 — état de travail retiré

Le précédent paquet de travail présentait une incohérence entre le numéro de version annoncé, la constante de version du script, le nombre de tests et le workflow CI. Il n'est pas conservé comme version livrable de référence. Les corrections correspondantes sont intégrées et vérifiées dans la 0.4.3.

## 0.4.1

- Une redirection HTTPS vers HTTP devient un échec bloquant.
- Une chaîne d'au moins cinq redirections est signalée comme longue et bloquante ; les chaînes plus courtes restent des avertissements.
- Le CLI rejette les délais `NaN` et infinis.
- Ajout de tests sur les réponses DNS mixtes (IP publique + IP privée), les chaînes longues et les délais invalides.
- Première intégration continue Windows/Linux (matrice initiale retirée en 0.4.3 au profit des versions Python maintenues).

## 0.4.0

- Résolution DNS avant chaque saut et connexion épinglée sur l'IP effectivement vérifiée ; blocage par défaut des destinations non publiques.
- Désactivation des proxys d'environnement pour éviter de déléguer la résolution à un proxy ; validation TLS conservée sur le nom d'hôte.
- Détection des correspondances strictement dupliquées et des en-têtes CSV en double.
- Signalement des migrations HTTPS vers HTTP.
- Correction de la normalisation du port explicite `:0` et du diagnostic des échecs réseau.
- Ajout des options `--version` et `--allow-private-hosts`, du parcours CLI et de la protection contre l'écrasement du CSV source.

## 0.3

- Détection des séparateurs CSV virgule, point-virgule ou tabulation ; en-têtes normalisés et lignes vides ignorées.
- Checklist SEO de migration.
- Vérification manuelle des redirections sans suivi automatique, comparaison de destination, statuts temporaires/permanents, boucles et chaînes.
- Lecture CSV avec BOM, validation des URL et détection des correspondances contradictoires.
- Tests automatisés sur serveur local intégré.

