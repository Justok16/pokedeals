# REPRISE — état d'avancement

> **Ce fichier est le point d'entrée après toute interruption** (fin de tokens,
> coupure, session en veille, conteneur recyclé). Consigne permanente de
> l'utilisateur : **reprendre le travail dès que possible, sans attendre qu'il
> relance.**
>
> Il est versionné, donc il survit à la mort du conteneur — contrairement à
> tout ce qui n'est que dans `/home/user`.
>
> **Dernière mise à jour : 21/09/2026**

---

## Où en est le projet

**Projet** : AI Business Lab — construire à partir de zéro, à budget nul, un
portefeuille de business numériques automatisés par IA sur le marché
francophone. **Aucun lien avec PokéDeals**, qui n'héberge ce dossier que
temporairement.

**Verticale retenue** : les **e-commerçants français** (décision du 21/09/2026,
sur le critère posé par l'utilisateur : revenu maximal, marché stable ou
porteur). Les artisans du bâtiment ont été écartés — marché en recul.

**Forme retenue** : A4 (newsletter de veille) + B2 (comparateur d'outils)
+ D1 (contenus courts, test jetable), monétisés par **affiliation récurrente**.

---

## Ce qui est fait

- [x] Étude de marché datée et sourcée (`01-etude-marche.md`)
- [x] Portefeuille de 15 concepts noté et classé (`02-portefeuille-concepts.md`)
- [x] Contre-épreuve sous grille « revenu maximal » (`outils/criteres-max-revenu.yaml`)
- [x] Plan d'exécution et plan des 90 jours (`03-plan-execution.md`)
- [x] Niche Radar, tableau de bord, monétisation/risques, agents, roadmap, budget (`04` à `09`)
- [x] Modèles réutilisables (`modeles/`)
- [x] Moteur de classement + 10 tests, vert en CI (`outils/`)
- [x] Kit de lancement de la verticale (`lancement/`)
- [x] Les 4 premiers numéros rédigés intégralement (`lancement/numeros/`)
- [x] Comparateur : 12 pages rédigées — méthodologie, page pilier, fiches plateformes, comparatifs, protocole IA, pages obligations (`lancement/comparateur/`)
- [x] Journal des vérifications réglementaires ouvert (`lancement/verifications.md`)
- [x] Arborescence autonome préparée (`.gitignore`, `.github/workflows/tests.yml`, chemins racine)

---

## EN COURS — sortir le projet dans son propre dépôt

**Bloqué sur une action de l'utilisateur.** L'application GitHub de la session
**ne peut pas créer de dépôt** (`403 Resource not accessible by integration`).

### Ce que l'utilisateur doit faire (une seule fois)

Créer sur github.com un dépôt **vide** nommé **`ai-business-lab`** — sans
README, sans `.gitignore`, sans licence (sinon la première poussée est refusée).
Visibilité privée de préférence.

### Ce qu'il faut faire dès que ce dépôt existe (sans rien redemander)

1. `list_repos` → confirmer que `Justok16/ai-business-lab` apparaît.
2. `add_repo` avec `access: "push"`.
3. Reconstruire l'arborescence autonome (voir `MIGRATION.md`, tout y est), puis
   pousser sur `main`.
4. Vérifier que la CI du nouveau dépôt passe (job `scoring` → 10 tests).
5. **Seulement après une poussée réussie**, nettoyer `pokedeals` :
   - supprimer `ai-business-lab/` ;
   - retirer le job `scoring_strategie` de `.github/workflows/tests.yml` ;
   - retirer la section `ai-business-lab/` du `README.md` racine et la ligne
     correspondante dans l'arborescence ;
   - pousser sur `claude/ai-business-portfolio-strategy-96yf4g`.
6. Fermer la **PR #118** avec un commentaire renvoyant vers le nouveau dépôt.

**Règle de sécurité** : ne jamais supprimer `ai-business-lab/` de `pokedeals`
tant que le contenu n'a pas été poussé ailleurs **avec succès**. Tant que le
nouveau dépôt n'existe pas, cette branche est le **seul endroit durable** où ce
travail existe.

---

## À FAIRE ensuite (ne dépend de personne)

- [x] ~~Rédiger les 4 premiers numéros de la newsletter en entier~~ — fait le
      21/09/2026, dans `lancement/numeros/`. Prêts à envoyer **après levée des
      marqueurs `[VÉRIFIER]`** sur source officielle.
- [x] ~~Rédiger les premières pages du comparateur~~ — fait le 21/09/2026, dans
      `lancement/comparateur/` : méthodologie publiée, page pilier chiffrée
      (le calcul complet du coût réel d'une boutique), 3 fiches plateformes,
      et plan détaillé des 6 pages restantes.
- [x] ~~Rédiger les pages restantes du comparateur~~ — fait le 21/09/2026.
      Douze pages au total dans `lancement/comparateur/`.
- [ ] **Prochaine tâche par défaut** : exécuter le protocole de test des outils
      d'IA (`lancement/comparateur/05-outils-ia-protocole.md`) — c'est la seule
      page qui ne peut pas être écrite sans essayer réellement les outils, et
      c'est la plus difficile à copier pour un concurrent.
- [ ] Ouvrir manuellement les textes sur Légifrance et EUR-Lex (bloqués depuis
      cet environnement) pour clore les `[À CONFIRMER]` restants.
- [~] Vérifier chaque fait réglementaire sur sa **source officielle** (règle R3).
      **Commencé le 21/09/2026**, journal dans `lancement/verifications.md` :
      rétractation en ligne, TVA OSS/IOSS et calendrier de facturation
      électronique **vérifiés** ; DSA **partiellement** — la qualification d'une
      boutique affichant des avis n'a pas pu être établie, le numéro 3 a donc
      été réécrit pour n'affirmer aucune obligation. Légifrance et EUR-Lex sont
      **bloqués par le proxy réseau** de cet environnement : ces textes-là
      doivent être ouverts manuellement avant publication.

---

## Décisions déjà prises — ne pas rouvrir sans raison nouvelle

| Décision | Motif |
|---|---|
| Projet indépendant de PokéDeals | Consigne explicite de l'utilisateur |
| Audience professionnelle, pas grand public | RPM FR 5-12 € en B2B contre 0,50-2,50 $ sur les formats faceless saturés |
| E-commerçants FR | Seule verticale testée qui combine marché en croissance (+7 %) et affiliation récurrente (Shopify 20 % sur 4 ans) |
| Artisans du bâtiment écartés | Marché en recul : 13 trimestres de baisse |
| Chaîne faceless divertissement écartée | Dernière du classement, y compris sous la grille « revenu maximal » |
| Angle « outils, vrais prix, obligations » | Le créneau e-commerce est saturé de vendeurs de méthodes ; c'est le seul angle défendable |
| Aucune promesse de revenus | Différenciation **et** protection juridique |

---

## Blocages connus

| Blocage | Nature | Levée |
|---|---|---|
| Création de dépôt GitHub | Droit manquant de l'app (403) | Action utilisateur, ci-dessus |
| Faits réglementaires en niveau 2/3 | Méthode | Vérification sur source officielle avant publication |

---

## Suivi automatique en place

- **Routine horaire** `Reprise automatique — AI Business Lab`
  (`trig_01NJayY6F8bQrnofRiia7i1i`) : réveille cette session toutes les heures,
  lit ce fichier, reprend ce qui peut l'être, et **reste silencieuse** si tout
  est bloqué côté utilisateur.
- **Abonnement aux événements de la PR #118** : CI et commentaires de revue.
