#!/usr/bin/python3
"""launchd wrapper for kam on the Mac. Rooted at /usr/bin/python3 so the job (and its children) carry the TCC grant for ~/Desktop.
Usage: /usr/bin/python3 kam_launchd_wrapper.py <kam args...>
"""
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
env = dict(os.environ)
env["PATH"] = f"{HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
env["HOME"] = HOME
env.setdefault("KAM_HOST", "mac")
env.setdefault("KAM_SKIP_OP", "1")
for k in ("ANTHROPIC_API_KEY", "CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID"):
    env.pop(k, None)
kam = f"{HOME}/.local/bin/kam"
sys.exit(subprocess.run([kam] + sys.argv[1:], env=env, check=False).returncode)
