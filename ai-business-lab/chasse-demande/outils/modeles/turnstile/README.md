# Anti-spam Turnstile pour le formulaire d'un site client (prêt le 03/11/2026)

Demande de l'utilisateur du 03/11 (« TOUT »). Cloudflare Turnstile bloque les robots sans faire cliquer sur des images.
Documentation officielle lue le 03/11/2026 : rendu côté navigateur (mise à jour du 17/06/2026), validation côté serveur
(22/10/2026), offres (14/08/2026) : **gratuit, jusqu'à 20 widgets par compte** (un widget peut couvrir plusieurs sites).

## Mise en place (premier formulaire d'un client)
1. **Compte Cloudflare du client** (règle du 05/10 : compte au nom de chaque client) : Turnstile → ajouter un widget pour
   son domaine → récupérer la clé publique (site key) et la clé secrète (secret key). La clé secrète va **seulement**
   dans les variables d'environnement du projet Cloudflare Pages (`TURNSTILE_SECRET`), jamais dans le dépôt.
2. Copier `formulaire.html` dans la page contact (remplacer `CLE_PUBLIQUE`) et `functions/api/contact.js` dans le
   projet Pages du client.
3. Script `api.js` chargé **depuis l'adresse officielle exacte** (la doc interdit de le copier ou de le mettre en cache).
4. Avant la mise en ligne : skills `vibe-security` / `security-review` (règle « nouveau code serveur »), test d'un
   envoi réel, `sh outils/unlighthouse/audit.sh` et `sh outils/liens/verifier.sh`.
5. Mentions légales et politique de confidentialité du client : citer Cloudflare Turnstile (service anti-robot).
