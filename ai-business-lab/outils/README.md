# outils/ — le moteur de classement du portefeuille

## Pourquoi du code plutôt qu'un tableau écrit à la main

Un classement écrit à la main dans un document n'est ni vérifiable ni
rejouable : on ne peut pas savoir si l'ordre vient des faits ou de l'envie du
rédacteur. Ici, le classement est **le résultat** d'une grille de poids
explicite appliquée à des notes explicites. Contester la stratégie revient donc
à modifier un fichier et à relancer une commande.

## Fichiers

| Fichier | Rôle |
|---|---|
| `criteres.yaml` | Les 18 critères, leur poids et le sens d'une note haute (grille de référence) |
| `criteres-max-revenu.yaml` | Grille alternative : « revenu maximal, marché stable » — pour voir ce que devient le classement quand on ne regarde presque que l'argent |
| `concepts.yaml` | Les 16 concepts et leurs notes (0-5), avec les justifications en commentaire |
| `scorer.py` | Le calcul et les rendus (Markdown, CSV, détail) |
| `tests/test_scorer.py` | Garantit que le calcul est juste et qu'une donnée fausse casse |

## Utilisation

```bash
python scorer.py                 # classement Markdown (celui du document 02)
python scorer.py --criteres criteres-max-revenu.yaml   # la même chose, grille "revenu maximal"
python scorer.py --format csv    # pour le tableau de bord
python scorer.py --detail A2     # le détail des points d'un concept
python -m pytest tests/ -v       # vérifier le moteur
```

## Comment contester le classement

1. Vous pensez que l'avantage défendable est surpondéré ? Changez son poids dans
   `criteres.yaml` et relancez.
2. Vous pensez qu'un concept est sous-noté ? Changez sa note dans
   `concepts.yaml`, **en écrivant la raison en commentaire**.
3. Vous avez une nouvelle idée ? Ajoutez-la à `concepts.yaml` : si son score
   passe devant un concept actif, elle mérite un test (cf. `../04-niche-radar.md`).

Les notes actuelles sont des **hypothèses datées du 21/09/2026**. Elles doivent
bouger après le premier cycle de tests : c'est le signe que le dispositif
apprend.

## Ce que les tests garantissent (et ce qu'ils ne garantissent pas)

Ils garantissent que le calcul est correct, qu'un critère oublié ou une note
hors bornes casse au lieu de fausser silencieusement le classement, et que les
poids influencent réellement l'ordre.

Ils ne garantissent **pas** que les notes reflètent la réalité du marché. Ça,
seuls les tests de terrain décrits dans `../03-plan-execution.md` peuvent le dire.
