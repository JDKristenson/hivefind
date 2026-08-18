#!/usr/bin/env bash
# KAM: move Phase 0 bootstrap secrets into 1Password and retire ~/.config/kam/env.local on the Mac.
# Run once, from a plain terminal, AFTER:   eval $(op signin)
# What it does (idempotent):
#   1. rotates the kam_writer DB password (self-service, no admin credential)
#   2. syncs the rotated bootstrap file to EC2 so its timers keep working (EC2 keeps env.local until Phase 2)
#   3. creates vault "KAM" and three items from the bootstrap values (values never echoed)
#   4. creates a read-only service account "kam-mac" on vault KAM and stores its token (0600) for launchd
#   5. points kam/.env.op at vault KAM, verifies `op run -- kam verify`, then deletes env.local
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
ENV_LOCAL="$HOME/.config/kam/env.local"
ENV_OP="$REPO/kam/.env.op"
SA_TOKEN_FILE="$HOME/.config/kam/op-service-account.token"
EC2="ec2-user@3.148.28.93"; KEY="$HOME/.ssh/openclaw-key.pem"
VAULT="KAM"

op whoami >/dev/null 2>&1 || { echo "not signed in. Run:  eval \$(op signin)   then re-run this script."; exit 1; }
[ -s "$ENV_LOCAL" ] || { echo "no bootstrap file at $ENV_LOCAL; nothing to migrate."; exit 1; }
if [ -n "${CLAUDECODE:-}" ]; then echo "run this from a plain terminal, not inside Claude Code."; exit 1; fi

get() { grep -E "^$1=" "$ENV_LOCAL" | head -1 | cut -d= -f2-; }

echo "1) rotating kam_writer password"
KAM_SKIP_OP=1 kam rotate-db-password >/dev/null

echo "2) syncing rotated bootstrap to EC2"
scp -q -i "$KEY" -o LogLevel=ERROR "$ENV_LOCAL" "$EC2:.config/kam/env.local"
ssh -i "$KEY" -o BatchMode=yes -o LogLevel=ERROR "$EC2" 'chmod 600 ~/.config/kam/env.local; sed -i "s/^KAM_HOST=mac/KAM_HOST=ec2/" ~/.config/kam/env.local' 2>/dev/null

echo "3) vault + items"
op vault get "$VAULT" >/dev/null 2>&1 || op vault create "$VAULT" >/dev/null
upsert() {  # title field value  (value passed as an argument to op, never printed)
  if op item get "$1" --vault "$VAULT" >/dev/null 2>&1; then
    op item edit "$1" --vault "$VAULT" "$2=$3" >/dev/null
  else
    op item create --category "API Credential" --title "$1" --vault "$VAULT" "$2=$3" >/dev/null
  fi
}
upsert "KAM Supabase kam_writer" "dsn[password]" "$(get KAM_DB_DSN)"
upsert "OpenRouter"              "credential"    "$(get OPENROUTER_API_KEY)"
upsert "KAM Notion integration"  "credential"    "$(get NOTION_TOKEN)"

echo "4) service account for launchd (read-only on vault $VAULT)"
if [ ! -s "$SA_TOKEN_FILE" ]; then
  op service-account create "kam-mac" --vault "$VAULT:read_items" --raw > "$SA_TOKEN_FILE"
  chmod 600 "$SA_TOKEN_FILE"
fi

echo "5) verify through 1Password, then retire the bootstrap file"
sed -i '' "s#op://[A-Za-z0-9 _-]*/KAM Supabase kam_writer/#op://$VAULT/KAM Supabase kam_writer/#; s#op://[A-Za-z0-9 _-]*/OpenRouter/#op://$VAULT/OpenRouter/#; s#op://[A-Za-z0-9 _-]*/KAM Notion integration/#op://$VAULT/KAM Notion integration/#" "$ENV_OP"
op run --env-file "$ENV_OP" -- kam verify
OP_SERVICE_ACCOUNT_TOKEN="$(cat "$SA_TOKEN_FILE")" op run --env-file "$ENV_OP" -- kam verify >/dev/null
rm -f "$ENV_LOCAL"
op run --env-file "$ENV_OP" -- kam doctor || true
echo "done. Mac uses 1Password now (session or service account); EC2 keeps its bootstrap file until Phase 2's per-agent vaults."
