# MIGRATION — sortir ce dossier dans son propre dépôt

Ce dossier est **autonome** : il ne dépend d'aucun fichier de `pokedeals`. Ce
document contient tout ce qu'il faut pour le déplacer, y compris si la session
qui l'a préparé n'existe plus.

## Prérequis (action utilisateur, une seule fois)

Créer sur github.com un dépôt **vide** nommé `ai-business-lab` — **sans** README,
**sans** `.gitignore`, **sans** licence. Un dépôt pré-initialisé ferait échouer
la première poussée.

> La session Claude ne peut pas créer ce dépôt elle-même : l'application GitHub
> renvoie `403 Resource not accessible by integration`.

## Procédure

```bash
# 1. Extraire le dossier vers un emplacement de travail, sans les caches Python
mkdir -p /tmp/ai-business-lab
tar --exclude='__pycache__' --exclude='.pytest_cache' \
    -cf - -C ai-business-lab . | tar -xf - -C /tmp/ai-business-lab
cd /tmp/ai-business-lab

# 2. Ces deux fichiers ne servent plus une fois le dossier devenu un dépôt
rm -f MIGRATION.md

# 3. Corriger les chemins : ils deviennent relatifs à la racine du dépôt
sed -i 's|cd ai-business-lab/outils|cd outils|g' 02-portefeuille-concepts.md lancement/README.md
sed -i 's|ai-business-lab/04-niche-radar.md|04-niche-radar.md|' modeles/prompts-agents.md
sed -i 's|`ai-business-lab/opportunites/|`opportunites/|' 04-niche-radar.md
grep -rn "ai-business-lab/" --include="*.md" . || echo "aucune référence résiduelle"

# 4. Vérifier que tout fonctionne dans la nouvelle arborescence
cd outils && python -m pytest tests/ -q && python scorer.py | head -4 && cd ..

# 5. Publier
git init -b main
git add -A
git commit -m "Dossier stratégique initial : étude, portefeuille noté, plan d'exécution"
git remote add origin https://github.com/Justok16/ai-business-lab.git
git push -u origin main
```

## Après la poussée, et seulement après

Nettoyer `pokedeals`, dans cet ordre :

1. `git rm -r ai-business-lab/`
2. Retirer le job `scoring_strategie` de `.github/workflows/tests.yml`
   (il ne reste que le job `pytest` du scraper, inchangé).
3. Retirer la section `## ai-business-lab/` du `README.md` racine, ainsi que la
   ligne correspondante dans le bloc « Structure du dépôt ».
4. Pousser sur `claude/ai-business-portfolio-strategy-96yf4g`.
5. Fermer la **PR #118** avec un commentaire renvoyant vers le nouveau dépôt.

**Ne jamais faire l'étape 1 avant que la poussée de l'étape 5 de la procédure
ci-dessus ait réussi** : tant que le nouveau dépôt n'existe pas, cette branche
est le seul endroit durable où ce travail existe.

## Ce que contient déjà le dossier pour être autonome

- `.gitignore` — caches Python, fichiers système, brouillons de travail.
- `.github/workflows/tests.yml` — CI du nouveau dépôt : lance les 10 tests du
  moteur de classement depuis `outils/`. **Ce fichier est inerte tant que le
  dossier est un sous-dossier de `pokedeals`** : GitHub Actions ne lit que le
  `.github/workflows/` situé à la racine d'un dépôt.
- `README.md` — présente le projet pour lui-même.
