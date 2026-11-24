# Fluxo de desenvolvimento

Este é o caminho de uma tarefa no time Jornada Inicial, da ideia ao PR. O fluxo é spec-driven: antes de escrever código, o time combina por escrito o que precisa ser feito, e a IA trabalha em cima desse combinado, não de um título de tarefa.

O motivo é simples. Uma tarefa vaga entregue a uma IA vira código que parece certo e resolve o problema errado. Cada etapa abaixo existe para tirar uma camada de incerteza antes da próxima.

## As etapas

| Etapa | Quem faz | Comando | Onde roda | O que sai |
| --- | --- | --- | --- | --- |
| 1. Refinar | Produto, projetos ou quem conhece a demanda | `/refinar-tarefa ABC-123` | Qualquer pasta | Descrição da tarefa reescrita, com critérios de aceite. Status "Refinado". |
| 2. PRD | Quem conhece a demanda, com revisão do time | `/gerar-prd ABC-123` | Qualquer pasta | PRD em um comentário da tarefa, para o time revisar. |
| 3. Desenvolver | Dev | `/desenvolver-tarefa ABC-123` | Repositório do projeto | Especificação em `.specs/`, código, testes e commits. |
| 4. Revisar a própria mudança | Dev | Agent `revisor-de-codigo` e `/security-check` | Repositório do projeto | Achados corrigidos antes do PR. |
| 5. Abrir o PR | Dev | `/descricao-de-pr` | Repositório do projeto | Descrição do PR com o que muda e como testar. |
| 6. Revisar o PR de outra pessoa | Dev | `/revisar-pr <link>` | Repositório do projeto | Relatório em Blocking, High, Medium e Suggestions, e a decisão de aprovar. |

As etapas 4 e 5 já fazem parte da `/desenvolver-tarefa`, que chama as ferramentas no fim da implementação. Elas aparecem separadas porque também funcionam sozinhas.

A etapa 2 vale para qualquer tipo de tarefa. A `/gerar-prd` ajusta o tamanho do documento ao tipo dela: o PRD de uma correção pequena cabe em poucas linhas.

## A etapa de desenvolvimento por dentro

A `/desenvolver-tarefa` lê a tarefa e o PRD no Jira e conduz o [TLC Spec-Driven](../.claude/skills/tlc-spec-driven/README.md), o framework que o time adotou. Você conversa em português e não precisa decorar os comandos dele.

O TLC tem quatro fases e escolhe a profundidade pelo tamanho da mudança:

```
Especificar  →  Desenhar  →  Quebrar em passos  →  Executar
 obrigatória    opcional        opcional          obrigatória
```

| Tamanho da mudança | O que acontece |
| --- | --- |
| Pequena: até 3 arquivos, cabe em uma frase | Modo rápido: descreve, implementa, verifica e faz o commit. |
| Média: funcionalidade clara | Especificação curta e implementação. |
| Grande: vários componentes | Especificação com requisitos numerados, desenho e quebra em passos. |
| Complexa: ambiguidade ou domínio novo | Tudo acima, mais discussão das áreas cinzentas, pesquisa e validação guiada. |

O que o time já decidiu no Jira entra como ponto de partida: o TLC não pergunta de novo o que a tarefa e o PRD respondem. As perguntas dessa etapa são as técnicas.

### O que fica no repositório do projeto

O TLC guarda o trabalho na pasta `.specs/` do projeto:

```
.specs/
├── project/      visão, roteiro e a memória de decisões do projeto
├── codebase/     mapa do código existente: stack, arquitetura, convenções e testes
├── features/     uma pasta por tarefa, com a especificação, o desenho e os passos
└── quick/        tarefas pequenas feitas no modo rápido
```

A pasta de cada tarefa leva a chave do Jira no nome, como `.specs/features/abc-123-resumo-curto/`. No modo rápido, ela fica em `.specs/quick/`, com a numeração do TLC na frente.

### Primeira vez em um projeto

Na primeira tarefa em um repositório, a `/desenvolver-tarefa` oferece mapear o código existente. Leva alguns minutos, acontece uma vez só e melhora todas as especificações seguintes, porque o TLC passa a conhecer a arquitetura, as convenções e como os testes rodam.

### Falando direto com o TLC

Quando você quiser usar o TLC sem passar pelo Jira, estas frases acionam cada parte dele:

| Para | Diga |
| --- | --- |
| Mapear um projeto existente | `map codebase` |
| Especificar uma funcionalidade | `specify feature <nome>` |
| Discutir pontos em aberto | `discuss feature` |
| Desenhar a solução | `design feature` |
| Quebrar em passos | `break into tasks` |
| Implementar | `implement` |
| Validar o que foi feito | `validate` |
| Fazer uma correção pequena | `quick fix: <descrição>` |
| Parar e retomar depois | `pause work` e `resume work` |

## Os status no Jira

| Status | Significado | Quem move |
| --- | --- | --- |
| Refinado | A descrição diz o que fazer e como saber que terminou. | A `/refinar-tarefa`, depois do aceite. |
| PRD em revisão | O PRD está na tarefa, esperando a revisão do time. | A `/gerar-prd`, depois do aceite. |
| PRD aprovado | O time revisou e concorda com os requisitos. | O time, à mão. |
| Em andamento | Alguém começou a desenvolver. | A `/desenvolver-tarefa`, depois do aceite. |
| EM REVIEW | O PR está aberto, esperando a revisão. | A `/desenvolver-tarefa`, depois do aceite, quando o PR é aberto. |
| AGUARDANDO DEPLOY | Todos os PRs da tarefa foram mesclados e a mudança ainda não está em produção. | Quem fez o merge, à mão, ou a `/desenvolver-tarefa` chamada de novo com a mesma chave. |
| Concluído | A mudança está em produção. | Quem acompanhou o deploy, à mão, ou a `/desenvolver-tarefa`, depois do aceite e da confirmação de que está em produção. |

Nenhuma skill grava ou move nada no Jira sem um aceite explícito na conversa.

### Depois do merge

O merge acontece no repositório, dias depois do desenvolvimento e fora de qualquer sessão do Claude Code. Nenhuma skill enxerga esse momento, então a tarefa não anda sozinha: ela fica em "EM REVIEW" até alguém mover.

Há três jeitos de não deixar tarefa pronta parada:

- Mover à mão logo depois do merge.
- Rodar `/desenvolver-tarefa ABC-123` de novo. Ela confere os PRs da tarefa, ou pergunta a você se a sessão não tiver essa informação, e oferece mover.
- Criar no Jira uma regra de automação que move a tarefa quando o PR é mesclado. É a única forma de pegar o merge sem depender de alguém lembrar, e precisa de quem administra o projeto no Jira.

Merge não é deploy. A tarefa só vai para "Concluído" quando a mudança está em produção.

## Para começar

1. Clone este repositório e abra o Claude Code na raiz dele.
2. Rode `/setup`. Ele copia as skills e os agents para a sua pasta pessoal, configura o MCP do Jira e oferece o kit de orquestração, que é opcional.
3. Abra o Claude Code no repositório do projeto e rode `/desenvolver-tarefa` com a chave da tarefa.
