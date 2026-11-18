---
name: desenvolver-tarefa
description: Desenvolve uma tarefa do Jira seguindo o fluxo spec-driven do time. Lê a tarefa e o PRD, confere se ela está pronta, prepara o repositório do projeto e conduz a especificação e a implementação com a skill tlc-spec-driven, fechando com checagem de segurança, revisão e descrição do PR. Use quando alguém pedir para desenvolver, implementar ou começar uma tarefa do Jira.
argument-hint: "[chave ou link da tarefa]"
---

# Desenvolver tarefa

Tarefa: $ARGUMENTS

Esta skill é a ponte entre o Jira e o desenvolvimento. O time refina a tarefa e, quando faz sentido, escreve o PRD na própria tarefa. A partir daí, quem desenvolve usa o TLC Spec-Driven (skill `tlc-spec-driven`) para especificar, desenhar, quebrar em passos e implementar.

O TLC é completo, mas é em inglês, tem muitos comandos e não conhece o Jira. O seu papel aqui é poupar a pessoa disso: você busca o que já foi decidido na tarefa, entrega ao TLC como ponto de partida e conduz as fases em português. A pessoa não precisa decorar comando nenhum.

Esta skill roda no repositório do projeto que a tarefa altera, não no repositório de ferramentas do time.

## Passo a passo

### 1. Busque a tarefa no Jira

A pessoa pode informar a chave (como `ABC-123`) ou colar o link; no caso do link, tire a chave dele. Se não veio nenhum dos dois, peça.

Leia o título, a descrição, o status, os comentários, a tarefa pai ou o épico e as tarefas ligadas.

Procure o PRD nos comentários. O comentário de PRD é o que começa exatamente com o cabeçalho `PRD - AAAA-MM-DD`. Se houver mais de um, vale o mais recente. Leia também os comentários feitos depois dele: são a revisão do time e podem ter mudado algum requisito.

Se a sessão não tiver ferramentas do Jira, avise que é preciso configurar o MCP do Jira (Atlassian) e pare.

### 2. Confira se a tarefa está pronta

| Situação | O que fazer |
| --- | --- |
| Status "PRD aprovado" | Siga. O PRD é a fonte dos requisitos. Se o status diz que há PRD e você não achou o comentário, pergunte onde ele está antes de seguir. |
| Status "PRD em revisão" | Avise que o time ainda não aprovou o PRD e que os requisitos podem mudar. Siga só se a pessoa confirmar. |
| Status "Refinado", sem PRD | Siga quando a descrição basta para desenvolver, como em correção de bug, ajuste pequeno ou tarefa técnica. Se a tarefa muda regra de negócio ou comportamento que o usuário percebe, sugira gerar o PRD antes, com a skill `gerar-prd` se ela estiver instalada, e deixe a pessoa decidir. |
| Ainda não refinada, ou com a descrição vazia | Diga que falta refinar e sugira a skill `refinar-tarefa`, se estiver instalada. Desenvolver em cima de uma tarefa vaga é a principal causa de entrega errada. Siga só se a pessoa insistir. |
| Em andamento | Pode ser trabalho retomado. Siga para o passo 3 e veja se já existe especificação no repositório. |
| Concluída, ou em um status que não está nesta tabela | Avise e pergunte o que a pessoa quer fazer. |

Diga em poucas frases o que você entendeu da tarefa e de onde veio cada informação: descrição, PRD ou comentários.

### 3. Prepare o repositório

- Confirme que a pasta atual é um repositório git e que é o projeto que a tarefa altera. Se não der para saber, pergunte.
- Confira se a skill `tlc-spec-driven` está disponível na sessão. Se não estiver, avise que ela é instalada pelo `/setup` do repositório de ferramentas do time e pare.
- Veja se já existe trabalho desta tarefa em `.specs/features/` ou em `.specs/quick/`. Se existir, o trabalho está sendo retomado: siga o TLC a partir de onde parou, em vez de especificar de novo.
- Olhe o `git status`. Se houver mudanças pendentes que não são desta tarefa, ou se a branch atual for de outra tarefa, mostre isso e pergunte como seguir. Não misture nem descarte o trabalho que já está lá.
- Não trabalhe direto na branch principal. Se a pessoa ainda está nela, crie uma branch seguindo a convenção do repositório. Se o repositório não define uma, use a chave da tarefa no nome, como `feat/ABC-123-resumo-curto`.
- Se o projeto ainda não tem `.specs/codebase/`, explique que o TLC consegue mapear o código existente uma vez, que isso melhora as especificações seguintes e que leva alguns minutos. Pergunte se a pessoa quer fazer agora. Não é obrigatório.
- Ofereça mover a tarefa no Jira para o status de em andamento. Só mova com aceite explícito, como em toda escrita no Jira (passo 7).

### 4. Entregue a tarefa ao TLC

Carregue a skill `tlc-spec-driven` e siga as instruções dela a partir daqui. Quem decide a profundidade é o TLC, pelo tamanho da mudança: de uma tarefa pequena direto no modo rápido até o fluxo completo com desenho e quebra em passos.

Entregue como ponto de partida o que o time já decidiu:

- o problema, o objetivo e o escopo;
- o que está fora de escopo, que o TLC deve respeitar como limite;
- os requisitos e os critérios de aceite. Se o PRD numera os requisitos (`R1`, `R2`...), mantenha a correspondência na especificação, para o time conseguir rastrear do PRD ao código;
- as perguntas em aberto do PRD, que são o ponto de partida da discussão de áreas cinzentas do TLC.

Não pergunte de novo o que a tarefa ou o PRD já respondem. As perguntas desta fase são as técnicas, que o PRD deixou de fora de propósito.

Registre a chave e o link da tarefa do Jira onde o TLC guardar o trabalho, e use a chave no nome da pasta:

- no fluxo com especificação, no topo do `spec.md`, em uma pasta como `.specs/features/abc-123-resumo-curto/`;
- no modo rápido, no `TASK.md`, mantendo a numeração do TLC e incluindo a chave no resto do nome, como `.specs/quick/NNN-abc-123-resumo-curto/`.

Os arquivos de `.specs/` entram nos commits junto com o código, a menos que o repositório do projeto os ignore.

Converse com a pessoa em português, mesmo com as referências do TLC em inglês. Os arquivos em `.specs/` seguem o idioma que o projeto já usa na documentação; na dúvida, português.

### 5. Se a implementação divergir do PRD

O PRD é o que o time revisou. Quando o desenho ou a implementação mostrar que um requisito não dá para cumprir como está escrito, ou que falta um requisito, pare e mostre a divergência à pessoa. Não mude o comportamento combinado em silêncio.

Se a pessoa decidir seguir de outro jeito, registre a decisão na especificação e inclua a divergência no comentário do passo 7.

### 6. Feche a entrega

Quando a implementação e a verificação do TLC terminarem:

1. Rode a checagem de segurança com a skill `security-check`, se ela estiver instalada, sobre tudo o que a branch mudou em relação à principal: os arquivos de `git diff --name-only origin/<principal>...HEAD`. Não use o modo `diff` dela aqui. Ele olha só mudanças pendentes, e o TLC já fez os commits, então o resultado viria vazio e pareceria uma aprovação.
2. Peça a revisão do agent `revisor-de-codigo`, se ele estiver disponível. Corrija o que ele apontar como necessário antes de seguir. As sugestões que a pessoa decidir não aplicar vão para os pontos de atenção da descrição do PR.
3. Escreva a descrição do PR com a skill `descricao-de-pr`, se estiver instalada, incluindo o link da tarefa.

Quando uma dessas ferramentas não estiver instalada, diga qual etapa ficou de fora, em vez de pular sem avisar.

Só faça push e abra o PR se a pessoa pedir.

### 7. Atualize o Jira, só com aceite

Escrever no Jira é uma ação visível para o time. Proponha e só faça depois de um aceite explícito:

- **No começo do trabalho:** a mudança para o status de em andamento, oferecida no passo 3.
- **No fim:** ofereça um comentário curto com o link do PR, o que foi entregue e as divergências em relação ao PRD, se houver.

Não mude a descrição, o PRD nem o responsável. Se o Jira não oferecer a transição, não mova para outro status: avise que a tarefa precisa ser movida à mão.

## Regras

- **O que já foi decidido não se rediscute.** Problema, escopo e requisitos vêm da tarefa e do PRD. Esta etapa decide como fazer.
- **Nada inventado.** Se a tarefa não responde e a pessoa não sabe, vira pergunta registrada na especificação, não suposição.
- **Uma tarefa por vez.** Não misture duas tarefas do Jira na mesma branch nem na mesma especificação.
- **Sem dado sensível.** Não leve dados de clientes, credenciais nem valores reais de transações do Jira para a especificação, para os testes ou para os commits.
- **As convenções do projeto mandam.** Regras de commit, de branch e de teste do repositório valem mais do que os padrões do TLC e desta skill.
