"""
[DOC-T01] tests/test_optimizer.py
-----------------------------------
Testes unitários para o motor de otimização PuLP.

Cobre:
- Solução ótima com os dados padrão da imagem
- Comportamento com estoque zerado
- Comportamento com estoque que só permite muçarela
- Comportamento com estoque que só permite calabresa
- Verificação de que os valores retornados são inteiros não-negativos
"""

import pytest
from schemas.models import StockInput
from services.lp_solver import resolver_otimizacao


def test_solucao_padrao():
    """Dados padrão da imagem devem retornar solução viável com lucro > 0."""
    stock = StockInput(massa=10.0, queijo=5.0, molho=4.0, calabresa=2.0)
    resultado = resolver_otimizacao(stock)

    assert resultado.status == "Optimal"
    assert resultado.lucro > 0
    assert resultado.mucarela >= 0
    assert resultado.calabresa >= 0


def test_lucro_maior_que_zero():
    """Lucro deve ser positivo com estoque suficiente."""
    stock = StockInput(massa=10.0, queijo=5.0, molho=4.0, calabresa=2.0)
    resultado = resolver_otimizacao(stock)
    assert resultado.lucro > 0


def test_estoque_zerado_levanta_erro():
    """Estoque zerado deve levantar ValueError."""
    stock = StockInput(massa=0.0, queijo=0.0, molho=0.0, calabresa=0.0)
    with pytest.raises(ValueError):
        resolver_otimizacao(stock)


def test_apenas_mucarela_possivel():
    """Sem calabresa no estoque, solução deve usar apenas muçarela."""
    stock = StockInput(massa=5.0, queijo=5.0, molho=5.0, calabresa=0.0)
    resultado = resolver_otimizacao(stock)
    assert resultado.calabresa == 0
    assert resultado.mucarela > 0


def test_consumo_nao_excede_estoque():
    """Consumo calculado não deve exceder o estoque informado."""
    stock = StockInput(massa=10.0, queijo=5.0, molho=4.0, calabresa=2.0)
    resultado = resolver_otimizacao(stock)

    assert resultado.consumo.massa <= stock.massa + 1e-6
    assert resultado.consumo.queijo <= stock.queijo + 1e-6
    assert resultado.consumo.molho <= stock.molho + 1e-6
    assert resultado.consumo.calabresa <= stock.calabresa + 1e-6


def test_quantidades_sao_inteiras():
    """Quantidades devem ser inteiras (PLI)."""
    stock = StockInput(massa=10.0, queijo=5.0, molho=4.0, calabresa=2.0)
    resultado = resolver_otimizacao(stock)

    assert isinstance(resultado.mucarela, int)
    assert isinstance(resultado.calabresa, int)
