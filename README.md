# 🎴 PokéDeals — Bot d'arbitrage de cartes Pokémon

Bot 100% automatique qui surveille **eBay France, Vinted et Leboncoin**, calcule la cote de chaque carte, et t'envoie une **notification Telegram** dès qu'une carte de la **série 151** ou du **bloc Méga Évolution** est vendue **au moins 30% net sous la cote** (port ≤ 6€, cartes neuves/near mint uniquement, non gradées, cote minimum 5€).

Il tourne **gratuitement sur GitHub Actions** : ton PC peut rester éteint. Il scanne **toutes les 15 minutes**, avec des pauses aléatoires et une IP différente à chaque passage pour ne pas se faire bannir.

**✨ Version fichier unique** : TOUT le programme est dans `main.py`. Le dépôt ne contient que 5 fichiers, et le seul que tu modifieras un jour est `config.yaml`.

```
pokedeals/
├── main.py                          ← le programme (ne jamais modifier)
├── config.yaml                      ← TES réglages (cartes, seuils, stock...)
├── requirements.txt                 ← 2 lignes techniques (ne jamais modifier)
├── data/seen.json                   ← mémoire du bot (se remplit tout seul)
└── .github/workflows/pokedeals.yml  ← le planificateur (ne jamais modifier)
```

---

## 🚀 Installation (une seule fois, ~20 minutes)

### Étape 1 — Créer le dépôt GitHub
1. Va sur [github.com](https://github.com) et connecte-toi.
2. Clique sur **New repository** (bouton vert).
3. Nom : `pokedeals` → coche **Public** (⚠️ important : les dépôts publics ont des minutes GitHub Actions **illimitées et gratuites** ; tes mots de passe ne seront PAS visibles, ils sont stockés à part).
4. Clique **Create repository**.

### Étape 2 — Uploader les fichiers
1. Sur la page du dépôt, clique **uploading an existing file**.
2. Depuis le dossier dézippé, glisse-dépose : **`main.py`**, **`config.yaml`**, **`requirements.txt`** et le dossier **`data`**.
3. **Commit changes**.

### Étape 3 — Créer le planificateur (le dossier caché .github passe mal en glisser-déposer, on le crée à la main)
1. **Add file → Create new file**.
2. Dans le champ du nom, tape exactement : `.github/workflows/pokedeals.yml`
3. Ouvre le fichier `.github/workflows/pokedeals.yml` du ZIP avec le Bloc-notes, copie TOUT, colle-le dans l'éditeur GitHub.
4. **Commit changes**. → L'onglet **Actions** apparaît avec le workflow **PokéDeals**.

### Étape 4 — Récupérer tes clés eBay
1. [developer.ebay.com](https://developer.ebay.com) → **Your Account → Application Keys**.
2. Section **Production** (pas Sandbox !) : note l'**App ID (Client ID)** et le **Cert ID (Client Secret)**.

### Étape 5 — Configurer Telegram
1. Dans Telegram, ouvre **@BotFather** → `/mybots` → ton bot → **API Token** → copie la chaîne complète (format `1245330032:AAH4x...`).
2. **Très important** : ouvre une discussion avec **ton bot** et envoie-lui `/start` (sinon Telegram lui interdit de t'écrire).
3. Ton `chat_id` (`1245330032`) est déjà renseigné dans `config.yaml`.

### Étape 6 — Enregistrer les 3 secrets dans GitHub
**Settings → Secrets and variables → Actions → New repository secret** (noms exacts, sans espace) :

| Nom du secret | Valeur |
|---|---|
| `EBAY_CLIENT_ID` | ton App ID eBay |
| `EBAY_CLIENT_SECRET` | ton Cert ID eBay |
| `TELEGRAM_BOT_TOKEN` | le token complet donné par @BotFather |

> 💡 L'email est désactivé dans ta config. Pour le réactiver un jour : mets `email: true` dans `config.yaml` et ajoute un 4ᵉ secret `GMAIL_APP_PASSWORD` (mot de passe d'application créé sur myaccount.google.com/apppasswords).

### Étape 7 — Lancer !
1. Onglet **Actions** → active les workflows si demandé.
2. **PokéDeals** → **Run workflow** → **Run workflow**.
3. Rond vert ✅ après 2-3 minutes = le bot tournera ensuite **tout seul toutes les 15 minutes, pour toujours**.

---

## 📲 Ce que tu recevras sur Telegram

**🔥 Alerte ACHAT** — dès qu'une nouvelle annonce passe TOUS les filtres : bonne carte (nom + numéro vérifiés), vraie carte à l'unité (pas de vêtement, jouet, lot, produit scellé, carte gradée ou contrefaçon), état neuf/near mint, port ≤ 6€, et prix total à au moins -30% de la cote. Avec prix de revente conseillé et profit net estimé (frais ~13% déduits).

**💰 Alerte VENTE** — quand la cote d'une carte de ton stock (`mes_achats`) atteint **2× ton prix d'achat**. Rappel hebdomadaire tant que c'est vrai.

**📊 Récap quotidien à 21h** — scans du jour, deals détectés, profit potentiel, progression de ton stock vers l'objectif ×2.

**⚠️🚀 Anomalies** — cote qui s'effondre (-30% : prudence, contrefaçons ?) ou qui explose (+50% : carte devenue recherchée).

⚠️ **Vérifie toujours les photos avant d'acheter** : le bot lit le texte des annonces, pas les images.

---

## ⚙️ Personnaliser : uniquement `config.yaml` (crayon ✏️ sur GitHub)

- **Ajouter/retirer des cartes** dans `watchlist` (ME05 Nuit Noire est prête en commentaire : enlève les `# ` après le 17 juillet 2026).
- **Déclarer un achat** dans `mes_achats` pour activer l'alerte de revente :
  ```yaml
  mes_achats:
    - nom: "Méga-Gardevoir ex 187/132"
      langue: fr
      prix_achat: 120
  ```
  (Quand tu as vendu, supprime la carte de la liste.)
- **Cote manuelle** pour les cartes japonaises peu présentes sur eBay FR : ajoute `cote: 180` sous la carte.
- **Régler les seuils** dans `regles` : `marge_achat` (0.30 = -30%), `multiplicateur_revente` (2.0 = ×2), `frais_port_max`, `cote_min`, etc.

---

## ❓ Questions fréquentes

**Pourquoi pas Cardmarket pour la cote ?** Son API est réservée aux professionnels et son site bloque les robots. La cote est calculée depuis eBay : médiane des annonces actives, nettoyée des valeurs extrêmes, corrigée de -8%, puis **lissée** sur les 5 derniers passages (insensible aux annonces farfelues).

**Leboncoin ne remonte rien ?** Sa protection anti-robot bloque souvent les serveurs. Le bot continue avec eBay et Vinted et réessaie au tour suivant. C'est prévu.

**Combien ça coûte ?** 0€. Dépôt public = minutes illimitées, API eBay gratuite, Telegram gratuit.

**Comment l'arrêter ?** Actions → PokéDeals → `⋯` → **Disable workflow**.

**Une erreur ❌ dans Actions ?** Clique sur le run → **scan** → l'étape en rouge → copie le message d'erreur et transmets-le à Claude.
