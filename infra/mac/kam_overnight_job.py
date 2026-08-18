#!/usr/bin/python3
"""06:15 ET Mac job: kam overnight, then heartbeat kam-overnight-mac. Rooted at /usr/bin/python3 for the Desktop TCC grant."""
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
env = dict(os.environ)
env["PATH"] = f"{HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
env["HOME"] = HOME
env["KAM_HOST"] = "mac"
tok = os.path.join(HOME, ".config", "kam", "op-service-account.token")
if os.path.isfile(tok):
    with open(tok) as f:  # 1Password service account (read-only on vault KAM); kam then resolves kam/.env.op via `op run`
        env["OP_SERVICE_ACCOUNT_TOKEN"] = f.read().strip()
else:
    env["KAM_SKIP_OP"] = "1"  # Phase 0 bootstrap: ~/.config/kam/env.local
kam = f"{HOME}/.local/bin/kam"
rc = subprocess.run([kam, "overnight"], env=env, check=False).returncode
if rc == 0:
    subprocess.run([kam, "heartbeat", "kam-overnight-mac"], env=env, check=False)
sys.exit(rc)
