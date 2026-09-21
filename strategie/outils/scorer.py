"""Classement reproductible du portefeuille de concepts.

Pourquoi ce fichier existe : un classement ecrit a la main dans un document
n'est pas verifiable et ne se rejoue pas. Ici, le classement est le RESULTAT
d'une grille de poids explicite (criteres.yaml) appliquee a des notes
explicites (concepts.yaml). Changer un poids ou une note et relancer le script
rejoue tout le classement -- c'est ce qui permet de discuter la strategie sur
des chiffres plutot que sur une intuition.

Usage :
    python scorer.py                 # tableau Markdown du classement
    python scorer.py --format csv    # meme chose en CSV (tableau de bord)
    python scorer.py --detail A2     # le detail des points d'un concept
"""

from __future__ import annotations

import argparse
import csv
import io
from dataclasses import dataclass
from pathlib import Path

import yaml

DOSSIER = Path(__file__).resolve().parent
FICHIER_CRITERES = DOSSIER / "criteres.yaml"
FICHIER_CONCEPTS = DOSSIER / "concepts.yaml"

NOTE_MAX = 5


@dataclass(frozen=True)
class Critere:
    nom: str
    poids: float
    sens: str


@dataclass(frozen=True)
class Concept:
    id: str
    nom: str
    cluster: str
    resume: str
    notes: dict[str, int]


class ErreurDonnees(ValueError):
    """Donnee de notation invalide (note hors bornes, critere manquant...)."""


def charger_criteres(chemin: Path = FICHIER_CRITERES) -> list[Critere]:
    brut = yaml.safe_load(chemin.read_text(encoding="utf-8"))
    criteres = [
        Critere(nom=nom, poids=float(valeur["poids"]), sens=str(valeur["sens"]))
        for nom, valeur in brut["criteres"].items()
    ]
    if not criteres:
        raise ErreurDonnees("aucun critere defini")
    return criteres


def charger_concepts(chemin: Path = FICHIER_CONCEPTS) -> list[Concept]:
    brut = yaml.safe_load(chemin.read_text(encoding="utf-8"))
    return [
        Concept(
            id=str(c["id"]),
            nom=str(c["nom"]),
            cluster=str(c.get("cluster", "")),
            resume=" ".join(str(c.get("resume", "")).split()),
            notes={str(k): int(v) for k, v in c["notes"].items()},
        )
        for c in brut["concepts"]
    ]


def valider(concept: Concept, criteres: list[Critere]) -> None:
    """Refuse silencieusement rien : une donnee fausse doit casser tot.

    Un critere oublie fausserait le score vers le bas sans prevenir, et une
    note a 7/5 le gonflerait : dans les deux cas le classement mentirait.
    """
    attendus = {c.nom for c in criteres}
    manquants = sorted(attendus - set(concept.notes))
    if manquants:
        raise ErreurDonnees(f"{concept.id} : criteres manquants {manquants}")
    inconnus = sorted(set(concept.notes) - attendus)
    if inconnus:
        raise ErreurDonnees(f"{concept.id} : criteres inconnus {inconnus}")
    for nom, note in concept.notes.items():
        if not 0 <= note <= NOTE_MAX:
            raise ErreurDonnees(f"{concept.id} : note {nom}={note} hors de 0-{NOTE_MAX}")


def score(concept: Concept, criteres: list[Critere]) -> float:
    """Score sur 100 = points obtenus / points maximum possibles."""
    valider(concept, criteres)
    obtenus = sum(c.poids * concept.notes[c.nom] for c in criteres)
    maximum = sum(c.poids * NOTE_MAX for c in criteres)
    return round(100 * obtenus / maximum, 1)


def sous_score(concept: Concept, criteres: list[Critere], noms: list[str]) -> float:
    """Score sur 100 restreint a quelques criteres (ex. 'potentiel economique')."""
    retenus = [c for c in criteres if c.nom in noms]
    if not retenus:
        raise ErreurDonnees(f"aucun critere parmi {noms}")
    obtenus = sum(c.poids * concept.notes[c.nom] for c in retenus)
    maximum = sum(c.poids * NOTE_MAX for c in retenus)
    return round(100 * obtenus / maximum, 1)


# Deux axes lus separement dans les documents : ce qui RAPPORTE, et ce qui
# coute peu / se lance vite. Un concept peut etre riche mais impossible a
# lancer a 0 EUR par un debutant -- c'est exactement le piege a rendre visible.
AXE_VALEUR = [
    "valeur_commerciale",
    "revenu_recurrent",
    "affiliation",
    "produit_numerique",
    "revente_actif",
    "potentiel_audience",
]
AXE_FAISABILITE = [
    "facilite_production",
    "cout_faible",
    "automatisation",
    "levier_actif_existant",
    "concurrence_faible",
]


def classement(concepts: list[Concept], criteres: list[Critere]) -> list[tuple[Concept, float, float, float]]:
    lignes = [
        (c, score(c, criteres), sous_score(c, criteres, AXE_VALEUR), sous_score(c, criteres, AXE_FAISABILITE))
        for c in concepts
    ]
    return sorted(lignes, key=lambda ligne: ligne[1], reverse=True)


def rendu_markdown(lignes) -> str:
    sortie = [
        "| # | ID | Concept | Score global /100 | Potentiel eco /100 | Faisabilite /100 |",
        "|---|----|---------|------------------:|-------------------:|-----------------:|",
    ]
    for rang, (concept, global_, valeur, faisa) in enumerate(lignes, start=1):
        sortie.append(
            f"| {rang} | {concept.id} | {concept.nom} | **{global_}** | {valeur} | {faisa} |"
        )
    return "\n".join(sortie)


def rendu_csv(lignes) -> str:
    tampon = io.StringIO()
    plume = csv.writer(tampon)
    plume.writerow(["rang", "id", "concept", "cluster", "score_global", "potentiel_eco", "faisabilite"])
    for rang, (concept, global_, valeur, faisa) in enumerate(lignes, start=1):
        plume.writerow([rang, concept.id, concept.nom, concept.cluster, global_, valeur, faisa])
    return tampon.getvalue().strip()


def rendu_detail(concept: Concept, criteres: list[Critere]) -> str:
    sortie = [f"{concept.id} — {concept.nom}", "", "| Critere | Note /5 | Poids | Points |", "|---|--:|--:|--:|"]
    for critere in criteres:
        note = concept.notes[critere.nom]
        sortie.append(f"| {critere.nom} | {note} | {critere.poids} | {round(note * critere.poids, 2)} |")
    sortie += ["", f"Score global : {score(concept, criteres)}/100"]
    return "\n".join(sortie)


def main() -> None:
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument("--format", choices=["markdown", "csv"], default="markdown")
    analyseur.add_argument("--detail", help="ID d'un concept (ex. A2) pour voir le detail des points")
    arguments = analyseur.parse_args()

    criteres = charger_criteres()
    concepts = charger_concepts()

    if arguments.detail:
        cible = next((c for c in concepts if c.id.lower() == arguments.detail.lower()), None)
        if cible is None:
            raise SystemExit(f"concept inconnu : {arguments.detail}")
        print(rendu_detail(cible, criteres))
        return

    lignes = classement(concepts, criteres)
    print(rendu_csv(lignes) if arguments.format == "csv" else rendu_markdown(lignes))


if __name__ == "__main__":
    main()
