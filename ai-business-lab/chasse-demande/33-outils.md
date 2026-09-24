# Outils pour renforcer Claude Code sur ce projet

Tenu à jour par la routine (point 3 : une recherche d'outils par jour).
Règle : gratuit et sans compte → installé par Claude ; compte ou clé
nécessaire → préparé puis proposé à l'utilisateur ; payant → seulement
quand un revenu le justifie (budget 0 €).

| Outil | Usage pour nous | Coût | État |
|---|---|---|---|
| Gmail (connecteur, boîte du pseudonyme) | Contacter et suivre les éditeurs | gratuit | **actif** |
| OpenRush (connecteur) | Mesurer la demande (volumes de recherche Google) | gratuit (déjà connecté) | **actif** |
| Jev — TypeSafe AI (skill `.claude/skills/typesafe-ai`, outil `outils/jev_trier_reponses.py`) | Aiguilleur des réponses : catégories fermées, repli Claude puis humain | 5 $/mois offerts via Vercel AI Gateway | skill installé ; **clé à ajouter** (inscription TypeSafe fermée → Vercel) |
| Similarweb, Crunchbase | Trafic des sites, fermetures de startups | payants (Similarweb 338 €/mois) | écartés tant que rien ne rapporte |
| Stripe | Encaisser un produit vendu en direct | commission | inutile pour Atlassian (Atlassian encaisse) |
| Plugin « Small Business » (Anthropic, 44 skills) | Contrats, propositions, factures, trésorerie, impôts | gratuit | **installé** dans le projet (.claude/settings.json) le 24/09 |
| Higgsfield | Vidéos IA de démonstration d'un produit | freemium | **à activer quand on aura un produit à promouvoir** |
| Outils de développement Shopify pour Claude Code (vidéo AI LABS, 24/09) | Créer apps/thèmes Shopify | gratuit (à vérifier) | en réserve : seulement si une piste Shopify se confirme (aucune à ce jour, voir 07 et 19) |

## Sources envoyées par l'utilisateur (24/09, nuit) et suite donnée

| Vidéo (auteur) | Suite |
|---|---|
| Claude pour les petites entreprises, 44 skills (Tony Lotis) | plugin officiel « Small Business » proposé à l'installation |
| Jev will 10x your Claude Code ; résumés NotebookLM sur Jev | skill installé + aiguilleur ; clé via Vercel à ajouter |
| 12 New Rules for Prompting Opus 5.5 (RoboNuggets) | `.claude/CLAUDE.md` créé (contexte permanent) |
| 7 Free GitHub Repos That Make Claude So Good… (AI Edge) | **noms des dépôts à obtenir** (description de la vidéo), puis vérifier/installer |
| Shopify Claude Code workflow (AI LABS) | en réserve |
| JARVIS avec Claude Code (Thomas Berton) | écarté : déjà couvert (session cloud + routine) |
| Trading bots Jev/MCP (Miles Deutscher, Saleh) | écartés : secteur à risque (point 19) |
| 1 Person Business (Nate Herk), 9-5 en 90 jours (Shane Hummus), Opus 5.5 (Alex Finn), gagner de l'argent (Amadou Fall) | pas d'outil ; confirme l'organisation actuelle |
| Formation Claude Code gratuite (Ben BK, playlist) ; vidéo wEEi2bCuZGQ (inaccessible) | rien à installer |

## Vidéos : ce qui a pu être lu (24/09, nuit)

YouTube bloque la lecture des sous-titres depuis les serveurs cloud
(« RequestBlocked ») ; protection anti-robots respectée, pas de
contournement. Contenu retrouvé par recherche web quand c'est possible.

- « 7 Free GitHub Repos… » (AI Edge / Miles Deutscher) : liste partielle
  retrouvée (skool.com, recherche) : Last30Days, Playwright MCP, gstack,
  Agency Agents, Buzz ; souvent cités à côté : Superpowers,
  awesome-claude-code, Repomix.
  - **Superpowers** (obra) : **installé** pour le projet (méthode : plan,
    tests, relecture) — servira au portage Forge.
  - Playwright : déjà utilisé via nos outils (Chromium dans l'environnement).
  - Autres : non installés (pas d'usage pour nous à ce jour).
- Pour les autres vidéos : obtenir leur contenu via NotebookLM
  (l'utilisateur) → export dans Google Drive → lecture par le connecteur
  Google Drive.
