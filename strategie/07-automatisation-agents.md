# 07 — Automatisation et architecture d'agents

## Règle préalable

**On n'automatise jamais une tâche qu'on n'a pas faite à la main au moins cinq
fois.** Sinon on industrialise une erreur, et on perd plus de temps à corriger
l'automatisation qu'on n'en aurait perdu à faire la tâche.

Deuxième règle : une automatisation se juge sur **gain de temps × fiabilité ÷
risque**, jamais sur « c'est techniquement possible ». La plupart des projets
échouent en automatisant ce qui ne rapporte rien.

## Classement des tâches

### AUTOMATISABLE — exécution complète par machine, sans relecture

- Collecte des prix, stocks et précommandes (**déjà en production**).
- Calcul de la cote et de l'historique (**déjà en production**).
- Génération des pages du comparateur.
- Génération du brouillon de newsletter.
- Génération des scripts vidéo à partir des deals du jour.
- Collecte des métriques (plateformes, Search Console) et mise à jour du tableau.
- Exécution du Niche Radar.
- Surveillance de santé des workflows (**déjà en production** via le watchdog).

### SEMI-AUTOMATISABLE — machine propose, humain valide (2 à 15 min/jour)

- **Envoi de la newsletter** : relecture de 10 min avant expédition. Une erreur
  de prix envoyée à toute la liste ne se rattrape pas.
- **Publication des vidéos** : la machine prépare, l'humain publie. C'est la
  barrière principale contre le risque R2 (contenu jugé répétitif au niveau de
  la chaîne).
- **Alertes de précommande** : validation sur les produits à fort enjeu, envoi
  direct sur les cas déjà éprouvés.
- **Fiches du Niche Radar** : la machine rédige, l'humain arbitre.

### HUMAIN — jamais délégué

- **Les décisions KILL et SCALE.** Une machine qui décide seule d'arrêter ou
  d'amplifier optimise la métrique qu'on lui a donnée, pas la stratégie.
- **Les accords avec les boutiques** et toute relation commerciale.
- **La ligne éditoriale** et ce qu'on refuse de publier.
- **Les engagements juridiques et fiscaux.**
- **Le support client payant** (A3) — et c'est précisément pourquoi A3 ne doit
  pas grossir trop vite.

### À RISQUE — validation humaine systématique, sans exception

- Toute **affirmation chiffrée publiée** (une cote fausse détruit la confiance
  et l'actif : R9).
- Tout contenu contenant un **lien d'affiliation** (mention obligatoire : R5).
- Tout contenu utilisant des **visuels de cartes** (R3).
- Tout vocabulaire touchant au **placement ou au rendement** (R7).
- Toute **communication de crise** (erreur publiée, réclamation d'une boutique).

## Les 15 agents

Un agent n'est pas un logiciel séparé : c'est un **rôle**, avec une entrée, une
sortie et une fréquence. Certains sont déjà implémentés dans ce dépôt sous forme
de scripts, d'autres sont des prompts, d'autres encore restent humains.

| # | Agent | Entrée | Sortie | Fréquence | État |
|---|---|---|---|---|---|
| 1 | **Trend Hunter** | Sources publiques (`04`) | Signaux bruts | Hebdo | À écrire |
| 2 | **Market Analyst** | Signaux | Fiches d'opportunité notées | Hebdo | À écrire (réutilise `scorer.py`) |
| 3 | **Niche Manager** | Fiches + portefeuille actuel | Proposition de test | Hebdo | **Humain assisté** |
| 4 | **Content Strategist** | Données du jour + performances passées | Plan éditorial | Quotidien | À écrire |
| 5 | **Scriptwriter** | Plan + données réelles | Scripts | Quotidien | À écrire (prompt) |
| 6 | **Fact Checker** | Script + base de faits | Validation ou rejet | Quotidien | **À écrire en priorité** — c'est le garde-fou de R9 |
| 7 | **Creative Director** | Script | Hook, rythme, visuels | Quotidien | Prompt + humain |
| 8 | **Producer** | Script validé | Vidéo/page/numéro | Quotidien | Semi-auto |
| 9 | **Publisher** | Contenu prêt | Publication | Quotidien | **Humain** (barrière R2) |
| 10 | **Analytics** | Plateformes, Search Console | Tableau de bord | Quotidien | À écrire |
| 11 | **Optimizer** | Historique de performance | Recommandations de format | Hebdo | À écrire |
| 12 | **Monetization Manager** | Audience + clics sortants | Opportunités de revenu | Mensuel | À écrire |
| 13 | **Product Manager** | Retours d'audience | Problèmes validés | Mensuel | **Humain assisté** |
| 14 | **CFO** | Revenus, coûts, temps | Marge, revenu/heure, ROI | Mensuel | À écrire |
| 15 | **CEO** | Tout le tableau de bord | Décisions KILL/SCALE | Hebdo | **Humain, jamais délégué** |

Les prompts des agents 1, 2, 4, 5, 6, 11 et 14 sont dans
[`modeles/prompts-agents.md`](modeles/prompts-agents.md).

## Ordre d'implémentation (et pourquoi cet ordre)

1. **Analytics (10)** — sans mesure, tout le reste est aveugle.
2. **Fact Checker (6)** — sans lui, l'automatisation fabrique du risque.
3. **Content Strategist (4) + Scriptwriter (5)** — le gain de temps quotidien
   le plus important.
4. **Trend Hunter (1) + Market Analyst (2)** — le Niche Radar.
5. **Optimizer (11)** — n'a de sens qu'avec un historique de performance réel.
6. **CFO (14)** — dès le premier euro.
7. **Monetization (12), Product (13)** — quand une audience existe.

## Ce qu'il ne faut pas automatiser, même si c'est possible

- **La réponse aux commentaires.** C'est la seule source gratuite de
  compréhension de l'audience, et la seule façon d'entendre un problème avant
  qu'il devienne un produit. L'automatiser revient à débrancher l'oreille.
- **La sélection du contenu à publier.** Laisser une machine choisir maximise la
  quantité, ce qui est exactement le comportement sanctionné en 2026.
- **La décision d'arrêter un projet.** C'est l'acte stratégique le plus
  important du dispositif.

## Objectif réaliste de supervision

| Horizon | Temps humain quotidien | Ce qui l'occupe |
|---|---|---|
| Mois 1-3 | 4 h | Construction, tests, mesure |
| Mois 4-6 | 2 h | Validation, décisions, relation boutiques |
| Mois 7-12 | 1-2 h | Revue, arbitrages, développement des actifs gagnants |

La cible de 1-2 h/jour est atteignable **parce que** l'infrastructure de
collecte existe déjà. Elle ne le serait pas en partant de zéro.
