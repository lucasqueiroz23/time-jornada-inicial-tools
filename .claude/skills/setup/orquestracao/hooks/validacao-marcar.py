#!/usr/bin/env python3
"""Hook SubagentStop (sem matcher).
Se o subagente que terminou editou arquivos (Edit/Write/NotebookEdit no transcript dele),
marca "validação independente pendente" para a sessão principal em
state/validacao-pendente/<session_id>, na pasta pessoal do Claude Code. O marcador é lido pelo hook de Stop
(validacao-gate.py) e apagado quando um `revisor` é disparado (validacao-limpar.py)."""
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
atype = d.get("agent_type") or ""
path = d.get("agent_transcript_path") or ""
if not isinstance(atype, str) or not isinstance(path, str):
    sys.exit(0)
path = os.path.expanduser(path)
if not sid or not atype or atype in ("revisor", "pesquisador", "varredor") or not os.path.isfile(path):
    sys.exit(0)
pat = re.compile(r'"name":\s*"(Edit|Write|NotebookEdit|MultiEdit)"')
editou = False
with open(path, "r", errors="ignore") as f:
    for line in f:
        if '"tool_use"' in line and pat.search(line):
            editou = True
            break
if not editou:
    sys.exit(0)
d_dir = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "state", "validacao-pendente")
os.makedirs(d_dir, exist_ok=True)
with open(os.path.join(d_dir, sid), "w") as f:
    f.write(json.dumps({"agent_type": atype, "agent_id": d.get("agent_id", "")}))
