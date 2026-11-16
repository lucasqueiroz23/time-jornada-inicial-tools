#!/usr/bin/env bash
# Mostra o que deste repositório ainda falta na pasta pessoal do Claude Code
# e se o MCP do Jira está configurado. Não instala nem altera nada. O
# "claude mcp list" inicia os servidores MCP já configurados para testar a
# conexão, então pode levar alguns segundos.
#
# Saída, uma linha por item:
#   agent <faltando|igual|diferente> <arquivo>
#   skill <faltando|igual|diferente> <pasta>
#   mcp   <oficial|outro|faltando|erro|sem-cli> [linha do "claude mcp list"]
set -u

raiz="$(cd "$(dirname "$0")/../../.." && pwd)"
destino="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

estado() {
  if [ ! -e "$2" ]; then
    echo faltando
  elif diff -rq -x .DS_Store "$1" "$2" >/dev/null 2>&1; then
    echo igual
  else
    echo diferente
  fi
}

for agent in "$raiz"/.claude/agents/*.md; do
  [ -e "$agent" ] || continue
  nome="$(basename "$agent")"
  echo "agent $(estado "$agent" "$destino/agents/$nome") $nome"
done

for skill in "$raiz"/.claude/skills/*/; do
  [ -e "$skill" ] || continue
  nome="$(basename "$skill")"
  # A skill setup só faz sentido dentro deste repositório.
  [ "$nome" = "setup" ] && continue
  echo "skill $(estado "${skill%/}" "$destino/skills/$nome") $nome"
done

if ! command -v claude >/dev/null 2>&1; then
  echo "mcp sem-cli"
  exit 0
fi

# Se a listagem falhar, não dá para afirmar que o MCP está faltando.
if ! lista="$(claude mcp list 2>&1)" || [ -z "$lista" ]; then
  echo "mcp erro $(echo "$lista" | tail -1)"
  exit 0
fi

oficial="$(echo "$lista" | grep -i 'mcp\.atlassian\.com' | head -1)"
outro="$(echo "$lista" | grep -i -E 'atlassian|jira' | head -1)"

if [ -n "$oficial" ]; then
  echo "mcp oficial $oficial"
elif [ -n "$outro" ]; then
  echo "mcp outro $outro"
else
  echo "mcp faltando"
fi
