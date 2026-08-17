#!/usr/bin/env bash
# KAM EC2 install (idempotent). Run as ec2-user with sudo available. Spec: PRD v1.1 §6.7, §10.
set -euo pipefail
BRANCH="${KAM_BRANCH:-kam-phase-0}"
REPO="https://github.com/JDKristenson/hivefind.git"
export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
uv python install 3.13 --quiet || true

if [ ! -d "$HOME/hivefind/.git" ]; then
  git clone --branch "$BRANCH" --single-branch "$REPO" "$HOME/hivefind"
else
  git -C "$HOME/hivefind" fetch origin "$BRANCH" --quiet
  git -C "$HOME/hivefind" checkout -q "$BRANCH"
  git -C "$HOME/hivefind" pull -q --ff-only origin "$BRANCH"
fi
cd "$HOME/hivefind"
uv tool install --editable . --python 3.13 --force --quiet
mkdir -p "$HOME/kam/reports" "$HOME/.config/kam"; chmod 700 "$HOME/.config/kam"
if [ ! -s "$HOME/.config/kam/env.local" ]; then
  echo "NOTE: $HOME/.config/kam/env.local is missing; scp it from the Mac (0600) before the timers can reach the log."
fi
sudo cp infra/ec2/systemd/*.service infra/ec2/systemd/*.timer /etc/systemd/system/
sudo systemctl daemon-reload
for t in kam-mirror kam-watchdog kam-verify-anchor kam-overnight-ec2 kam-ledger; do
  sudo systemctl enable --now "$t.timer" >/dev/null
done
echo "installed: $(kam --help 2>/dev/null | head -1)"
systemctl list-timers --no-pager | grep kam- || true
free -m | head -2; df -h /home | tail -1
