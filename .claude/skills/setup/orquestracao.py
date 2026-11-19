#!/usr/bin/env python3
"""Instala, verifica ou remove o kit de orquestração na pasta pessoal do Claude Code.

O kit tem três partes, além dos agents (que o setup copia como qualquer outro):
  - a regra, copiada para rules/orquestracao.md;
  - quatro hooks, copiados para hooks/;
  - entradas em settings.json: os hooks e duas variáveis de ambiente.

Uso:
  orquestracao.py checar                  só lê e mostra o estado de cada parte
  orquestracao.py instalar [--substituir] instala o que falta
  orquestracao.py remover                 desfaz a instalação

Sem --substituir, um arquivo que já existe com conteúdo diferente não é trocado,
e o hook correspondente não é registrado. Antes de alterar o settings.json, o
script grava uma cópia ao lado dele. Uma variável de ambiente que já existe com
outro valor nunca é alterada.

Código de saída: 0 quando deu certo, 1 quando nada foi alterado por causa de um
erro, 2 quando instalou mas manteve algum arquivo da pessoa.
"""
import json
import os
import shutil
import sys
import time

ORIGEM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orquestracao")
PADRAO = os.path.expanduser("~/.claude")
DESTINO = os.path.abspath(os.environ.get("CLAUDE_CONFIG_DIR") or PADRAO)
# Se o settings.json for um link (dotfiles), a escrita vai para o arquivo real.
SETTINGS = os.path.realpath(os.path.join(DESTINO, "settings.json"))

REGRA = ("regra.md", os.path.join("rules", "orquestracao.md"))
HOOKS = [
    # (arquivo, evento, matcher)
    ("validacao-gate.py", "Stop", None),
    ("subagente-contrato.sh", "SubagentStart", None),
    ("validacao-limpar.py", "SubagentStart", "revisor"),
    ("validacao-marcar.py", "SubagentStop", None),
]
ENV = {
    "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet",
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1",
}


def arquivos():
    """Pares (origem, destino) de todos os arquivos do kit."""
    pares = [(os.path.join(ORIGEM, REGRA[0]), os.path.join(DESTINO, REGRA[1]))]
    for nome, _, _ in HOOKS:
        pares.append((os.path.join(ORIGEM, "hooks", nome), os.path.join(DESTINO, "hooks", nome)))
    return pares


def estado_arquivo(origem, destino):
    if not os.path.exists(destino):
        return "faltando"
    with open(origem, "rb") as a, open(destino, "rb") as b:
        return "igual" if a.read() == b.read() else "diferente"


def comando(nome):
    """Comando gravado no settings.json para um hook."""
    if DESTINO == os.path.abspath(PADRAO):
        return '"$HOME"/.claude/hooks/' + nome
    return '"' + os.path.join(DESTINO, "hooks", nome) + '"'


def e_do_kit(texto, nome):
    """O comando aponta para o arquivo do kit na pasta pessoal, e não para um
    hook de mesmo nome em outro lugar."""
    if not isinstance(texto, str):
        return False
    caminho = texto.strip().replace('"', "").replace("'", "")
    caminho = caminho.replace("${HOME}", os.path.expanduser("~")).replace("$HOME", os.path.expanduser("~"))
    caminho = os.path.expanduser(caminho)
    return os.path.abspath(caminho) == os.path.join(DESTINO, "hooks", nome)


def formato_invalido(dados):
    """Devolve a descrição do primeiro problema de formato, ou None."""
    hooks = dados.get("hooks", {})
    if not isinstance(hooks, dict):
        return "a chave hooks não é um objeto"
    for evento, grupos in hooks.items():
        if not isinstance(grupos, list):
            return "hooks.%s não é uma lista" % evento
        for grupo in grupos:
            if not isinstance(grupo, dict):
                return "hooks.%s tem um item que não é um objeto" % evento
            itens = grupo.get("hooks", [])
            if not isinstance(itens, list) or not all(isinstance(h, dict) for h in itens):
                return "hooks.%s tem um grupo com a lista hooks fora do formato" % evento
    if not isinstance(dados.get("env", {}), dict):
        return "a chave env não é um objeto"
    return None


def ler_settings():
    """Devolve (dados, erro). Arquivo ausente conta como configuração vazia."""
    if not os.path.exists(SETTINGS):
        return {}, None
    try:
        with open(SETTINGS, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError) as e:
        return None, str(e)
    if not isinstance(dados, dict):
        return None, "o conteúdo não é um objeto JSON"
    return dados, formato_invalido(dados)


def tem_hook(dados, nome, evento):
    """O hook conta como configurado se algum comando do evento aponta para o
    arquivo do kit."""
    for grupo in (dados.get("hooks") or {}).get(evento) or []:
        for h in grupo.get("hooks") or []:
            if e_do_kit(h.get("command"), nome):
                return True
    return False


def gravar_settings(dados):
    existia = os.path.exists(SETTINGS)
    if existia:
        base = SETTINGS + ".antes-da-orquestracao-" + time.strftime("%Y%m%d-%H%M%S")
        copia, n = base, 1
        while os.path.exists(copia):
            n += 1
            copia = "%s-%d" % (base, n)
        shutil.copy2(SETTINGS, copia)
        print("copia " + copia)
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    temporario = SETTINGS + ".tmp"
    with open(temporario, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if existia:
        shutil.copymode(SETTINGS, temporario)
    os.replace(temporario, SETTINGS)


def checar():
    for origem, destino in arquivos():
        print("arquivo %s %s" % (estado_arquivo(origem, destino), os.path.relpath(destino, DESTINO)))
    dados, erro = ler_settings()
    if erro:
        print("settings erro " + erro)
        return 1
    for nome, evento, _ in HOOKS:
        print("config %s %s (%s)" % ("ok" if tem_hook(dados, nome, evento) else "faltando", nome, evento))
    env = dados.get("env") or {}
    for chave, valor in ENV.items():
        if chave not in env:
            print("env faltando %s=%s" % (chave, valor))
        elif str(env[chave]) == valor:
            print("env ok %s=%s" % (chave, valor))
        else:
            print("env diferente %s atual=%s kit=%s" % (chave, env[chave], valor))
    return 0


def instalar(substituir):
    dados, erro = ler_settings()
    if erro:
        print("settings erro " + erro)
        print("nada foi alterado")
        return 1

    pulados = []
    for origem, destino in arquivos():
        estado = estado_arquivo(origem, destino)
        rel = os.path.relpath(destino, DESTINO)
        if estado == "diferente" and not substituir:
            pulados.append(os.path.basename(destino))
            print("arquivo mantido %s (diferente do kit; use --substituir para trocar)" % rel)
            continue
        if estado != "igual":
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copyfile(origem, destino)
            print("arquivo copiado " + rel)
        if os.sep + "hooks" + os.sep in destino:
            os.chmod(destino, 0o755)

    mudou = False
    hooks = dados.setdefault("hooks", {})
    for nome, evento, matcher in HOOKS:
        if tem_hook(dados, nome, evento):
            continue
        if nome in pulados:
            print("config pulado %s (%s): o arquivo em hooks/ não é o do kit" % (nome, evento))
            continue
        grupo = {"hooks": [{"type": "command", "command": comando(nome), "timeout": 5}]}
        if matcher:
            grupo["matcher"] = matcher
        hooks.setdefault(evento, []).append(grupo)
        print("config adicionado %s (%s)" % (nome, evento))
        mudou = True

    env = dados.setdefault("env", {})
    for chave, valor in ENV.items():
        if chave not in env:
            env[chave] = valor
            print("env adicionado %s=%s" % (chave, valor))
            mudou = True
        elif str(env[chave]) != valor:
            print("env mantido %s=%s (o kit sugere %s)" % (chave, env[chave], valor))

    for chave in ("hooks", "env"):
        if not dados[chave]:
            del dados[chave]
    if mudou:
        gravar_settings(dados)
    else:
        print("settings sem alteração")
    return 2 if pulados else 0


def remover():
    dados, erro = ler_settings()
    if erro:
        print("settings erro " + erro)
        print("nada foi alterado")
        return 1

    mudou = False
    hooks = dados.get("hooks") or {}
    for nome, evento, _ in HOOKS:
        grupos = hooks.get(evento) or []
        novos = []
        for grupo in grupos:
            antes = grupo.get("hooks") or []
            depois = [h for h in antes if not e_do_kit(h.get("command"), nome)]
            if len(depois) != len(antes):
                mudou = True
                print("config removido %s (%s)" % (nome, evento))
                if not depois:
                    continue
                grupo = dict(grupo, hooks=depois)
            novos.append(grupo)
        if evento in hooks:
            if novos:
                hooks[evento] = novos
            else:
                del hooks[evento]
    if "hooks" in dados and not dados["hooks"]:
        del dados["hooks"]

    env = dados.get("env") or {}
    for chave, valor in ENV.items():
        if str(env.get(chave)) == valor:
            del env[chave]
            mudou = True
            print("env removido " + chave)
        elif chave in env:
            print("env mantido %s=%s (não é o valor do kit)" % (chave, env[chave]))
    if "env" in dados and not dados["env"]:
        del dados["env"]

    if mudou:
        gravar_settings(dados)
    else:
        print("settings sem alteração")

    for origem, destino in arquivos():
        rel = os.path.relpath(destino, DESTINO)
        estado = estado_arquivo(origem, destino)
        if estado == "igual":
            os.remove(destino)
            print("arquivo removido " + rel)
        elif estado == "diferente":
            print("arquivo mantido %s (foi alterado; apague à mão se quiser)" % rel)
    return 0


def main(argv):
    acao = argv[1] if len(argv) > 1 else "checar"
    extras = argv[2:]
    if acao == "checar" and not extras:
        return checar()
    if acao == "instalar" and extras in ([], ["--substituir"]):
        return instalar(bool(extras))
    if acao == "remover" and not extras:
        return remover()
    print(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv))
