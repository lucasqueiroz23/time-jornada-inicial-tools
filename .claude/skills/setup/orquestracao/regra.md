# Orquestração: a janela principal coordena, subagentes executam

A janela principal (esta sessão) é a **coordenadora**: entende o pedido, decide, verifica e sintetiza para o usuário. Trabalho mecânico, volumoso ou paralelizável vai para **subagentes com modelos mais baratos** pela Agent tool. O modelo padrão dos subagentes é Sonnet (`CLAUDE_CODE_SUBAGENT_MODEL` no settings.json), e subagentes não podem disparar outros subagentes (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`). O Haiku é o mais barato; o Sonnet custa cerca do dobro, e os modelos de topo, várias vezes mais.

## Fica com a coordenadora (não delegar)
- Interpretar a intenção do usuário, perguntar quando ambíguo, escolher entre abordagens.
- A síntese final e a resposta ao usuário.
- Ações destrutivas ou externas: commit, push, delete, mensagens, escrita em Jira/Confluence.
- Consulta pontual de um fato que ela já sabe onde está (um arquivo, um símbolo, um valor).

## O que delegar, e para quem

| Tarefa | Agente | Modelo |
|---|---|---|
| Varrer muitos arquivos, contar, listar, extrair, checar padrão com critério objetivo, resumir um log, uma reunião ou um documento longo | `varredor` | Haiku |
| Localizar código, mapear um fluxo, responder "onde" ou "como" lendo o repositório, pesquisar docs | `pesquisador` (ou `Explore`) | Sonnet |
| Implementar mudança já delimitada, escrever testes, corrigir bug com reprodução conhecida, rodar e interpretar uma suíte | `executor` | Sonnet |
| Revisar um diff ou branch contra critérios dados (bugs, convenções, segurança, spec) | `revisor` | Sonnet |
| Sub-tarefa que exige o mesmo julgamento da coordenadora (arquitetura, código financeiro crítico, spec ambígua) | fazer na própria janela, ou `general-purpose` passando `model` com o mesmo modelo da janela | igual à janela |

Regra de bolso: se o critério de pronto cabe em duas linhas, é Haiku ou Sonnet. Se precisa de bom senso, é da janela.

## Como escrever o brief
Todo prompt de subagente traz, nesta ordem: **contexto** (o que é o projeto e por que a tarefa importa), **objetivo** (uma frase), **escopo** (paths, janela de tempo, limites, o que não tocar), **critério de pronto** e **formato de saída** (curto, com `arquivo:linha` quando for código, sem despejar arquivos inteiros). Tarefas independentes saem em **paralelo na mesma mensagem**, em background. Tarefa que depende do resultado de outra espera a primeira terminar.

## Quando o subagente volta
- O relatório é entrada, não conclusão. Confira o que for barato conferir: um `grep`, um `git diff`, abrir o arquivo citado.
- Não refaça o trabalho na janela. Se veio incompleto, mande de volta com `SendMessage` para o mesmo agente, que já tem o contexto.
- Ao usuário, repasse só o que muda a decisão, e diga em uma linha que o resultado veio de um subagente.
- Se o subagente editou arquivos, a entrega ainda não está pronta: passa pela validação independente abaixo.

## Validação independente (obrigatória)
Toda entrega de subagente que **editou arquivos** passa por um `revisor` antes de chegar ao usuário. O revisor recebe o alvo (paths ou `git diff`), o brief original com o critério de pronto e os critérios de revisão. Não recebe o relatório do executor, de propósito: ele verifica a mudança, não o relato. Quando houver testes ou lint no escopo, o revisor roda por conta própria.

A coordenadora cruza os dois resultados:
- Revisor aprovou e a conferência barata bate: reporta ao usuário, dizendo que passou por revisão independente.
- Revisor apontou achados: devolve ao **mesmo** executor com `SendMessage`, só os achados, e pede nova revisão do que mudou. No máximo duas rodadas; depois, leva o impasse ao usuário com os dois lados.
- Revisor e executor discordam sobre um fato: a coordenadora confere ela mesma aquele ponto antes de decidir.

Exceções, sempre ditas explicitamente ao usuário: o usuário pediu para pular; ou a edição foi trivial (texto, config de uma linha) e a coordenadora já conferiu o diff inteiro. O hook de Stop lembra quando um subagente editou arquivos e nenhum revisor rodou depois, e bloqueia o encerramento do turno uma vez.

## Quando não delegar
- Tarefa de um passo que a janela resolve com uma chamada de ferramenta.
- Loop interativo em que cada passo depende do anterior e a janela já tem o estado em contexto. Delegue só se puder entregar o loop inteiro.
- Quando escrever o brief custa mais do que fazer a tarefa.
