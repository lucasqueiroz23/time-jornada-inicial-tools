---
name: revisar-pr
description: Revisa o pull request de outra pessoa e entrega um relatório classificado em Blocking, High, Medium e Suggestions, com a regra de quando aprovar e o comentário pronto para o PR. Use quando alguém pedir para revisar um PR ou uma lista de PRs, comentar a revisão no PR ou decidir se aprova.
argument-hint: "[link ou número do PR]"
---

# Revisar PR

PR a revisar: $ARGUMENTS

Esta skill é para revisar o PR de outra pessoa. Para revisar a sua própria mudança antes de abrir o PR, use o agent `revisor-de-codigo`.

A revisão responde a uma pergunta: este PR pode ser mergeado como está? A classificação existe para quem abriu o PR saber o que precisa corrigir antes do merge e o que é só sugestão, sem ter que adivinhar o peso de cada comentário.

## Fluxo

1. **Entenda a intenção.** Leia o que o autor disse sobre o PR: a descrição, a tarefa ligada e qualquer mensagem que a pessoa tenha colado. A revisão mede o diff contra essa intenção. Um PR que avisa que é a primeira parte de um trabalho não é reprovado por faltar a segunda.
2. **Pegue o diff.** Atualize o repositório com `git fetch --prune` e compare com `git diff origin/<destino>...origin/<branch>`. Quando o PR vem de um fork, a branch não está em `origin`: no GitHub, use `gh pr diff <número>`. Para os dados do PR (título, descrição, branch de destino, comentários), use a ferramenta que a sessão tiver para a plataforma do repositório, como o `gh` no GitHub ou um MCP. Se não houver nenhuma, peça para a pessoa colar o que falta.
3. **Leia o contexto em volta do diff**, não só as linhas alteradas: quem chama o código, a configuração de ambiente, o pipeline e, quando houver, os outros PRs da mesma tarefa.
4. **Rode o que der:** build, lint e testes do repositório, em um `git worktree` temporário, para não mexer na pasta de trabalho da pessoa. Remova o worktree ao terminar. Rodar o PR executa o código dele na máquina, então faça isso só depois de ler o diff, e pergunte antes quando o PR vier de um fork ou de alguém de fora do time.
5. **Classifique cada achado** pela tabela abaixo.
6. **Mostre o relatório** a quem pediu a revisão.
7. **Comente e aprove só se a pessoa pedir**, seguindo a regra de aprovação.

## Classificação

| Nível | Critério |
| --- | --- |
| **Blocking** | Quebra produção, perde ou corrompe dado, abre falha de segurança, ou o PR não faz o que diz. Não pode ser mergeado assim. |
| **High** | Bug real ou risco relevante no escopo do PR, que deve ser corrigido antes do merge, mesmo sem quebrar tudo. |
| **Medium** | Problema real que não impede o merge: afeta só ambiente de teste, depende de confirmação externa, ou só passa a valer em uma fase seguinte. Nesse último caso, marque "antes de <fase>". |
| **Suggestions** | Melhoria, simplificação, cobertura de teste ou observação de desenho. |

Na dúvida entre dois níveis, o critério é o efeito em produção do PR como ele está, não o efeito de uma fase futura.

## Regra de aprovação

- **Aprova** quando não há item em Blocking nem em High. Medium e Suggestions não seguram a aprovação.
- **Não aprova** quando há qualquer item em Blocking ou High. Nesse caso, o resultado é pedir alterações.

Comentar, aprovar e pedir alterações são ações que o autor e o time veem. Faça só com pedido explícito de quem pediu a revisão, naquela conversa. Antes de postar, confira que o PR continua aberto e que o commit de topo é o mesmo que você revisou: se entrou commit novo, revise a diferença antes.

## Formato do comentário

Em português, um comentário geral por PR:

```markdown
## Revisão (commit <sha curto>)

**Resultado: aprovado.** | **Resultado: não aprovado** (N Blocking, N High).

**Verificado:** <o que foi lido e rodado; o que não foi possível verificar>

### Blocking
### High
### Medium
### Suggestions
```

- As quatro seções aparecem sempre. Seção vazia leva "Nenhum.".
- Os itens são numerados em sequência única no comentário. Cada um tem título em negrito, o fato, o efeito e, quando houver, a sugestão. Cite arquivo, função ou variável entre crases.
- Só entra o que foi conferido no código. Suposição vai marcada como "confirmar".
- Diga o que rodou e o que não rodou. Uma aprovação sem os testes rodados precisa dizer isso.
- Não prometa nada em nome de quem pediu a revisão.

## Achado de segurança

Uma falha explorável não vai detalhada em comentário de PR, onde fica visível para qualquer pessoa com acesso ao repositório.

- **No relatório mostrado na conversa**, o achado aparece completo, para quem pediu a revisão levá-lo ao dono do código e ao time de segurança por um canal restrito.
- **No comentário do PR**, o achado continua contando como Blocking, mas o item traz só este texto: "Achado de segurança. O detalhe foi enviado por canal restrito." Sem arquivo, linha nem forma de explorar.

## Como postar

Use a ferramenta que a sessão tiver para a plataforma do repositório. No GitHub, o `gh` cobre os três casos: `gh pr comment --body-file <arquivo>`, `gh pr review --approve` e `gh pr review --request-changes --body-file <arquivo>`. O pedido de alterações exige um corpo.

Se a sessão não tiver ferramenta para a plataforma, entregue o comentário pronto para a pessoa colar e diga qual ação ela deve marcar. Não tente contornar com chamadas diretas à API usando credenciais ou cookies da pessoa.

Em algumas plataformas, um commit novo zera a aprovação já dada. Em uma nova rodada, revise o que mudou desde o commit revisado, com `git diff <sha anterior> origin/<branch>`, e aprove de novo se for o caso.

Ao terminar, responda com o resultado de cada PR e, quando você tiver postado, o link do comentário.
