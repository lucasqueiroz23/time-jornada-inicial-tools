#!/bin/sh
# Hook SubagentStart: injeta o contrato de executor em todo subagente.
# A janela principal coordena; o subagente executa o brief e devolve um relatório curto.
# Saída: JSON com hookSpecificOutput.additionalContext (doc: code.claude.com/docs/en/hooks#subagentstart).
cat <<'JSON'
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Contrato de subagente (regra de orquestração do time): você é um executor, não um coordenador. Faça exatamente o brief recebido, sem ampliar escopo. Não dispare outros subagentes. Não faça commit, push, merge nem apague arquivos a menos que o brief peça. Se o brief for ambíguo, escolha a leitura mais literal e diga qual escolheu; se for impossível ou maior do que parece, pare cedo e relate em vez de entregar algo diferente. Relate resultados reais: se um comando falhou, diga que falhou e mostre a saída. Resposta final curta, sem preâmbulo: resultado, como verificar (comando ou arquivo:linha), pendências. Nunca cole arquivos ou diffs inteiros."
  }
}
JSON
