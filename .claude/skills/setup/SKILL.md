---
name: setup
description: Prepara a máquina de quem vai usar as ferramentas deste repositório. Verifica o que falta, copia os agents e as skills para a pasta pessoal do Claude Code, configura o MCP do Jira e oferece o kit de orquestração, que é opcional. Rode com /setup para instalar, configurar ou atualizar as ferramentas do time.
disable-model-invocation: true
---

# Setup

Quem roda esta skill pode ser de produto ou de projetos e não ter familiaridade com terminal. Explique cada passo em linguagem simples, diga o que vai mudar na máquina antes de mudar e não peça para a pessoa rodar comandos que você mesmo consegue rodar.

O setup pode ser rodado quantas vezes for preciso. Rodar de novo serve para atualizar as cópias depois de um `git pull`.

## Passo a passo

### 1. Confirme que está no repositório

Esta skill só funciona na raiz do `time-jornada-inicial-tools`, porque copia os arquivos a partir dele. Confira que `.claude/skills/setup/checar.sh` existe na pasta atual. Se não existir, avise que o Claude Code precisa ser aberto na pasta do repositório e pare.

### 2. Verifique o que falta

Rode o script de verificação. Ele não instala nem altera nada, mas pode levar alguns segundos: para testar a conexão, o Claude Code inicia os servidores MCP que a pessoa já tem configurados.

```bash
bash .claude/skills/setup/checar.sh
```

Cada linha da saída é um item:

| Linha | Significado |
| --- | --- |
| `agent faltando` ou `skill faltando` | Ainda não está na pasta pessoal. |
| `agent igual` ou `skill igual` | Já está instalado e atualizado. |
| `agent diferente` ou `skill diferente` | Existe na pasta pessoal, mas com conteúdo diferente do repositório. |
| `mcp oficial` | O MCP oficial da Atlassian já está configurado. |
| `mcp outro` | Existe outro servidor MCP com "atlassian" ou "jira" no nome ou no comando, como o `mcp-atlassian`. |
| `mcp faltando` | Não há MCP de Jira. |
| `mcp erro` | Não foi possível listar os servidores MCP. O resto da linha traz o erro. |
| `mcp sem-cli` | O comando `claude` não existe no terminal, então não dá para verificar nem configurar por aqui. |

Nas linhas `mcp oficial` e `mcp outro`, o resto da linha é o que o Claude Code informou sobre o servidor: conectado, pedindo autenticação ou com falha de conexão.

A pasta pessoal é a que estiver em `CLAUDE_CONFIG_DIR` ou, se a variável não existir, `~/.claude`. Descubra qual é com `echo "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"` e use esse caminho em todos os passos seguintes.

### 3. Mostre o resumo e peça o aceite

Mostre uma tabela curta com o que já está pronto e o que será feito.

Não há nada a fazer quando todos os agents e skills estão `igual` e o MCP é `oficial` conectado, `outro` conectado ou `sem-cli`. Nesse caso, diga isso e pule para o passo 6, que oferece o kit de orquestração. No `sem-cli`, o resumo do passo 7 precisa dizer que o MCP não foi verificado.

Nos outros casos, só siga depois que a pessoa aceitar. O setup grava fora do repositório, na pasta pessoal dela, e ela precisa saber disso antes.

### 4. Copie os agents e as skills

- **Faltando:** copie. Agents vão para `agents/` da pasta pessoal e cada pasta de skill vai inteira para `skills/`. Crie as pastas se não existirem.
- **Igual:** não faça nada.
- **Diferente:** mostre o que muda com `diff -ru -x .DS_Store -x .skill-meta.json <pasta pessoal> <repositório>` e explique que as linhas com `-` são as da cópia da pessoa e as com `+` são as do repositório. Pergunte, item por item, se pode substituir. A diferença pode ser uma versão antiga, mas também pode ser um ajuste que a pessoa fez de propósito, e substituir apaga esse ajuste.

Para substituir uma skill, copie por cima com `cp -R <repositório>/. <pasta pessoal>/`. Não apague a pasta antes: ela pode ter arquivos que a pessoa criou e que não existem no repositório.

Não copie a skill `setup`. Fora deste repositório ela não tem de onde copiar.

### 5. Configure o MCP do Jira

- **`mcp oficial` conectado:** não faça nada.
- **`mcp oficial` pedindo autenticação:** siga para o login abaixo.
- **`mcp oficial` ou `mcp outro` com falha de conexão:** não adicione outro servidor. Mostre a linha que o script devolveu, diga que o MCP existe mas não está funcionando e oriente a pessoa a abrir o `/mcp` para ver o erro. Registre isso como pendência no resumo.
- **`mcp outro` conectado:** diga qual servidor foi encontrado e pergunte se a pessoa já usa o Jira por ele. O nome sozinho não garante: um servidor da Atlassian pode estar configurado só para o Confluence. Se ela usa, não faça nada, porque dois servidores de Jira na mesma sessão confundem a escolha das ferramentas. Se não usa ou não sabe, ofereça adicionar o oficial.
- **`mcp faltando`:** adicione o servidor oficial da Atlassian para todos os projetos da pessoa:

  ```bash
  claude mcp add --transport http --scope user atlassian https://mcp.atlassian.com/v2/mcp
  ```

- **`mcp erro`:** não adicione nada. Sem a listagem não dá para saber se já existe um MCP de Jira, e adicionar às cegas pode duplicar o servidor. Mostre o erro e registre como pendência.
- **`mcp sem-cli`:** não tente instalar o Claude Code. Diga que o MCP não foi verificado e que, se faltar, precisa ser adicionado pela tela de conectores do aplicativo que a pessoa usa, com o endereço `https://mcp.atlassian.com/v2/mcp`.

O login é feito pela própria pessoa, no navegador, com a conta Atlassian dela. O servidor oficial não usa token nem senha: nunca peça credenciais na conversa. Oriente assim:

1. Abrir o `claude` em um terminal.
2. Digitar `/mcp`, escolher `atlassian` e seguir para a autenticação.
3. Fazer o login no navegador e autorizar o acesso ao Jira da empresa.

Esses três passos valem para quem tem o comando `claude`. No caso `sem-cli`, o login acontece na mesma tela de conectores em que o servidor foi adicionado.

Um servidor recém-adicionado só aparece em uma sessão nova. Avise que é preciso fechar e abrir o Claude Code depois do setup.

### 6. Ofereça o kit de orquestração

O kit é opcional e é para quem desenvolve. Não ofereça a quem só vai refinar tarefas ou gerar PRD: para essa pessoa, diga em uma frase que ele existe e siga para o resumo.

Ele muda o jeito de o Claude Code trabalhar em todos os projetos da pessoa: a sessão principal passa a coordenar, e o trabalho mecânico vai para subagentes com modelos mais baratos (`varredor`, `pesquisador`, `executor` e `revisor`, copiados no passo 4). Além dos agents, o kit instala:

- uma regra em `rules/orquestracao.md`, que diz o que delegar e para quem;
- quatro hooks em `hooks/`. Um deles impede o Claude de encerrar a resposta, uma vez, quando um subagente editou arquivos e nenhum `revisor` conferiu;
- quatro entradas de hook e duas variáveis de ambiente no `settings.json` da pessoa, que fazem os subagentes usarem o Sonnet por padrão e os impedem de criar outros subagentes.

Veja o estado atual com o comando abaixo. Ele só lê.

```bash
python3 .claude/skills/setup/orquestracao.py checar
```

Trate estes casos antes de oferecer:

- **O `python3` não existe na máquina:** diga que o kit depende dele e pule este passo.
- **A saída traz `settings erro`:** o `settings.json` da pessoa está fora do formato esperado e o script não vai mexer nele. Mostre o erro, registre como pendência e pule este passo.
- **Tudo está `igual` e `ok`:** diga que o kit já está instalado e siga.
- **Algum dos agents `varredor`, `pesquisador`, `executor` ou `revisor` não ficou instalado no passo 4:** a regra e os hooks dependem deles. Diga isso e só ofereça o kit se a pessoa aceitar copiar os agents antes.

Explique o que muda com as palavras acima e pergunte se a pessoa quer instalar. Este é o único passo do setup que altera o `settings.json`, então o aceite precisa ser específico para ele: o aceite do passo 3 não vale aqui. Depois do aceite:

```bash
python3 .claude/skills/setup/orquestracao.py instalar
```

O comando termina com código 0 quando instalou tudo, 2 quando instalou mas manteve algum arquivo que a pessoa já tinha, e 1 quando nada foi alterado por causa de um erro. O código 2 não é falha.

Leia a saída e repasse o que importa:

- **`arquivo mantido`:** a pessoa já tinha esse arquivo com outro conteúdo, e ele não foi trocado. Se for um hook, a linha `config pulado` avisa que ele também não foi registrado no `settings.json`. O `--substituir` troca todos os arquivos mantidos de uma vez, então antes mostre a diferença de cada um com `diff -u <pasta pessoal>/<arquivo> .claude/skills/setup/orquestracao/<arquivo>` e peça o aceite. Se a pessoa quiser manter algum deles, não rode o `--substituir`: diga que o kit ficou parcial e quais partes ficaram de fora.
- **`env mantido`:** a variável já existia com outro valor e não foi alterada. Diga qual valor ficou e qual o kit sugere, e deixe a decisão com a pessoa.
- **`copia`:** o caminho da cópia do `settings.json` feita antes da alteração. Informe no resumo.
- **`settings erro`:** nada foi alterado. Mostre o erro e registre como pendência.

Não edite o `settings.json` à mão para completar o que o script não fez. Para desfazer a instalação, o comando é `python3 .claude/skills/setup/orquestracao.py remover`.

### 7. Diga como ficou

Feche com um resumo curto:

- o que foi copiado, o que já estava atualizado e o que a pessoa preferiu manter;
- como ficou o MCP do Jira;
- se o kit de orquestração foi instalado, recusado ou não oferecido e, quando instalado, onde está a cópia do `settings.json` e como desfazer;
- o que ainda depende dela, como o login no navegador, um MCP com falha ou reabrir o Claude Code;
- um exemplo de uso para testar, escolhido entre as skills que ficaram instaladas.

Se algum passo falhou, mostre o erro e diga o que não foi feito. Não descreva como concluído o que não foi.

## Regras

- **Nada fora do combinado.** O setup só mexe em `agents/` e `skills/` da pasta pessoal e na configuração de MCP do Claude Code. Não instala programas e não mexe no repositório. O `settings.json`, `rules/` e `hooks/` só são alterados pelo script do kit de orquestração, no passo 6, com aceite próprio. O script deixa uma cópia do `settings.json` ao lado do original, e os hooks, quando rodam, guardam um marcador por sessão em `state/`.
- **Nunca substitua sem mostrar.** Arquivo diferente só é trocado depois de a pessoa ver a diferença e aceitar.
- **Sem credenciais.** Não peça, não leia e não grave token, senha ou e-mail de ninguém. Não rode comandos que imprimam a configuração dos servidores MCP, como `claude mcp get`, porque ela pode conter tokens.
