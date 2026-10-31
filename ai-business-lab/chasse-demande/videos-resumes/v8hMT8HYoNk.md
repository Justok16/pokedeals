# v8hMT8HYoNk : « Claude + VPS + Doppler : le setup que j'aurais dû connaître bien plus tôt » (Shubham Sharma)

Envoyée par l'utilisateur le 31/10/2026. Transcription vidIQ (le relais Gemini était à court de quota), durée environ 15 min.
Vidéo sponsorisée par Hostinger (code promo, offres Black Friday).

## Idée principale
Un VPS est un ordinateur loué, allumé en permanence. Autrefois il fallait des connaissances d'administrateur
système (SSH, Docker, pare-feu). Désormais, on branche Claude Code au compte de l'hébergeur (plugin ou MCP
Hostinger) et Claude installe, sécurise et surveille tout seul : logiciels libres, applications, DNS, HTTPS,
pare-feu, alertes quand un service tombe.

## Outils cités (noms exacts, rôle)
- **Hostinger** (VPS KVM 2, 8 Go de RAM, nom de domaine offert) et son **plugin/MCP** pour Claude Code : payants.
- **Coolify** et **Dokploy** : interfaces pour installer des logiciels ou déployer des applications sur un VPS. L'auteur les a abandonnées au profit de Claude.
- **Umami** : statistiques de visite d'un site, sans Google Analytics.
- **Dub** : suivi des clics sur des liens, par exemple ceux d'un aimant à prospects.
- **Excalidash** : version libre et installable d'Excalidraw (schémas).
- **DocuSeal** : signature électronique libre, équivalent de DocuSign.
- **Cal.com** : page de prise de rendez-vous ; l'auteur affirme que la version payante coûte 16 $/mois.
- **Hermes** : agent qui tourne en continu sur un VPS.
- **Doppler** : coffre-fort de clés API, « le 1Password des clés ». L'auteur pense qu'il est gratuit jusqu'à 10 ou 40 clés, sans en être sûr.
- **Ubuntu** (système), **fail2ban**, **Docker Compose**, clé SSH obligatoire : la sécurisation que Claude propose d'office.

## Méthode montrée
1. Louer un VPS avec seulement Ubuntu installé.
2. Dans Claude Code, créer un environnement « VPS » et installer le plugin Hostinger.
3. Autoriser la connexion MCP et demander « liste-moi mes serveurs ».
4. Claude sécurise le serveur : connexion par mot de passe coupée, pare-feu, fail2ban, Docker.
5. Claude installe Cal.com sur un sous-domaine en ajoutant lui-même le DNS chez Cloudflare.
6. Les clés sont rangées dans Doppler, pour qu'aucune ne traîne sur l'ordinateur.

## Tri DIG16 (31/10)
| Idée | Décision | Raison |
|---|---|---|
| Louer un VPS géré par Claude | **Écartée** | Payant (budget 0 €). Le site dig16.fr et les sites clients sont hébergés gratuitement sur Cloudflare Pages, et le relais tourne gratuitement sur Vercel. Déjà tranché pour TuiF6yIeLG4, 5nkJKNQAi8I et e2JSCYig10g. |
| Code promo et Black Friday Hostinger | **Écartée** | Lien sponsorisé ; aucun achat. |
| Umami | **Réserve** | Le site a déjà Cloudflare Web Analytics, gratuit et sans cookie. À ressortir si un client veut des statistiques plus fines. Il faut un hébergement ou l'offre cloud (gratuité à revérifier). |
| Dub (suivi des liens) | **Réserve** | Utile pour mesurer les clics des publications et des mails. Gratuité à revérifier sur la page officielle le jour où il sert. |
| Excalidash | **Réserve** | Le connecteur Excalidraw est déjà disponible dans les outils de Claude. Pas besoin d'installer quoi que ce soit. |
| DocuSeal | **Déjà en place** | Utilisé pour les signatures du kit client (skill `nouveau-client`). |
| Cal.com | **Déjà en réserve** | Lignes existantes de `reserve-prete.md` (rendez-vous en ligne). |
| Doppler (coffre à clés) | **Réserve** | Nos clés sont déjà en variables d'environnement, jamais dans le dépôt. À ressortir si les clés se multiplient ou si un client a besoin de clés partagées. Offre gratuite à lire sur la page officielle avant tout usage. |
| Sécuriser d'office tout serveur (clé SSH, pare-feu, fail2ban) | **Noté** | Principe repris si un jour un serveur est loué (après le premier client payant et sur décision de l'utilisateur). |
