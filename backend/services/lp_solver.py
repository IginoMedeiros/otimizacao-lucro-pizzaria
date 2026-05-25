"""
[DOC-B03] services/lp_solver.py
---------------------------------
Motor de otimização baseado em Programação Linear Inteira (PLI).

Responsabilidades:
- Modelar o problema de otimização da pizzaria usando PuLP
- Resolver o modelo com o solver CBC (embutido no PuLP, sem instalação extra)
- Retornar a solução estruturada com quantidades, lucro e consumo por ingrediente

Modelo Matemático:
------------------
Variáveis de decisão:
    x = número inteiro de pizzas de Muçarela  (x >= 0)
    y = número inteiro de pizzas de Calabresa (y >= 0)

Função Objetivo:
    Maximizar Z = 20x + 25y

Restrições (baseadas nos dados da imagem):
    Massa:     0.5x + 0.5y  <= massa_disponivel
    Queijo:    0.3x + 0.2y  <= queijo_disponivel
    Molho:     0.2x + 0.2y  <= molho_disponivel
    Calabresa: 0.15y        <= calabresa_disponivel

Receitas por pizza (kg):
    Ingrediente | Muçarela | Calabresa
    ------------|----------|----------
    Massa       |   0.50   |   0.50
    Queijo      |   0.30   |   0.20
    Molho       |   0.20   |   0.20
    Calabresa   |   0.00   |   0.15
"""

import pulp
from schemas.models import StockInput, OptimizeResult, ConsumoIngredientes


# ---------------------------------------------------------------------------
# CONSTANTES — Receitas por pizza (consumo em kg por unidade produzida)
# ---------------------------------------------------------------------------

RECEITA_MUCARELA = {
    "massa": 0.50,
    "queijo": 0.30,
    "molho": 0.20,
    "calabresa": 0.00,
}

RECEITA_CALABRESA = {
    "massa": 0.50,
    "queijo": 0.20,
    "molho": 0.20,
    "calabresa": 0.15,
}

LUCRO_MUCARELA = 20.0   # R$ por pizza
LUCRO_CALABRESA = 25.0  # R$ por pizza

# Estoque mínimo necessário para produzir ao menos 1 pizza de qualquer tipo
# Muçarela: precisa de 0.2kg de molho (menor requisito entre todos)
ESTOQUE_MINIMO_MOLHO = 0.20


# ---------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ---------------------------------------------------------------------------

def resolver_otimizacao(stock: StockInput) -> OptimizeResult:
    """
    Recebe os estoques disponíveis e resolve o problema de PLI para
    maximizar o lucro da pizzaria.

    Parâmetros:
        stock (StockInput): estoques de massa, queijo, molho e calabresa em kg

    Retorna:
        OptimizeResult: solução ótima com quantidades, lucro e consumo

    Raises:
        ValueError: se o estoque for insuficiente para produzir qualquer pizza
    """

    # ------------------------------------------------------------------
    # 0. Validação rápida — estoque mínimo para qualquer produção
    #    Muçarela requer: massa>=0.5, queijo>=0.3, molho>=0.2
    #    Calabresa requer: massa>=0.5, queijo>=0.2, molho>=0.2, calabresa>=0.15
    # ------------------------------------------------------------------
    pode_mucarela = (
        stock.massa >= 0.5 and
        stock.queijo >= 0.3 and
        stock.molho >= 0.2
    )
    pode_calabresa = (
        stock.massa >= 0.5 and
        stock.queijo >= 0.2 and
        stock.molho >= 0.2 and
        stock.calabresa >= 0.15
    )

    if not pode_mucarela and not pode_calabresa:
        raise ValueError(
            "Estoque insuficiente para produzir qualquer pizza. "
            "Verifique os valores informados."
        )

    # ------------------------------------------------------------------
    # 1. Criar o problema de maximização
    # ------------------------------------------------------------------
    prob = pulp.LpProblem("Otimizacao_Pizzaria", pulp.LpMaximize)

    # ------------------------------------------------------------------
    # 2. Variáveis de decisão — inteiras, não-negativas
    # ------------------------------------------------------------------
    x = pulp.LpVariable("mucarela", lowBound=0, cat="Integer")
    y = pulp.LpVariable("calabresa", lowBound=0, cat="Integer")

    # ------------------------------------------------------------------
    # 3. Função objetivo: maximizar lucro total
    # ------------------------------------------------------------------
    prob += (LUCRO_MUCARELA * x + LUCRO_CALABRESA * y, "Lucro_Total")

    # ------------------------------------------------------------------
    # 4. Restrições de ingredientes
    # ------------------------------------------------------------------
    prob += (RECEITA_MUCARELA["massa"] * x + RECEITA_CALABRESA["massa"] * y <= stock.massa,     "Restricao_Massa")
    prob += (RECEITA_MUCARELA["queijo"] * x + RECEITA_CALABRESA["queijo"] * y <= stock.queijo,  "Restricao_Queijo")
    prob += (RECEITA_MUCARELA["molho"] * x + RECEITA_CALABRESA["molho"] * y <= stock.molho,     "Restricao_Molho")
    prob += (RECEITA_MUCARELA["calabresa"] * x + RECEITA_CALABRESA["calabresa"] * y <= stock.calabresa, "Restricao_Calabresa")

    # ------------------------------------------------------------------
    # 5. Resolver com CBC
    # ------------------------------------------------------------------
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    status = pulp.LpStatus[prob.status]

    if status not in ("Optimal", "Feasible"):
        raise ValueError(f"Solver encerrou com status inesperado: {status}")

    # ------------------------------------------------------------------
    # 6. Extrair resultados
    # ------------------------------------------------------------------
    qtd_mucarela = int(pulp.value(x))
    qtd_calabresa = int(pulp.value(y))
    lucro_total = float(pulp.value(prob.objective))

    consumo = ConsumoIngredientes(
        massa=round(RECEITA_MUCARELA["massa"] * qtd_mucarela + RECEITA_CALABRESA["massa"] * qtd_calabresa, 4),
        queijo=round(RECEITA_MUCARELA["queijo"] * qtd_mucarela + RECEITA_CALABRESA["queijo"] * qtd_calabresa, 4),
        molho=round(RECEITA_MUCARELA["molho"] * qtd_mucarela + RECEITA_CALABRESA["molho"] * qtd_calabresa, 4),
        calabresa=round(RECEITA_MUCARELA["calabresa"] * qtd_mucarela + RECEITA_CALABRESA["calabresa"] * qtd_calabresa, 4),
    )

    return OptimizeResult(
        mucarela=qtd_mucarela,
        calabresa=qtd_calabresa,
        lucro=round(lucro_total, 2),
        consumo=consumo,
        status=status,
    )
