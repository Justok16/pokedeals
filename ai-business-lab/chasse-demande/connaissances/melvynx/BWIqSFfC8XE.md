# Fait plus d'argent avec les e-mails (setup complet avec Codex ou Claude Code)

Vidéo : https://youtu.be/BWIqSFfC8XE · durée 19:20 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé demandé, basé strictement sur la vidéo :

### 1) Idée principale
L'auteur explique que l'e-mail marketing reste le canal le plus efficace et prévisible pour transformer une audience en revenus (notamment pour les SaaS et les formations). Il montre comment automatiser et configurer entièrement l'e-mail marketing d'un SaaS en moins de 20 minutes en combinant l'outil **Lumail** et un agent IA (**Claude Code**).

---

### 2) Outils, sites et dépôts GitHub cités
* **Lumail** (`lumail.io`) : 
  * **Prix :** Offre gratuite disponible (comportant un nombre illimité d'abonnés, 3 000 e-mails gratuits, 1 domaine web et des workflows illimités) ; des forfaits payants existent (Creator à 20 $, Pro à 60 $, Business à 200 $).
  * **Rôle :** Plateforme d'e-mail marketing automatisé propulsée par IA (gestion des abonnés, campagnes, workflows, e-mails transactionnels, intégrations CLI).
* **SpyLand.ing** (`spyland.ing`) : 
  * **Prix :** Non précisé (présenté comme un projet SaaS personnel de l'auteur).
  * **Rôle :** SaaS personnel de l'auteur qui analyse et surveille les modifications de landing pages et de prix des concurrents.
* **Cloudflare** : 
  * **Prix :** Non précisé.
  * **Rôle :** Gestionnaire de domaine et de DNS (utilisé avec un agent IA pour configurer automatiquement les enregistrements DNS de Lumail).
* **Claude Code** (via OpenAI Codex/CLI/skills) : 
  * **Prix :** Non précisé.
  * **Rôle :** Agent IA utilisé dans le terminal pour automatiser la configuration et la connexion entre le code source du SaaS et Lumail.

---

### 3) Astuces concrètes et réutilisables
* **Utilisation d'un sous-domaine d'e-mail :** Pour protéger la réputation de votre domaine principal lors de l'envoi d'e-mails (ex : utiliser `hey.spyland.ing` au lieu de `spyland.ing`), afin d'éviter d'endommager votre marque en cas de mauvaise manipulation.
* **Automatisation par l'agent IA :** Utiliser les commandes CLI et les skills de Claude Code pour configurer automatiquement les enregistrements DNS (Cloudflare) et lier l'API de Lumail sans avoir à tout paramétrer manuellement.
* **Segmentation et workflows basés sur les tags :** 
  * Mettre en place un workflow d'onboarding (ex: `Signup onboarding`) qui vérifie si l'utilisateur a effectué une action clé (comme l'ajout d'une page surveillée).
  * Utiliser des tags (ex: `spyland-activated`, `spyland-free`, `spyland-upgrade`) pour automatiser l'envoi d'e-mails ciblés en fonction du comportement exact de l'utilisateur (relances s'il n'est pas actif, passage à un workflow de type *freemium* ou *free trial*).
* **Automatisation des e-mails transactionnels :** Connecter les codes de vérification OTP de connexion pour qu'ils soient envoyés automatiquement et proprement via Lumail.

---

### 4) Chiffres de revenus annoncés
* **Revenus de l'auteur grâce à l'e-mail marketing :** 100 % de son revenu (affirmé par l'auteur).
* **Ancienneté de son business en ligne :** Plus de 4 ans (affirmé par l'auteur).
* **Volume gratuit sur Lumail :** 3 000 e-mails par mois et abonnés illimités pour 0 $ (affirmé par l'auteur).
