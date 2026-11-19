#!/usr/bin/env python3
"""Hook Stop (sessão principal).
Se um subagente editou arquivos e nenhum `revisor` rodou depois, bloqueia o encerramento
do turno UMA vez com o lembrete. Na segunda tentativa (stop_hook_active=true) deixa passar
e limpa o marcador, para nunca travar a sessão."""
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
if not os.path.isfile(p):
    sys.exit(0)
if d.get("stop_hook_active"):
    os.remove(p)
    sys.exit(0)
try:
    info = json.load(open(p))
except Exception:
    info = {}
quem = info.get("agent_type") or "um subagente"
print(json.dumps({
    "decision": "block",
    "reason": (
        f"Validação independente pendente (regra de orquestração do time): o subagente `{quem}` editou arquivos "
        "e nenhum `revisor` rodou depois. Antes de encerrar: dispare o `revisor` com o alvo (paths ou `git diff`), "
        "o brief original com o critério de pronto e os critérios de revisão, sem repassar o relatório do executor; "
        "depois cruze os dois resultados. Se a entrega não deve ser revisada (o usuário pediu para pular, ou as "
        "edições foram triviais e você já conferiu o diff inteiro), diga isso explicitamente ao usuário e encerre de novo."
    )
}, ensure_ascii=False))
