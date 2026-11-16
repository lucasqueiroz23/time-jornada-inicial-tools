---
name: descricao-de-pr
description: Escreve a descrição de um pull request a partir das alterações da branch atual. Use quando alguém pedir para descrever, resumir ou abrir um PR.
---

# Descrição de PR

A descrição é lida por quem vai revisar o PR e, mais tarde, por quem tentar entender por que a mudança foi feita. Essas pessoas não acompanharam o desenvolvimento, então o texto precisa se sustentar sozinho.

## Passos

1. Veja o que a branch muda em relação à principal:
   - `git log main..HEAD --oneline` para os commits;
   - `git diff main...HEAD` para o código.
2. Entenda o motivo da mudança. Se ele não estiver claro nos commits nem na conversa, pergunte antes de escrever.
3. Escreva a descrição no modelo abaixo.
4. Mostre o texto e só abra o PR se a pessoa pedir.

## Modelo

```markdown
## O que muda

Um ou dois parágrafos explicando a mudança e o motivo dela.

## Como testar

Passos para quem revisa conseguir validar a mudança.

## Pontos de atenção

Riscos, migrações, variáveis de ambiente novas ou decisões que merecem um olhar mais cuidadoso. Remova a seção se não houver nenhum.
```

## Regras

- Escreva em português, com frases completas.
- Fale do comportamento que muda, não de cada arquivo alterado. O diff já mostra os arquivos.
- Se algo não foi testado, diga isso de forma explícita em "Como testar".
- Inclua o link do card ou da issue quando houver.
