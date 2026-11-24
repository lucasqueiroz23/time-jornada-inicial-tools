---
name: desenvolver-tarefa
description: Desenvolve uma tarefa do Jira seguindo o fluxo spec-driven do time. Lê a tarefa e o PRD, confere se ela está pronta, prepara o repositório do projeto e conduz o plano e a implementação com a skill tlc-spec-lean, fechando com checagem de segurança, revisão, descrição do PR e a atualização do status da tarefa no Jira. Use quando alguém pedir para desenvolver, implementar ou começar uma tarefa do Jira.
argument-hint: "[chave ou link da tarefa]"
---

# Desenvolver tarefa

Tarefa: $ARGUMENTS

Esta skill é a ponte entre o Jira e o desenvolvimento. O time refina a tarefa e, quando faz sentido, escreve o PRD na própria tarefa. A partir daí, quem desenvolve usa o TLC Spec Lean (skill `tlc-spec-lean`) para fechar um plano, construir em fatias e passar por uma revisão independente.

O lean é em inglês e não conhece o Jira. O seu papel aqui é poupar a pessoa disso: você busca o que já foi decidido na tarefa, entrega ao lean como ponto de partida e conduz as fases em português. A pessoa não precisa decorar comando nenhum.

Esta skill roda no repositório do projeto que a tarefa altera, não no repositório de ferramentas do time.

## Passo a passo

### 1. Busque a tarefa no Jira

A pessoa pode informar a chave (como `ABC-123`) ou colar o link; no caso do link, tire a chave dele. Se não veio nenhum dos dois, peça.

Leia o título, a descrição, o status, os comentários, a tarefa pai ou o épico e as tarefas ligadas. Se a sessão tiver a ferramenta de informações de desenvolvimento do Jira, veja também os PRs ligados à tarefa e se estão abertos ou mesclados.

Procure o PRD nos comentários. O comentário de PRD é o que começa exatamente com o cabeçalho `PRD - AAAA-MM-DD`. Se houver mais de um, vale o mais recente. Leia também os comentários feitos depois dele: são a revisão do time e podem ter mudado algum requisito.

Se a sessão não tiver ferramentas do Jira, avise que é preciso configurar o MCP do Jira (Atlassian) e pare.

### 2. Confira se a tarefa está pronta

Olhe primeiro os PRs da tarefa. O estado deles vale mais do que o status, que costuma ficar para trás. Sem a ferramenta de informações de desenvolvimento, pergunte à pessoa pelos PRs só quando a tarefa já estiver em andamento ou adiante.

| PRs da tarefa | O que fazer |
| --- | --- |
| Há pelo menos um PR, e todos estão mesclados | O desenvolvimento acabou. Confirme com a pessoa que não falta nada e vá direto para o passo 7, para oferecer o próximo status. Vale para qualquer status que não seja o de concluída, mesmo um de pendente. |
| Há PR aberto, mesmo que outro esteja mesclado ou fechado | Costuma ser um ajuste pedido na revisão. Siga para o passo 3 e retome o trabalho na branch da tarefa. Se a tarefa ainda não está no status de revisão, ofereça também o comentário e a mudança de status do passo 7. |
| Há PR fechado sem merge | Não conta como aberto nem como mesclado. Mostre à pessoa e pergunte o que ela quer fazer. |

Se nenhuma linha acima se aplica, vale o status:

| Situação | O que fazer |
| --- | --- |
| Status "PRD aprovado" | Siga. O PRD é a fonte dos requisitos. Se o status diz que há PRD e você não achou o comentário, pergunte onde ele está antes de seguir. |
| Status "PRD em revisão" | Avise que o time ainda não aprovou o PRD e que os requisitos podem mudar. Siga só se a pessoa confirmar. |
| Status "Refinado", sem PRD | Siga quando a descrição basta para desenvolver, como em correção de bug, ajuste pequeno ou tarefa técnica. Se a tarefa muda regra de negócio ou comportamento que o usuário percebe, sugira gerar o PRD antes, com a skill `gerar-prd` se ela estiver instalada, e deixe a pessoa decidir. |
| Ainda não refinada, ou com a descrição vazia | Diga que falta refinar e sugira a skill `refinar-tarefa`, se estiver instalada. Desenvolver em cima de uma tarefa vaga é a principal causa de entrega errada. Siga só se a pessoa insistir. |
| Em andamento | Pode ser trabalho retomado. Siga para o passo 3 e veja se já existe plano desta tarefa no repositório. |
| Na espera de deploy | Pergunte se a mudança já está em produção e vá para o passo 7. |
| Concluída, ou em um status que não está nesta tabela | Avise e pergunte o que a pessoa quer fazer. |

Diga em poucas frases o que você entendeu da tarefa e de onde veio cada informação: descrição, PRD ou comentários.

### 3. Prepare o repositório

- Confirme que a pasta atual é um repositório git e que é o projeto que a tarefa altera. Se não der para saber, pergunte.
- Confira se a skill `tlc-spec-lean` está disponível na sessão. Se não estiver, avise que ela é instalada pelo `/setup` do repositório de ferramentas do time e pare.
- Veja se já existe trabalho desta tarefa em `.specs/features/`. Se existir, o trabalho está sendo retomado: siga o lean a partir de onde os arquivos e o `git log` mostram que ele parou, em vez de planejar de novo.
- Se a pasta da tarefa tem `spec.md` ou `tasks.md` em vez de `plan.md`, ela foi começada com o `tlc-spec-driven`, que o time usava antes. Os formatos não se convertem: mostre isso à pessoa e pergunte se ela quer terminar à mão o que falta ou recomeçar a tarefa pelo lean.
- Olhe o `git status`. Se houver mudanças pendentes que não são desta tarefa, ou se a branch atual for de outra tarefa, mostre isso e pergunte como seguir. Não misture nem descarte o trabalho que já está lá.
- Não trabalhe direto na branch principal. Se a pessoa ainda está nela, crie uma branch seguindo a convenção do repositório. Se o repositório não define uma, use a chave da tarefa no nome, como `feat/ABC-123-resumo-curto`.
- Se a tarefa ainda não está em andamento nem em revisão, ofereça mover a tarefa no Jira para o status de em andamento. Só mova com aceite explícito, como em toda escrita no Jira (passo 7).

### 4. Entregue a tarefa ao lean

Carregue a skill `tlc-spec-lean` e siga as instruções dela a partir daqui. Ela tem três fases:

| Fase | O que acontece | Onde a pessoa decide |
| --- | --- | --- |
| Plano | O pedido é salvo, as decisões de produto que faltam são perguntadas e o plano é escrito: problema, caminho pelo código, decisões difíceis de reverter e critérios de aceite por fatia. | Responde às perguntas e aprova o plano. É a única parada obrigatória. |
| Build | Uma fatia por vez, de ponta a ponta, com os testes dela e um commit por fatia. | Só se aparecer uma decisão que o plano não previu. |
| Revisão | Um subagente que não escreveu o código confere o pedido e o plano contra o que foi feito. Depois vem uma única rodada de correção. | Decide os achados que forem de produto. |

Mudança pequena, de menos de três arquivos, mais ou menos, e sem decisão difícil de reverter, dispensa o plano: as respostas vão para o `request.md`, e a revisão acontece do mesmo jeito. Você decide, pelo critério do lean, e diz à pessoa que dispensou o plano.

**O pedido.** O `request.md` do lean guarda o pedido como ele veio. Aqui o pedido é a tarefa do Jira: grave nele a chave, o link, o título, a descrição, o comentário de PRD e os comentários posteriores que mudem algum requisito, sem resumir nem reescrever, além do que a pessoa disse na conversa. A exceção é dado sensível (dado de cliente, credencial, valor real de transação): esse fica de fora, com uma nota dizendo o que foi omitido. Se a tarefa tem tela, protótipo ou link de design anexado, liste cada um no `request.md`: para o lean, o que acompanha o pedido é o resultado esperado, e ele guarda as imagens em `captures/`. Use a chave no nome da pasta, como `.specs/features/abc-123-resumo-curto/`.

**O ponto de partida.** O que o time já decidiu entra no plano sem ser rediscutido:

- o problema, o objetivo e o escopo;
- o que está fora de escopo, que o lean deve respeitar como limite;
- os requisitos e os critérios de aceite. Se o PRD numera os requisitos (`R1`, `R2`...), cite o número em cada critério do plano, para o time conseguir rastrear do PRD ao código;
- as perguntas em aberto do PRD, que viram as primeiras perguntas do plano.

Não pergunte de novo o que a tarefa ou o PRD já respondem. As perguntas desta fase são as decisões de produto e as trocas que o PRD deixou de fora e que só aparecem quando se olha o código. O que dá para descobrir lendo o código, procure em vez de perguntar; e como o código será escrito é decisão do build, não pergunta para a pessoa.

**Dois cuidados que o time aprendeu usando.**

- Antes de fechar o plano, procure todos os lugares do código que usam o que a tarefa muda: quem chama o método, quem lê a configuração, quem depende do comportamento. A tarefa costuma citar um ou dois, e o código tem mais. Cada um entra no plano com um critério próprio, ou em "Out of scope" com o motivo.
- Cada critério ganha um teste que falharia se a regra estivesse errada, na camada em que a regra roda. Quando o teste nasce junto com o código, confira que ele falha sem a mudança antes de confiar nele.

**Os scripts.** O lean traz scripts em Python que conferem o plano e a mensagem de commit. Rode-os como a skill manda. Se a máquina não tiver Python 3 ou a execução for bloqueada, faça a mesma conferência por leitura, contra o modelo do plano, e diga no relatório final que o script não rodou.

**Os arquivos de `.specs/`.** Se o repositório do projeto já versiona a pasta, eles entram nos commits junto com o código. Se o repositório a ignora, ficam locais. Se ele não a ignora e ainda não tem nenhuma spec versionada, pergunte à pessoa antes do primeiro commit: abrir esse precedente é uma decisão do time daquele projeto. Se a resposta for não versionar, acrescente `.specs/` ao `.git/info/exclude` do repositório, que vale só na máquina dela, para a árvore ficar limpa sem mexer no `.gitignore` do projeto.

Converse com a pessoa em português, mesmo com as referências do lean em inglês. Nos arquivos de `.specs/`, os títulos de seção ficam em inglês, como o lean pede, e o texto segue o idioma que o projeto já usa na documentação; na dúvida, português.

### 5. Se a implementação divergir do PRD

O PRD é o que o time revisou. Quando o plano ou o build mostrar que um requisito não dá para cumprir como está escrito, ou que falta um requisito, pare e mostre a divergência à pessoa. Não mude o comportamento combinado em silêncio.

Se a pessoa decidir seguir de outro jeito, registre a decisão no plano, ou no `request.md` quando não houver plano, com as palavras dela, e inclua a divergência no comentário do passo 7.

### 6. Feche a entrega

Quando o build, a revisão e a rodada de correção do lean terminarem:

1. Rode a checagem de segurança com a skill `security-check`, se ela estiver instalada, sobre tudo o que a branch mudou em relação à principal: os arquivos de `git diff --name-only origin/<principal>...HEAD`. Não use o modo `diff` dela aqui. Ele olha só mudanças pendentes, e o lean já fez os commits, então o resultado viria vazio e pareceria uma aprovação.
2. Não peça outra revisão geral: a revisão do lean já foi feita por quem não escreveu o código. Chame o agent `revisor-de-codigo` só se a pessoa pedir. Se a revisão do lean não rodou por falta de subagentes, siga o que o lean manda nesse caso: rode o prompt de revisão em uma sessão nova ou entregue-o à pessoa, e diga isso no relatório. Os achados que a pessoa decidir não corrigir vão para os pontos de atenção da descrição do PR.
3. Escreva a descrição do PR com a skill `descricao-de-pr`, se estiver instalada, incluindo o link da tarefa.

Quando uma dessas ferramentas não estiver instalada, diga qual etapa ficou de fora, em vez de pular sem avisar.

Com o kit de orquestração instalado, a trava de revisão pode impedir o encerramento uma vez, pedindo um `revisor`, porque o revisor do lean é um subagente e grava o `review.md`. É esperado. Se ele só gravou o parecer, diga à pessoa que aquele subagente era o próprio revisor e encerre de novo.

Só faça push e abra o PR se a pessoa pedir.

### 7. Atualize o Jira, só com aceite

Escrever no Jira é uma ação visível para o time. Proponha e só faça depois de um aceite explícito:

- **No começo do trabalho:** a mudança para o status de em andamento, oferecida no passo 3.
- **Quando o PR for aberto:** ofereça um comentário curto com o link do PR, o que foi entregue e as divergências em relação ao PRD, se houver. Na mesma proposta, ofereça mover a tarefa para o status de revisão, como "EM REVIEW". Se a tarefa tem PR em mais de um repositório, liste todos no comentário e diga em que ordem devem ser mesclados, se a ordem importar. Vale também quando a pessoa abriu o PR por conta própria e a tarefa ainda não está em revisão.
- **Depois do merge:** ofereça mover a tarefa para o status de espera de deploy, como "AGUARDANDO DEPLOY", quando todos os PRs dela estiverem mesclados e ela ainda não estiver nesse status. Um PR ainda aberto segura a tarefa em revisão.
- **Concluída:** quando todos os PRs estiverem mesclados, ou a tarefa já estiver na espera de deploy, pergunte se a mudança já está em produção. Só ofereça mover para o status de concluído depois de a pessoa confirmar. PR mesclado não é deploy.

Para saber em que ponto os PRs estão, consulte as informações de desenvolvimento da tarefa no Jira, se a sessão tiver essa ferramenta. Se não tiver, pergunte à pessoa.

O merge quase sempre acontece dias depois, fora desta sessão, e nenhuma skill enxerga esse momento. Por isso, se a sessão terminar com o PR aberto, ou sem PR porque a pessoa não pediu para abrir, diga em uma frase em que status a tarefa ficou e o que falta para ela andar: mover à mão depois do merge ou chamar esta skill de novo com a mesma chave. O mesmo vale para a tarefa que ficou na espera de deploy: ela só vira concluída quando alguém mover depois do deploy. Não deixe a pessoa achar que a tarefa fecha sozinha.

Não mude a descrição, o PRD nem o responsável. Os nomes de status mudam de projeto para projeto: use o que o Jira oferecer como transição para aquele momento. Se o Jira não oferecer a transição, não mova para outro status: avise que a tarefa precisa ser movida à mão.

## Regras

- **O que já foi decidido não se rediscute.** Problema, escopo e requisitos vêm da tarefa e do PRD. Esta etapa decide como fazer.
- **Nada inventado.** Se a tarefa não responde e a pessoa não sabe, vira pergunta registrada na especificação, não suposição.
- **Uma tarefa por vez.** Não misture duas tarefas do Jira na mesma branch nem na mesma especificação.
- **Sem dado sensível.** Não leve dados de clientes, credenciais nem valores reais de transações do Jira para a especificação, para os testes ou para os commits.
- **As convenções do projeto mandam.** Regras de commit, de branch e de teste do repositório valem mais do que os padrões do lean e desta skill.
