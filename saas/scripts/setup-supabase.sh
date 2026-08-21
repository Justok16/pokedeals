#!/usr/bin/env bash
# Provisionne le projet Supabase de PokéDeals via l'API de gestion Supabase,
# applique le schema (supabase/migrations/), et ecrit .env.local.
#
# A LANCER EN LOCAL (pas depuis un environnement distant dont le reseau est
# restreint -- api.supabase.com doit etre joignable).
#
# Prerequis :
#   export SUPABASE_ACCESS_TOKEN=sbp_xxxxx   (Personal Access Token, cf.
#     https://supabase.com/dashboard/account/tokens)
#
# Usage : ./scripts/setup-supabase.sh [nom-du-projet] [region]
#   region par defaut : eu-west-3 (Paris)

set -euo pipefail

if [ -z "${SUPABASE_ACCESS_TOKEN:-}" ]; then
  echo "Erreur : la variable SUPABASE_ACCESS_TOKEN n'est pas definie." >&2
  echo "Cree un jeton sur https://supabase.com/dashboard/account/tokens" >&2
  exit 1
fi

PROJECT_NAME="${1:-pokedeals}"
REGION="${2:-eu-west-3}"
API="https://api.supabase.com/v1"
AUTH_HEADER="Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATIONS_DIR="${SCRIPT_DIR}/../supabase/migrations"
ENV_FILE="${SCRIPT_DIR}/../.env.local"

if ! command -v jq >/dev/null 2>&1; then
  echo "Erreur : jq est requis (brew install jq / apt install jq)." >&2
  exit 1
fi

echo "==> Récupération de l'organisation Supabase..."
ORG_ID=$(curl -sS -H "$AUTH_HEADER" "$API/organizations" | jq -r '.[0].id')
if [ -z "$ORG_ID" ] || [ "$ORG_ID" = "null" ]; then
  echo "Erreur : aucune organisation trouvée sur ce compte Supabase." >&2
  exit 1
fi
echo "    organisation : $ORG_ID"

echo "==> Création du projet '$PROJECT_NAME' (région $REGION)..."
DB_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=' | head -c 32)
CREATE_RESPONSE=$(curl -sS -X POST "$API/projects" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "{\"name\":\"$PROJECT_NAME\",\"organization_id\":\"$ORG_ID\",\"region\":\"$REGION\",\"db_pass\":\"$DB_PASSWORD\",\"plan\":\"free\"}")

PROJECT_REF=$(echo "$CREATE_RESPONSE" | jq -r '.id')
if [ -z "$PROJECT_REF" ] || [ "$PROJECT_REF" = "null" ]; then
  echo "Erreur lors de la création du projet :" >&2
  echo "$CREATE_RESPONSE" | jq . >&2
  exit 1
fi
echo "    projet créé : $PROJECT_REF"
echo "    mot de passe DB (à conserver si besoin d'accès direct psql) : $DB_PASSWORD"

echo "==> Attente de la disponibilité du projet (peut prendre 1-2 min)..."
for i in $(seq 1 60); do
  STATUS=$(curl -sS -H "$AUTH_HEADER" "$API/projects/$PROJECT_REF" | jq -r '.status')
  if [ "$STATUS" = "ACTIVE_HEALTHY" ]; then
    echo "    projet prêt."
    break
  fi
  echo "    statut actuel : $STATUS (tentative $i/60)"
  sleep 5
done

if [ "$STATUS" != "ACTIVE_HEALTHY" ]; then
  echo "Erreur : le projet n'est pas devenu ACTIVE_HEALTHY à temps." >&2
  exit 1
fi

for MIGRATION_FILE in "$MIGRATIONS_DIR"/*.sql; do
  echo "==> Application de la migration ($(basename "$MIGRATION_FILE"))..."
  SQL_ESCAPED=$(jq -Rs . < "$MIGRATION_FILE")
  QUERY_RESPONSE=$(curl -sS -X POST "$API/projects/$PROJECT_REF/database/query" \
    -H "$AUTH_HEADER" -H "Content-Type: application/json" \
    -d "{\"query\": $SQL_ESCAPED}")

  if echo "$QUERY_RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
    echo "Erreur lors de l'application de $(basename "$MIGRATION_FILE") :" >&2
    echo "$QUERY_RESPONSE" | jq . >&2
    exit 1
  fi
  echo "    OK."
done

echo "==> Récupération des clés API..."
API_KEYS=$(curl -sS -H "$AUTH_HEADER" "$API/projects/$PROJECT_REF/api-keys")
ANON_KEY=$(echo "$API_KEYS" | jq -r '.[] | select(.name == "anon") | .api_key')
SERVICE_ROLE_KEY=$(echo "$API_KEYS" | jq -r '.[] | select(.name == "service_role") | .api_key')

cat > "$ENV_FILE" <<EOF
NEXT_PUBLIC_SUPABASE_URL=https://${PROJECT_REF}.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=${ANON_KEY}
EOF

echo ""
echo "==> Terminé. Écrit dans $ENV_FILE"
echo ""
echo "Prochaine étape (manuelle, ne peut pas être automatisée) : configurer"
echo "les fournisseurs OAuth Google/GitHub dans le dashboard Supabase :"
echo "  https://supabase.com/dashboard/project/${PROJECT_REF}/auth/providers"
echo ""
echo "URI de redirection à renseigner côté Google Cloud Console / GitHub :"
echo "  https://${PROJECT_REF}.supabase.co/auth/v1/callback"
echo ""
echo "Pour connecter le scraper (scraper/) à cette même base -- alimente les"
echo "watchlists persos, cf. scraper/connecteur_supabase.py -- ajoute ces 2"
echo "secrets GitHub Actions sur le dépôt (Settings > Secrets and variables >"
echo "Actions) :"
echo "  SUPABASE_URL = https://${PROJECT_REF}.supabase.co"
echo "  SUPABASE_SERVICE_ROLE_KEY = ${SERVICE_ROLE_KEY}"
echo "(clé SECRÈTE, contourne les policies RLS -- ne JAMAIS l'utiliser côté"
echo "SaaS/navigateur, uniquement dans les secrets GitHub Actions du scraper)"
echo ""
echo "Notifications push/email (optionnel, cf. README.md section 3) :"
echo "  - VAPID (push) : générer les clés, mettre NEXT_PUBLIC_VAPID_PUBLIC_KEY"
echo "    dans .env.local/Vercel, VAPID_PRIVATE_KEY + VAPID_CLAIM_EMAIL en"
echo "    secrets GitHub Actions."
echo "  - Resend (email) : créer un compte sur resend.com, ajouter"
echo "    RESEND_API_KEY + RESEND_FROM_EMAIL en secrets GitHub Actions."
