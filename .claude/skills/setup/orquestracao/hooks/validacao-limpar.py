#!/usr/bin/env python3
"""Hook SubagentStart (matcher: revisor).
Um revisor foi disparado nesta sessão: a validação independente deixa de estar pendente."""
import json, os, re, sys

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if not isinstance(d, dict):
    sys.exit(0)
sid = d.get("session_id")
# O id vira nome de arquivo: só aceita o que não sai da pasta de estado.
if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", sid):
    sys.exit(0)
p = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "state", "validacao-pendente", sid)
if sid and os.path.isfile(p):
    os.remove(p)
