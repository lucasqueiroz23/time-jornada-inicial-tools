# Fluxo de desenvolvimento

Este é o caminho de uma tarefa no time Jornada Inicial, da ideia ao PR. O fluxo é spec-driven: antes de escrever código, o time combina por escrito o que precisa ser feito, e a IA trabalha em cima desse combinado, não de um título de tarefa.

O motivo é simples. Uma tarefa vaga entregue a uma IA vira código que parece certo e resolve o problema errado. Cada etapa abaixo existe para tirar uma camada de incerteza antes da próxima.

## As etapas

| Etapa | Quem faz | Comando | Onde roda | O que sai |
| --- | --- | --- | --- | --- |
| 1. Refinar | Produto, projetos ou quem conhece a demanda | `/refinar-tarefa ABC-123` | Qualquer pasta | Descrição da tarefa reescrita, com critérios de aceite. Status "Refinado". |
| 2. PRD | Quem conhece a demanda, com revisão do time | `/gerar-prd ABC-123` | Qualquer pasta | PRD em um comentário da tarefa, para o time revisar. |
| 3. Desenvolver | Dev | `/desenvolver-tarefa ABC-123` | Repositório do projeto | Plano em `.specs/`, código, testes, commits e o parecer de uma revisão independente. |
| 4. Checar a própria mudança | Dev | `/security-check` e, se quiser uma segunda leitura, o agent `revisor-de-codigo` | Repositório do projeto | Achados corrigidos antes do PR. |
| 5. Abrir o PR | Dev | `/descricao-de-pr` | Repositório do projeto | Descrição do PR com o que muda e como testar. |
| 6. Revisar o PR de outra pessoa | Dev | `/revisar-pr <link>` | Repositório do projeto | Relatório em Blocking, High, Medium e Suggestions, e a decisão de aprovar. |

As etapas 4 e 5 já fazem parte da `/desenvolver-tarefa`, que roda a checagem de segurança e escreve a descrição do PR no fim. O `revisor-de-codigo` fica para quando você pedir, porque a revisão independente do lean já aconteceu. Elas aparecem separadas porque também funcionam sozinhas.

A etapa 2 vale para qualquer tipo de tarefa. A `/gerar-prd` ajusta o tamanho do documento ao tipo dela: o PRD de uma correção pequena cabe em poucas linhas.

## A etapa de desenvolvimento por dentro

A `/desenvolver-tarefa` lê a tarefa e o PRD no Jira e conduz o [TLC Spec Lean](../.claude/skills/tlc-spec-lean/SKILL.md), o framework que o time adotou. Você conversa em português e não precisa decorar os comandos dele.

O lean tem três fases:

```
Plano  →  Build  →  Revisão
```

| Fase | O que acontece | O que você faz |
| --- | --- | --- |
| Plano | As decisões de produto que faltam são perguntadas e o plano é escrito: o problema, o caminho pelo código, as decisões difíceis de reverter e os critérios de aceite, agrupados em fatias. | Responde às perguntas e aprova o plano. É a única parada obrigatória. |
| Build | Uma fatia por vez, de ponta a ponta: código, testes e um commit. | Decide só o que o plano não previu. |
| Revisão | Um subagente que não escreveu o código confere o pedido e o plano contra o que foi feito. Depois vem uma única rodada de correção. | Decide os achados que forem de produto. |

Uma fatia é um resultado que alguém consegue ver funcionando, cortado por todas as camadas que ele precisa. "A API" ou "a tela" são camadas, não fatias.

Mudança pequena, de menos de três arquivos, mais ou menos, e sem decisão difícil de reverter, dispensa o plano. As perguntas e a revisão acontecem do mesmo jeito.

O que o time já decidiu no Jira entra como ponto de partida: o lean não pergunta de novo o que a tarefa e o PRD respondem. As perguntas dessa etapa são as que o PRD deixou de fora, quase sempre as que só aparecem quando se olha o código.

### O que fica no repositório do projeto

O lean guarda o trabalho na pasta `.specs/` do projeto:

```
.specs/
├── STATE.md                 decisões que as próximas tarefas precisam respeitar
└── features/
    └── abc-123-resumo-curto/
        ├── request.md       o pedido como veio: a tarefa do Jira e o PRD
        ├── plan.md          o plano aprovado e o registro da revisão
        └── review.md        o parecer do revisor
```

A pasta de cada tarefa leva a chave do Jira no nome. Se o repositório do projeto ainda não tem nenhuma spec versionada, a `/desenvolver-tarefa` pergunta antes do primeiro commit se a pasta entra no git: é uma decisão do time daquele projeto.

### Por que o lean

O time começou com o `tlc-spec-driven` 2.0.0. Na hora de atualizar, testou em tarefas reais a versão nova dele, a 4.1.0, e o `tlc-spec-lean` 3.2.0, e ficou com o lean. A 4.1.0 do `tlc-spec-driven` não tem mais o modo rápido, registra um teste por critério e confere as etapas por script, o que pesa em tarefa pequena: no teste, uma correção de uma linha gerou uma especificação de nove critérios. O lean mantém o que deu resultado nos dois testes, que são as perguntas de produto antes de escrever, o teste para cada regra e o revisor que não é o autor, com uma parada só.

O `tlc-spec-driven` continua fazendo sentido para trabalho muito grande, em várias sessões, ou que precise de uma trilha de prova por critério. Se aparecer um caso assim, ele pode voltar para o repositório.

### Falando direto com o lean

Quando você quiser usar o lean sem passar pelo Jira, estas frases acionam cada parte dele:

| Para | Diga |
| --- | --- |
| Planejar uma funcionalidade | `plan feature <nome>` |
| Construir um plano aprovado | `build this plan` |
| Revisar o que foi construído | `review this work` |

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
