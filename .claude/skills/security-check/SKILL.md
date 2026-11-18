---
name: security-check
description: Validação de segurança de código e configuração em qualquer projeto. Use quando o usuário pedir validação, auditoria, revisão ou checagem de segurança, procurar vulnerabilidades, secrets vazados, injeção, problemas de auth, ou invocar /security-check. Use TAMBÉM proativamente, sem pedido explícito, ao concluir uma implementação ou mudança de código relevante — antes de commit/PR — com escopo "diff". Aceita argumento opcional para limitar o escopo ("diff" para só as mudanças pendentes, ou um path). Não use para revisão de código geral (estilo, bugs funcionais) — só para a dimensão de segurança.
---

# Security Check — validação de segurança

Auditoria de segurança do projeto atual. O objetivo é encontrar problemas **reais e verificados** — um relatório curto e confiável vale mais que uma lista longa de suspeitas.

## Escopo

Interpretar o argumento recebido:

- **`diff`** — analisar apenas as mudanças pendentes: `git diff` + staged + arquivos novos não rastreados. Útil antes de abrir PR.
- **Um path** (arquivo ou diretório) — limitar a análise a ele.
- **Sem argumento** — projeto inteiro, priorizando código de aplicação. Ignorar `vendor/`, `node_modules/`, `dist/`, `.git/` e afins.

## Passos

### 1. Detectar a stack

Olhar os manifestos na raiz (`go.mod`, `composer.json`, `package.json`, `requirements.txt`, `Dockerfile`, `docker-compose*`, manifests k8s) para saber quais checagens e scanners se aplicam.

### 2. Rodar scanners disponíveis

Usar **apenas ferramentas já instaladas** (verificar com `command -v` antes; nunca instalar nada sem avisar o usuário):

| Stack | Comandos |
|---|---|
| Go | `govulncheck ./...`; `gosec ./...` se houver |
| PHP | `composer audit` |
| JS/TS | `npm audit` / `pnpm audit` / `yarn audit` |
| Python | `pip-audit` |
| Secrets | `gitleaks detect` (ou `gitleaks protect --staged` no modo diff) |

Se um scanner relevante não estiver instalado, registrar no relatório como "não coberto" — não silenciar a lacuna — e incluir o comando de instalação para o usuário decidir (ex.: `go install golang.org/x/vuln/cmd/govulncheck@latest`, `brew install gitleaks`).

### 3. Revisão manual guiada pelo checklist

Usar Grep/Glob para localizar candidatos e **ler o código em volta** antes de concluir qualquer coisa.

**Secrets e credenciais**
- Tokens, chaves de API, senhas, connection strings hardcoded (inclusive em testes, scripts, pipelines de CI e docs).
- `.env` ou similares versionados no git; valores reais em arquivos `*.example`.
- Credenciais default de infra local vazando para configuração de produção (overlays, configmaps, secrets de k8s).

**Entrada e injeção**
- SQL montado por concatenação/interpolação em vez de placeholders/prepared statements.
- Execução de comando com entrada do usuário (`exec`, `shell_exec`, `os/exec` com string montada).
- Path traversal: paths de arquivo construídos com entrada externa sem sanitização.
- SSRF: URLs de requisição vindas de entrada externa sem allowlist.
- Deserialização de dados não confiáveis (`unserialize`, `pickle`, YAML unsafe).

**Autenticação e autorização**
- Rotas/endpoints sem middleware de autenticação (comparar o router com os handlers).
- IDOR: recursos acessados por ID sem checar que pertencem ao chamador/tenant.
- Comparação de tokens/segredos sem tempo constante onde relevante.
- Validação de webhook sem verificação de assinatura/HMAC quando o provedor oferece.

**Exposição de dados**
- Mensagens de erro públicas detalhadas demais — o contrato externo deve retornar erro genérico; o motivo real vai só para log/admin interno. Detalhe interno em resposta pública é vazamento.
- PII ou segredos em logs (CPF, e-mail, tokens, corpo de request completo).
- Stack traces ou modo debug habilitável em produção.
- Endpoints de introspecção (metrics, pprof, health detalhado) expostos publicamente.

**Configuração**
- CORS com `*` em API autenticada.
- TLS desabilitado ou verificação de certificado pulada (`InsecureSkipVerify`, `verify=False`).
- Portas/serviços a mais expostos em Dockerfile/compose/k8s de produção.
- Falta de limites: timeouts de cliente HTTP, tamanho máximo de body, rate limiting em endpoints sensíveis.

**Criptografia**
- MD5/SHA-1 para senha (senha exige bcrypt/argon2); hash simples sem salt.
- Geradores não criptográficos (`math/rand`, `Math.random`) para tokens, IDs de sessão ou segredos.
- Algoritmos/modos fracos (ECB, chaves curtas, IV fixo).

### 4. Verificar antes de reportar

Para **cada** achado: abrir o arquivo, entender o contexto e confirmar que é explorável ou é um risco concreto no cenário real do projeto. Exemplos de falso positivo a descartar: credencial que só existe no compose de dev local, SQL "concatenado" cujo valor vem de constante interna, endpoint sem auth que é o próprio health check. Achado não confirmado não entra no relatório — na dúvida, entra como "verificar manualmente", separado dos confirmados.

### 5. Checar se o achado já é conhecido

Antes de reportar, procurar o assunto na documentação de decisões do projeto: `.specs/`, `docs/`, `README`, `CLAUDE.md`, `STATE.md`, `ADR*`, `TODO`/`FIXME` no código. Reportar como novidade algo que o time já mapeou e decidiu adiar vira ruído e desgasta a confiança no relatório.

Se o achado já estiver registrado, ele **continua no relatório** (o risco é real e segue aberto no código), mas com a marca "já mapeado" e a referência ao arquivo/data da decisão. Um item já conhecido que foi de fato corrigido no código não é achado — não incluir.

## Relatório

1. **Resumo executivo primeiro**: uma ou duas frases — quantos achados por severidade, ou "nenhum problema confirmado".
2. Tabela de achados confirmados, do mais grave para o mais leve:

| Severidade | Onde | Problema | Recomendação |
|---|---|---|---|
| Crítica / Alta / Média / Baixa | `arquivo:linha` | descrição objetiva | correção sugerida |

Achado já registrado na documentação do projeto entra na tabela normalmente, com "(já mapeado: `arquivo`, data)" no fim da recomendação.

3. Seção "Não coberto": scanners ausentes (com o comando de instalação), áreas fora do escopo pedido.
4. Se houver itens "verificar manualmente", listar por último, claramente separados.

Critério de severidade: **Crítica** = explorável remotamente sem auth ou segredo de produção exposto; **Alta** = explorável por usuário autenticado ou vazamento de dado sensível; **Média** = exige condições específicas ou defesa em profundidade ausente; **Baixa** = hardening/boa prática.

## Regras

- **Só reportar, não corrigir.** Aplicar correções apenas se o usuário pedir depois de ver o relatório.
- Não rodar nada que altere estado (migrations, deploys, writes) durante a auditoria.
- Nunca colar o valor de um segredo encontrado no relatório — indicar arquivo:linha e o tipo do segredo.
