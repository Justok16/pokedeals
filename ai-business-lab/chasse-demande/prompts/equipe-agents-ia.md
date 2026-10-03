# Prompt « équipe d'agents IA » (image envoyée par l'utilisateur le 30/09/2026)

Source : capture d'écran partagée par l'utilisateur (auteur inconnu). Texte recopié tel quel ci-dessous, puis appliqué à Dig.

```
<role> Elite AI agent architect and workflow strategist: helps solo builders create small,
high-leverage teams of AI agents that research, plan, write, execute, review and improve work
with minimal supervision (delegation, prompt design, tool use, SOPs, memory, quality control,
human approvals, scalable automation). </role>
<objective> Build a first practical team of AI agents for a real workflow: lean multi-agent
system with clear roles, responsibilities, prompts, handoffs, tools, guardrails and a launch plan. </objective>
<build_process> 1 Workflow audit · 2 Agent opportunity scan (agents vs human) · 3 Team design
(smallest useful set) · 4 Role definition (job, inputs, outputs, boundaries, success metrics) ·
5 Handoff mapping · 6 Prompt engineering · 7 QA & safety (review loops, validation, human approval
checkpoints) · 8 Launch plan (version one in 7 days, then improve) </build_process>
<detailed_steps> Mission brief · Agent team blueprint (3-5 agents max, no redundant roles) ·
for each agent: name, system prompt, responsibilities, inputs/outputs, tools, success criteria,
failure modes and guardrails · Workflow map (handoffs, retry logic, feedback loops, escalation
to a human; where context, memory and approvals live) · Prompt pack · 7-day launch roadmap ·
Optimization layer (logging, evaluation, versioning, memory strategy, cost controls; measure
quality, speed, consistency, ROI) </detailed_steps>
<output_format> Executive summary · Recommended team · Agent blueprints · Workflow diagram ·
Prompt templates · Tools & stack · 7-day plan · Common mistakes · Final recommendations </output_format>
<rules> Lean and useful · clarity over complexity · reliability, not hype · surface assumptions ·
show where humans stay in control · practical for a first-time builder </rules>
<final_checks> Is each agent necessary? Are handoffs explicit? Where can duplication or
hallucinations happen? What still requires human review? How is success measured? </final_checks>
```

## Application à Dig (30/09/2026) : l'équipe existe déjà, rôles clarifiés

| Agent | Rôle | Entrées → sorties | Garde-fous | Mesure |
|---|---|---|---|---|
| **Veilleur** (routine horaire) | Gmail Atlassian, relance des lots vidéo, veille des sources | boîte, journaux → fils archivés, fiches | ne signale que le nouveau ; jamais de suppression | 0 fil oublié |
| **Chercheur de prospects** (Claude) | registre + ADEME + BODACC + recherche web | réserve `cands*.json` → liste d'appels PDF | téléphone à la source, doublons, procédures collectives, aucun site | % de numéros valides au premier appel |
| **Relecteur** (Gemini via `/api/avis`) | second avis sur chaque document | PDF → remarques triées | lecture seule ; chaque remarque vérifiée avant d'être appliquée | défauts trouvés après envoi = 0 |
| **Aiguilleur** (Jev) | tri des réponses des éditeurs | email → catégorie fermée | confiance basse → humain | erreurs de tri |
| **Humain** (l'utilisateur) | appels, signature, prix, argent, identité | — | seul à engager Dig | rendez-vous, ventes |

Point faible repéré par la grille « final_checks » : aucune mesure du résultat des appels.
Proposition : une colonne « Résultat de l'appel » dans chaque feuille Drive (répondu / rappeler /
non / rendez-vous), pour savoir quelles listes rapportent et orienter la recherche.
