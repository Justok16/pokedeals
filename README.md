# 🎴 PokéDeals — Bot d'alerte Pokémon TCG

Bot 100% automatique, sans serveur ni base de données, qui surveille en continu **eBay France, Vinted, Leboncoin** et **83 boutiques françaises/japonaises spécialisées** (Shopify, PrestaShop, WooCommerce), et t'envoie une **notification Telegram** dès qu'il trouve quelque chose d'intéressant pour toi.

Il tourne **gratuitement sur GitHub Actions** : ton PC peut rester éteint, tout se passe dans le cloud, sur un planning automatique (le plus fréquent toutes les 15 minutes).

---

## 🧭 Les 3 choses qu'il fait pour toi

### 1. 🔥 Radar de bonnes affaires (historique)
Calcule une **cote** (le juste prix) pour chaque carte de ta liste à partir des annonces eBay réelles, l'affine avec Cardtrader/Cardmarket, puis compare chaque annonce eBay/Vinted/Leboncoin à cette cote. Alerte dès qu'une carte se vend nettement en dessous — avec le prix de revente conseillé et le profit net estimé.

### 2. 🔥📦 Radar boutiques spécialisées
Surveille 83 boutiques Shopify/PrestaShop/WooCommerce françaises et japonaises pour deux choses : une carte de ta liste en dessous de ton prix cible, ou le **retour en stock** d'une carte que tu attendais.

### 3. 🎉 Radar de précommandes
Détecte dès qu'un produit scellé précis que tu attends (ex. un coffret anniversaire) apparaît en précommande sur une de ces boutiques, avant même sa sortie officielle.

*(Deux fonctions annexes tournent aussi en tâche de fond : un suivi de tendance de prix long terme sur quelques cartes japonaises choisies à la main, et un "prix le plus bas du jour" envoyé chaque matin sur 4 cartes suivies dans plusieurs langues — moins prioritaires, mais utiles pour savoir si c'est le bon moment d'acheter.)*

---

## 📲 Ce que tu reçois sur Telegram

| Icône | Signification |
|---|---|
| 🔥 | Bonne affaire détectée (historique ou boutique) : au moins 30% sous la cote, carte neuve/near mint, non gradée |
| 📦 | Une carte suivie est revenue en stock chez une boutique |
| 🎉 | Un produit scellé attendu vient d'apparaître en précommande |
| 💰 | Une carte de ton stock (`mes_achats`) a atteint 2× ton prix d'achat — c'est le moment de vendre |
| 📊 | Récap quotidien à 21h : scans du jour, deals détectés, profit potentiel |
| ⚠️ / 🚀 | Une cote s'effondre (prudence, contrefaçons ?) ou explose (carte devenue recherchée) |
| 🗓️ | Une cote fixée à la main il y a plus de 30 jours mérite d'être revérifiée |

⚠️ **Vérifie toujours les photos avant d'acheter** : le bot lit le texte des annonces, pas les images (sauf activation optionnelle de la vérification photo par IA, cf. secrets ci-dessous).

---

## 🚀 Installation (une seule fois)

### Étape 1 — Récupérer le code
Ce dépôt GitHub contient déjà tout le programme (une trentaine de fichiers Python + les planificateurs). Le plus simple : **fork** ce dépôt sur ton propre compte GitHub (bouton **Fork** en haut de la page), ou clone-le puis pousse-le sur un nouveau dépôt à toi. Garde-le **public** (⚠️ les dépôts publics ont des minutes GitHub Actions illimitées et gratuites ; tes secrets restent invisibles, stockés à part).

### Étape 2 — Récupérer tes clés eBay
1. [developer.ebay.com](https://developer.ebay.com) → **Your Account → Application Keys**.
2. Section **Production** (pas Sandbox !) : note l'**App ID (Client ID)** et le **Cert ID (Client Secret)**.

### Étape 3 — Récupérer ton token Cardtrader
1. Crée un compte sur [cardtrader.com](https://www.cardtrader.com), puis génère un token API dans les paramètres de ton compte.

### Étape 4 — Configurer Telegram
1. Dans Telegram, ouvre **@BotFather** → `/mybots` → ton bot → **API Token** → copie la chaîne complète (format `1245330032:AAH4x...`).
2. **Très important** : ouvre une discussion avec **ton bot** et envoie-lui `/start` (sinon Telegram lui interdit de t'écrire).
3. Ton `chat_id` doit être renseigné dans `config.yaml`.

### Étape 5 — Enregistrer les secrets dans GitHub
**Settings → Secrets and variables → Actions → New repository secret** (noms exacts, sans espace) :

| Nom du secret | Obligatoire ? | Valeur |
|---|---|---|
| `EBAY_CLIENT_ID` | oui | ton App ID eBay |
| `EBAY_CLIENT_SECRET` | oui | ton Cert ID eBay |
| `TELEGRAM_BOT_TOKEN` | oui | le token complet donné par @BotFather |
| `CARDTRADER_TOKEN` | oui | ton token Cardtrader |
| `GMAIL_APP_PASSWORD` | optionnel | active les alertes Leboncoin par email (mot de passe d'application créé sur myaccount.google.com/apppasswords) |
| `ANTHROPIC_API_KEY` | optionnel | active la vérification par IA que la photo d'une annonce montre bien le bon Pokémon avant d'alerter |
| `POKEMONPRICETRACKER_API_KEY` | optionnel | active le suivi de tendance de prix long terme sur les cartes japonaises/coréennes suivies |

### Étape 6 — Lancer !
1. Onglet **Actions** → active les workflows si demandé (bouton vert en haut).
2. Choisis **PokéDeals** dans la liste à gauche → **Run workflow** → **Run workflow**.
3. Rond vert ✅ après quelques minutes = le bot tournera ensuite **tout seul, pour toujours**, sur son planning automatique.

Les autres planificateurs (scan des boutiques, radar de précommandes...) démarrent d'eux-mêmes selon leur propre planning — rien de plus à faire.

---

## ⚙️ Personnaliser : uniquement `config.yaml`

Le seul fichier que tu modifieras (crayon ✏️ sur GitHub) :

- **Ajouter/retirer des cartes** dans `watchlist` — chaque carte a un nom, un numéro de collection (obligatoire), une langue, et éventuellement un alias.
- **Déclarer un achat** dans `mes_achats` pour activer l'alerte de revente :
  ```yaml
  mes_achats:
    - nom: "Méga-Gardevoir ex 187/132"
      langue: fr
      prix_achat: 120
  ```
  (Quand tu as vendu, supprime la carte de la liste.)
- **Cote manuelle** pour une carte peu présente sur eBay : ajoute `cote: 180` et `cote_date: "2026-08-17"` sous la carte (un rappel Telegram te prévient au bout de 30 jours de la revérifier).
- **Régler les seuils** dans `regles` : `marge_achat` (part sous la cote pour déclencher une alerte), `multiplicateur_revente`, `frais_port_max`, `cote_min`, etc. — les valeurs actuelles dans `config.yaml` font foi, ce README ne les duplique pas pour éviter qu'elles se désynchronisent.

---

## ❓ Questions fréquentes

**Pourquoi pas Cardmarket pour la cote ?** Son API est réservée aux professionnels et son site interdit le scraping quotidien. La cote est calculée depuis eBay (médiane des annonces pertinentes, nettoyée des valeurs extrêmes, lissée sur plusieurs jours), puis affinée par Cardtrader quand disponible, avec un repli sur le guide de prix public Cardmarket via l'API TCGdex.

**Leboncoin ne remonte rien ?** Sa protection anti-robot bloque souvent les requêtes directes. Le bot bascule alors sur les alertes email Leboncoin (si `GMAIL_APP_PASSWORD` est configuré) et réessaie la recherche directe au tour suivant. C'est prévu et surveillé (une alerte Telegram te prévient si le blocage devient anormalement fréquent, signe d'un vrai problème plutôt que d'un aléa).

**Combien ça coûte ?** 0€. Dépôt public = minutes GitHub Actions illimitées, API eBay/Cardtrader/TCGdex gratuites, Telegram gratuit. Seul `ANTHROPIC_API_KEY` (optionnel) a un coût, minime, si tu l'actives.

**Comment arrêter un planificateur ?** Onglet **Actions** → choisis le workflow dans la liste à gauche → `⋯` → **Disable workflow**.

**Une erreur ❌ dans Actions ?** Clique sur le run en échec → l'étape en rouge → copie le message d'erreur et transmets-le à Claude Code.

**Je veux comprendre comment le code est organisé.** `CLAUDE.md` est la référence technique complète (architecture, chaque fichier, pièges déjà rencontrés) — pensée pour que Claude Code s'y retrouve, mais utile aussi si tu veux creuser toi-même.
