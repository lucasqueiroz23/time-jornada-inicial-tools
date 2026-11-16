# time-jornada-inicial-tools

Repositório do time Jornada Inicial para guardar e compartilhar **agents** e **skills** usados no dia a dia com o Claude Code.

A ideia é ter um lugar único, versionado e revisável, para que o que uma pessoa cria e funciona bem fique disponível para o time todo.

## O que fica aqui

| Tipo | O que é | Quando usar |
| --- | --- | --- |
| **Agent** | Um subagente com papel, instruções e ferramentas próprias. | Tarefas delegáveis com escopo fechado, como revisar um PR, investigar um bug ou escrever testes. |
| **Skill** | Um conjunto de instruções (e arquivos de apoio) que o Claude carrega quando a tarefa pede. | Procedimentos repetíveis do time, como passos de deploy, checklist de revisão ou padrões de um projeto. |

## Estrutura

Os arquivos ficam em `.claude/`, no mesmo formato que o Claude Code lê. Assim, ao abrir o Claude Code dentro deste repositório, tudo já está disponível sem configuração.

```
.
└── .claude/
    ├── agents/
    │   └── revisor-de-codigo.md
    └── skills/
        ├── descricao-de-pr/
        │   └── SKILL.md
        └── refinar-tarefa/
            └── SKILL.md
```

- Cada agent é um arquivo `.md` em `.claude/agents/`.
- Cada skill é uma pasta em `.claude/skills/` com um `SKILL.md` dentro, mais os arquivos de apoio que ela precisar.
- Nomes em `kebab-case`, descrevendo o que a ferramenta faz.

## Disponíveis

| Nome | Tipo | O que faz |
| --- | --- | --- |
| [refinar-tarefa](.claude/skills/refinar-tarefa/SKILL.md) | Skill | Refina uma tarefa do Jira com pouca informação: diz o que entendeu, tira as dúvidas com quem pediu, reescreve a descrição e, depois do aceite, grava no Jira e move a tarefa para "Refinado". Feita para produto e projetos. Precisa do MCP do Jira configurado. Uso: `/refinar-tarefa ABC-123`. |
| [revisor-de-codigo](.claude/agents/revisor-de-codigo.md) | Agent | Revisa as alterações locais ou de uma branch em busca de bugs, riscos e pontos de melhoria. |
| [descricao-de-pr](.claude/skills/descricao-de-pr/SKILL.md) | Skill | Escreve a descrição de um pull request a partir das alterações da branch atual. |

O `revisor-de-codigo` e a `descricao-de-pr` servem de exemplo para quem for criar os próximos.

## Como usar

### Neste repositório

Abra o Claude Code na raiz do repositório. Os agents aparecem em `/agents` e as skills podem ser chamadas pelo nome, como `/descricao-de-pr`.

### Em todos os seus projetos

Copie o que precisar para a sua pasta pessoal do Claude Code:

```bash
mkdir -p ~/.claude/agents ~/.claude/skills
cp .claude/agents/revisor-de-codigo.md ~/.claude/agents/
cp -r .claude/skills/descricao-de-pr ~/.claude/skills/
```

### Em um projeto específico

Copie para a pasta `.claude/` do projeto:

```bash
mkdir -p <projeto>/.claude/agents <projeto>/.claude/skills
cp .claude/agents/revisor-de-codigo.md <projeto>/.claude/agents/
cp -r .claude/skills/descricao-de-pr <projeto>/.claude/skills/
```

As cópias não se atualizam sozinhas. Quando algo mudar aqui, copie de novo.

## Como contribuir

1. Crie uma branch a partir da `main`.
2. Adicione o agent ou a skill seguindo os modelos abaixo.
3. Teste em uma tarefa real antes de abrir o PR.
4. Inclua a ferramenta na tabela [Disponíveis](#disponíveis).
5. Abra o PR explicando o que a ferramenta faz e em que situação você usou.

### Modelo de agent

`.claude/agents/nome-do-agent.md`

```markdown
---
name: nome-do-agent
description: O que o agent faz e quando deve ser usado.
tools: Read, Grep, Glob, Bash
---

Instruções do agent: papel, passos que deve seguir e formato da resposta.
```

O campo `tools` limita o que o agent pode usar. Sem ele, o agent herda todas as ferramentas da sessão, incluindo as de conectores como o Jira. Para herdar tudo e bloquear só algumas, use `disallowedTools` no lugar.

Um agent roda separado da conversa e devolve um resultado no fim. Se a ferramenta precisa perguntar, esperar resposta ou pedir aceite, faça uma skill, como a `refinar-tarefa`.

### Modelo de skill

`.claude/skills/nome-da-skill/SKILL.md`

```markdown
---
name: nome-da-skill
description: O que a skill faz e quando deve ser usada.
---

Instruções da skill: passo a passo, regras e exemplos.
```

A `description` é o que o Claude lê para decidir se usa a ferramenta, então escreva de forma específica: o que ela faz e em que situação se aplica.

## Boas práticas

- **Sem segredos.** Nada de tokens, senhas ou dados de clientes nos arquivos.
- **Uma responsabilidade por ferramenta.** É melhor ter duas skills pequenas do que uma que tenta fazer tudo.
- **Explique o porquê.** Instruções com o motivo junto funcionam melhor do que regras soltas.
- **Mantenha vivo.** Se algo parou de funcionar ou ficou obsoleto, atualize ou remova.
