---
name: refinar-tarefa
description: Refina uma tarefa do Jira que está com pouca informação. Lê a tarefa, diz o que entendeu, tira as dúvidas com quem pediu e reescreve a descrição com resumo, o que precisa ser feito, como deve funcionar e critérios de aceite. Depois do aceite, grava no Jira e move a tarefa para Refinado. Use quando alguém pedir para refinar, detalhar ou enriquecer uma tarefa do Jira.
argument-hint: "[chave ou link da tarefa]"
---

# Refinar tarefa

Tarefa a refinar: $ARGUMENTS

Quem usa esta skill é o pessoal de produto e de projetos do time Jornada Inicial. As tarefas costumam nascer no Jira com um título e uma ou duas frases, e quem desenvolve parte desse texto para escrever a especificação e o código, muitas vezes com ajuda de IA. Uma tarefa vaga vira entrega errada ou retrabalho.

O seu papel é conversar com quem conhece a demanda até a descrição dizer o que precisa ser feito, como deve funcionar e como saber que terminou, e então gravar essa descrição no Jira e mover a tarefa para "Refinado".

A conversa é sobre produto e regra de negócio. Não investigue código e não proponha solução técnica: isso fica para a etapa seguinte, com quem desenvolve.

## Passo a passo

### 1. Busque a tarefa no Jira

A tarefa sempre vem do Jira. A pessoa pode informar a chave (como `ABC-123`) ou colar o link da tarefa; no caso do link, tire a chave dele. Se não veio nenhum dos dois, peça.

Leia o título, a descrição, os comentários, a tarefa pai ou o épico e as tarefas ligadas. Os comentários costumam ter decisões que não foram para a descrição.

Se a sessão não tiver ferramentas do Jira, avise que é preciso configurar o MCP do Jira (Atlassian) e pare. Não refine a partir de texto colado na conversa.

### 2. Diga o que você entendeu

Antes de perguntar qualquer coisa, explique em poucas frases o que você entendeu: o que a tarefa pede, para quem e por quê. Deixe claro o que está escrito na tarefa, o que é dedução sua e o que está faltando.

Peça para a pessoa confirmar ou corrigir. Ela pode aproveitar para dizer o que acha que a tarefa deveria ser; trate isso como informação dela, com o mesmo peso do que está no Jira.

### 3. Tire as dúvidas

Liste as perguntas de uma vez, numeradas e curtas.

- Pergunte só o que muda a descrição. O que a tarefa ou os comentários já respondem não vira pergunta.
- Pergunta aberta vale. Se a tarefa não diz como a coisa deve se comportar, "como isso deve funcionar?" é a pergunta certa: quem está refinando é quem sabe o que se espera.
- Quando você perceber um caso que a tarefa não cobre (erro, falta de permissão, lista vazia, dado antigo), pergunte por ele de forma específica.

Espere as respostas. Se elas abrirem dúvidas novas, pergunte de novo.

Toda pergunta que impede o desenvolvimento precisa ser resolvida antes de a tarefa ser considerada pronta. Se a pessoa não souber responder, diga que a tarefa ainda não está pronta e o que falta descobrir. Se ela quiser gravar mesmo assim, inclua as perguntas na seção "Pendências" da descrição.

### 4. Mostre como a descrição ficou

Mostre a descrição na conversa como texto formatado, e não dentro de um bloco de código, com o título da tarefa no topo. Diga em uma frase se ela está pronta para desenvolvimento ou o que ainda falta.

Pergunte se pode gravar no Jira, avisando que a tarefa também vai para a coluna "Refinado" quando estiver pronta. Se a pessoa pedir ajustes, ajuste e mostre de novo.

### 5. Grave no Jira depois do aceite

Só grave quando a pessoa aceitar de forma explícita.

- Substitua a descrição pela nova, mantendo os links, prints e anexos que a descrição original citava.
- Se a tarefa está pronta para desenvolvimento, mova para o status "Refinado". Se foi gravada com pendências, deixe no status em que está e diga isso: ela só vai para "Refinado" quando as pendências forem resolvidas.
- Se o Jira não oferecer a transição para "Refinado", não mova para outro status. Avise que a descrição foi gravada e que a tarefa precisa ser movida à mão.
- Título, responsável e os outros campos ficam como estão.
- Depois de gravar, confirme com a chave da tarefa e o status em que ela ficou.

## Estrutura da descrição

O título é o que a tarefa já tem no Jira. Ele não muda e não se repete dentro da descrição.

| Seção | Conteúdo |
| --- | --- |
| **Resumo** | De uma a três frases: o que muda e por quê. |
| **O que precisa ser feito** | Texto corrido descrevendo a entrega. |
| **Como deve funcionar** | O comportamento esperado do ponto de vista de quem usa, incluindo os casos de erro que a pessoa definiu. Entra só quando acrescenta algo à seção anterior. |
| **Critérios de aceite** | Lista de afirmações que uma pessoa ou um teste consegue verificar como verdadeiras ou falsas. |
| **Sugestão de quebra** | Só quando a tarefa junta entregas que podem sair separadas: a lista das tarefas menores. |
| **Pendências** | Só quando a pessoa decidiu gravar com perguntas sem resposta. |

Deixe de fora a seção que ficar vazia.

## Regras de escrita

- **Nada inventado.** Toda informação da descrição vem da tarefa, dos comentários ou das respostas de quem está refinando. Se algo é dedução sua, confirme na conversa antes de colocar na descrição.
- **Sem enchimento.** Cada frase precisa dizer a quem vai desenvolver algo que essa pessoa precisa saber. Não escreva introdução, conclusão, lista de benefícios, "considerações" nem frase que só repete o título. Não use emojis. Tarefa simples tem descrição curta.
- **Critérios verificáveis.** "A tela deve ser rápida" não serve. "A listagem carrega em até 2 segundos com 1.000 registros" serve, desde que o número tenha vindo de quem está refinando.
- **Tamanho de tarefa, não de documento.** A especificação detalhada vem em outra etapa. A descrição deve ser entendida em uma leitura.
- **Português**, com frases completas e os termos que o time já usa na tarefa.
