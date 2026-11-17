---
name: gerar-prd
description: Gera o PRD de uma tarefa do Jira que já foi refinada. Lê a tarefa, avalia se ela precisa de PRD, tira as dúvidas com quem pediu, escreve o documento e, depois do aceite, grava como comentário na tarefa e move para "PRD em revisão". Use quando alguém pedir para gerar, escrever ou atualizar o PRD de uma tarefa do Jira.
argument-hint: "[chave ou link da tarefa]"
---

# Gerar PRD

Tarefa: $ARGUMENTS

O PRD é o passo entre a tarefa refinada e a especificação técnica. A tarefa refinada diz o que precisa ser feito em poucas linhas; o PRD abre isso em requisitos que o time consegue revisar antes de alguém escrever código. Ele fica na própria tarefa do Jira, como comentário, para que a revisão aconteça onde o time já trabalha.

O PRD fala do problema, de quem é afetado e do comportamento esperado. Ele não escolhe solução técnica, não desenha arquitetura e não quebra o trabalho em tarefas: isso é da etapa seguinte. Um PRD que já decide a implementação tira do time a chance de revisar o que importa nesta etapa, que é se o problema e os requisitos estão certos.

## Passo a passo

### 1. Busque a tarefa no Jira

A pessoa pode informar a chave (como `ABC-123`) ou colar o link; no caso do link, tire a chave dele. Se não veio nenhum dos dois, peça.

Leia o título, a descrição, o status, os comentários, a tarefa pai ou o épico e as tarefas ligadas. Se a descrição tiver as seções "Como deve funcionar", "Sugestão de quebra" ou "Pendências", elas são entrada do PRD: as pendências viram perguntas no passo 4.

Se a sessão não tiver ferramentas do Jira, avise que é preciso configurar o MCP do Jira (Atlassian) e pare.

### 2. Avalie se a tarefa precisa de PRD

Nem toda tarefa precisa. Faça esta avaliação antes de qualquer outra, para não pedir refinamento de uma tarefa que nem vai ter PRD.

| Situação | Recomendação |
| --- | --- |
| Funcionalidade nova, mudança de regra de negócio ou de comportamento que alguém de fora do time percebe | PRD. |
| Correção de bug ou ajuste em que a descrição já diz tudo o que há para dizer | Sem PRD. A descrição refinada basta. |
| Investigação ou trabalho técnico sem mudança de comportamento, como reduzir conexões, migrar versão ou melhorar desempenho | Sem PRD. O que essa tarefa pede é uma especificação técnica, que vem na etapa seguinte. |

Se a recomendação for não gerar, diga isso em uma frase com o motivo e pare, sem gravar nada no Jira. A recomendação é sua, mas a decisão é de quem pediu: se a pessoa disser que quer o PRD mesmo assim, siga.

### 3. Confira o status e os PRDs anteriores

O status da tarefa define se você pode seguir e se a tarefa muda de status no passo 6.

| Status da tarefa | O que fazer | Move para "PRD em revisão"? |
| --- | --- | --- |
| "Refinado" | Siga. | Sim. |
| Ainda não refinada, ou com a descrição vazia | Diga que o PRD parte de uma tarefa refinada e sugira refinar antes, com a skill `refinar-tarefa` se ela estiver instalada. Um PRD escrito sobre uma tarefa vaga só espalha a incerteza por mais páginas. Se a pessoa quiser seguir mesmo assim, siga, e trate as lacunas como perguntas no passo 4. | Não. A tarefa não passou pelo refinamento. |
| "PRD em revisão" | Você está escrevendo uma nova versão do PRD. | Não, ela já está lá. |
| "PRD aprovado" | Avise que o time já aprovou o PRD e pergunte se a pessoa quer mesmo uma nova versão. Se quiser, siga. | Não. Desfazer uma aprovação é decisão do time, e a tarefa é movida à mão. |
| Em andamento, concluída ou qualquer outro | Avise que o trabalho já começou e pergunte se o PRD ainda faz sentido. Se a pessoa confirmar, siga. | Não. |

Depois procure um PRD anterior nos comentários. O comentário de PRD é o que começa exatamente com o cabeçalho `PRD - AAAA-MM-DD`; um comentário que só menciona a palavra PRD não conta. Se houver mais de um, vale o mais recente. Se você ficar em dúvida sobre qual comentário é o PRD, pergunte.

Quando existe um PRD anterior, leia também os comentários feitos depois dele. Eles são a revisão do time, e cada apontamento é entrada para a nova versão.

### 4. Diga o que entendeu e tire as dúvidas

Explique em poucas frases o problema, quem é afetado e o que muda. Separe o que está escrito na tarefa do que é dedução sua.

Depois liste as perguntas de uma vez, numeradas e curtas. Pergunte só o que muda o PRD:

- quem usa e em que situação, quando a tarefa não diz;
- o que fica de fora, porque escopo aberto é a principal causa de retrabalho;
- casos que a tarefa não cobre, como erro, falta de permissão, dado ausente e o que acontece com o que já existe;
- como o time vai saber que funcionou, quando os critérios de aceite não bastam.

Espere as respostas. Se elas abrirem dúvidas novas, pergunte de novo. O que ficar sem resposta vai para "Perguntas em aberto", nunca vira suposição escrita como fato.

Se o Claude Code estiver aberto no repositório do projeto que a tarefa altera, você pode ler o código para entender como a funcionalidade se comporta hoje. Use isso para descrever o estado atual e para fazer perguntas melhores. Não use para propor a solução.

### 5. Mostre o PRD

Mostre o PRD na conversa como texto formatado, e não dentro de um bloco de código. Diga em uma frase se ele está pronto para revisão ou o que ainda falta.

Pergunte se pode gravar no Jira e diga exatamente o que vai acontecer: que o PRD entra como um comentário novo na tarefa e, conforme a tabela do passo 3, se a tarefa vai para "PRD em revisão" ou fica no status em que está. Se a pessoa pedir ajustes, ajuste e mostre de novo.

### 6. Grave no Jira depois do aceite

Só grave quando a pessoa aceitar de forma explícita.

- **Sempre um comentário novo.** Nunca edite nem apague um comentário existente, nem o do PRD anterior: ele pode ser de outra pessoa, e é a versão que o time revisou. Quando houver PRD anterior, diga logo abaixo do cabeçalho que esta versão substitui a de tal data.
- **Formato.** Escreva o comentário em Markdown, com um título por seção.
- **Status.** Mova para "PRD em revisão" só quando a tabela do passo 3 disser que sim. Se o Jira não oferecer essa transição, não mova para outro status: avise que o PRD foi gravado e que a tarefa precisa ser movida à mão.
- **Perguntas em aberto não seguram a tarefa.** O PRD vai para revisão mesmo com perguntas sem resposta, porque a revisão é o lugar de respondê-las. Destaque-as na confirmação.
- **Aprovação.** Quem move para "PRD aprovado" é o time, depois de revisar. Esta skill nunca faz essa transição.
- A descrição, o título, o responsável e os outros campos ficam como estão.

Depois de gravar, confirme com a chave da tarefa, o status em que ela ficou e as perguntas em aberto, se houver.

## Estrutura do PRD

A primeira linha do comentário é o cabeçalho `PRD - AAAA-MM-DD`, com a data de hoje. É por ele que o time e esta skill acham o documento entre os outros comentários, então não mude o formato.

| Seção | Conteúdo |
| --- | --- |
| **Problema** | O que acontece hoje, quem sente e por que vale resolver agora. De um a três parágrafos. |
| **Objetivo** | O resultado esperado, em uma ou duas frases. Com número, quando quem pediu deu o número. |
| **Quem é afetado** | Os perfis de usuário ou os sistemas que percebem a mudança e o que muda para cada um. |
| **Escopo** | O que esta entrega inclui. |
| **Fora de escopo** | O que alguém poderia esperar e não entra, com o motivo quando houver. |
| **Requisitos** | Lista numerada (`R1`, `R2`...). Cada item descreve um comportamento que dá para verificar, incluindo os casos de erro definidos na conversa. |
| **Critérios de aceite** | Os critérios da tarefa refinada, mais os que surgiram na conversa, cada um apontando o requisito que ele verifica. Se um critério da tarefa não corresponde a nenhum requisito, falta um requisito: escreva-o ou pergunte. |
| **Riscos, dependências e restrições** | O que pode atrapalhar a entrega, do que ou de quem ela depende e as restrições que já vieram da tarefa. |
| **Perguntas em aberto** | O que ficou sem resposta e quem pode responder. |

Deixe de fora a seção que ficar vazia, menos "Fora de escopo": se não houver nada, escreva isso, para o time saber que a pergunta foi feita.

## Regras de escrita

- **Nada inventado.** Toda informação vem da tarefa, dos comentários, do código lido ou das respostas de quem pediu. Dedução sua só entra depois de confirmada na conversa.
- **Sem solução técnica.** Nada de nome de tabela, endpoint, biblioteca ou padrão de arquitetura, a não ser que seja uma restrição que já veio da tarefa. Nesse caso, registre em "Riscos, dependências e restrições".
- **Requisitos verificáveis.** "O sistema deve ser rápido" não serve. "A listagem carrega em até 2 segundos com 1.000 registros" serve, desde que o número tenha vindo de quem pediu.
- **Tamanho proporcional.** O PRD precisa caber em uma leitura de poucos minutos. Se passar de umas duas páginas, a tarefa provavelmente junta entregas que deveriam ser separadas: diga isso e sugira a quebra.
- **Sem dado sensível.** O comentário fica visível para quem acessa a tarefa. Não coloque dados de clientes, credenciais nem valores reais de transações; use exemplos fictícios.
- **Sem enchimento.** Não escreva introdução, conclusão, lista de benefícios nem frase que só repete o título. Não use emojis.
- **Português**, com frases completas e os termos que o time já usa na tarefa.
