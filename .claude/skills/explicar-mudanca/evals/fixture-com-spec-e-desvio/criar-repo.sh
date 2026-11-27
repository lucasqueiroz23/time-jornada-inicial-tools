#!/usr/bin/env bash
# Cria um repositório de exemplo com uma branch "escrita pela IA" que cumpre parte do plano,
# faz uma mudança fora do escopo, engole um erro e tem um teste que só testa o mock.
set -eu
DEST="${1:-loja}"
rm -rf "$DEST"; mkdir -p "$DEST"; cd "$DEST"
git init -q -b main
git config user.email dev@example.com; git config user.name Dev
mkdir -p loja tests
cat > loja/__init__.py <<'P'
P
cat > loja/pedidos.py <<'P'
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Pedido:
    id: int
    itens: list
    status: str = "pendente"
    criado_em: datetime = field(default_factory=datetime.now)


class RepositorioPedidos:
    def __init__(self):
        self._pedidos = {}

    def salvar(self, pedido):
        self._pedidos[pedido.id] = pedido

    def buscar(self, pedido_id):
        return self._pedidos.get(pedido_id)
P
cat > loja/precos.py <<'P'
def calcular_total(itens):
    """Soma preço x quantidade, arredondando para centavos no final."""
    total = sum(i["preco"] * i["quantidade"] for i in itens)
    return round(total, 2)
P
cat > loja/notificacoes.py <<'P'
class Notificador:
    def __init__(self, cliente_email):
        self.cliente_email = cliente_email

    def enviar(self, destino, assunto, corpo):
        self.cliente_email.send(to=destino, subject=assunto, body=corpo)
P
cat > tests/test_precos.py <<'P'
from loja.precos import calcular_total


def test_total_soma_itens():
    assert calcular_total([{"preco": 10.0, "quantidade": 2}, {"preco": 0.5, "quantidade": 3}]) == 21.5
P
git add -A; git commit -qm "loja: pedidos, preços e notificações"

git switch -qc develop
cat > loja/relatorios.py <<'P'
from loja.precos import calcular_total


def total_do_dia(pedidos):
    return calcular_total([i for p in pedidos for i in p.itens])
P
git add -A; git commit -qm "relatório de total do dia"

git switch -qc feat/ABC-123-cancelar-pedido
mkdir -p .specs/features/abc-123-cancelar-pedido
cat > .specs/features/abc-123-cancelar-pedido/request.md <<'P'
# ABC-123 — Permitir cancelar pedido

Hoje o cliente liga para o suporte para cancelar um pedido. Queremos uma função de serviço que o
backoffice possa chamar.

## Critérios de aceite
1. Um pedido com status "pendente" pode ser cancelado e passa a ter status "cancelado".
2. Um pedido com status "enviado" não pode ser cancelado: a operação falha com erro claro e o status não muda.
3. O motivo do cancelamento é obrigatório e fica registrado no pedido.
4. O cliente recebe um e-mail avisando do cancelamento.
P
cat > .specs/features/abc-123-cancelar-pedido/plan.md <<'P'
# Plano — ABC-123

## Caminho
- `loja/cancelamento.py`: função `cancelar_pedido(repo, notificador, pedido_id, motivo)`.
- `loja/pedidos.py`: campos `motivo_cancelamento` e `cancelado_em` no `Pedido`.
- Testes em `tests/test_cancelamento.py`, um por critério.

## Fora do escopo
- Reembolso.
- Qualquer mudança em preços ou relatórios.
P
git add -A; git commit -qm "ABC-123: plano"

cat > loja/pedidos.py <<'P'
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Pedido:
    id: int
    itens: list
    status: str = "pendente"
    criado_em: datetime = field(default_factory=datetime.now)
    email_cliente: str = ""
    cancelado_em: Optional[datetime] = None


class RepositorioPedidos:
    def __init__(self):
        self._pedidos = {}

    def salvar(self, pedido):
        self._pedidos[pedido.id] = pedido

    def buscar(self, pedido_id):
        return self._pedidos.get(pedido_id)
P
cat > loja/cancelamento.py <<'P'
from datetime import datetime


class CancelamentoNaoPermitido(Exception):
    pass


def cancelar_pedido(repo, notificador, pedido_id, motivo=None):
    pedido = repo.buscar(pedido_id)
    if pedido.status == "enviado":
        raise CancelamentoNaoPermitido(f"Pedido {pedido_id} já foi enviado")

    pedido.status = "cancelado"
    pedido.cancelado_em = datetime.now()
    repo.salvar(pedido)

    try:
        notificador.enviar_template(pedido.email_cliente, "pedido_cancelado", {"id": pedido.id})
    except Exception:
        pass

    return pedido
P
git add -A; git commit -qm "ABC-123: cancelamento de pedido"

cat > loja/precos.py <<'P'
from decimal import Decimal, ROUND_HALF_UP


def calcular_total(itens):
    """Soma preço x quantidade com Decimal, arredondando cada item."""
    total = Decimal("0")
    for i in itens:
        subtotal = Decimal(str(i["preco"])) * i["quantidade"]
        total += subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(total)
P
cat > tests/test_cancelamento.py <<'P'
from unittest.mock import MagicMock

from loja.cancelamento import cancelar_pedido


def test_cancela_pedido_pendente():
    repo = MagicMock()
    pedido = MagicMock(status="pendente")
    repo.buscar.return_value = pedido

    cancelar_pedido(repo, MagicMock(), 1, "desistiu")

    repo.salvar.assert_called_once_with(pedido)
P
git add -A; git commit -qm "ABC-123: testes e ajuste de precisão nos preços"
git switch -q feat/ABC-123-cancelar-pedido
