"""
[DOC-B01] routers/optimizer.py
--------------------------------
Endpoint de otimização da pizzaria.

Responsabilidades:
- Receber o payload de estoque enviado pelo frontend
- Delegar o cálculo ao motor de otimização (lp_solver.py)
- Retornar a solução estruturada ou uma mensagem de erro clara

Rota:
    POST /api/otimizar

Request Body (StockInput):
    {
        "massa": 10.0,
        "queijo": 5.0,
        "molho": 4.0,
        "calabresa": 2.0
    }

Response (OptimizeResult):
    {
        "mucarela": 8,
        "calabresa": 6,
        "lucro": 310.0,
        "consumo": { "massa": 7.0, "queijo": 3.6, "molho": 2.8, "calabresa": 0.9 },
        "status": "Optimal"
    }

Erros tratados:
    422 — payload inválido (Pydantic valida automaticamente)
    400 — estoque insuficiente para qualquer pizza
    500 — erro inesperado no solver
"""

from fastapi import APIRouter, HTTPException
from schemas.models import StockInput, OptimizeResult
from services.lp_solver import resolver_otimizacao

router = APIRouter(prefix="/api", tags=["Otimização"])


@router.post(
    "/otimizar",
    response_model=OptimizeResult,
    summary="Calcular produção ótima de pizzas",
    description=(
        "Recebe os estoques de ingredientes e retorna a quantidade ótima "
        "de pizzas de muçarela e calabresa para maximizar o lucro, "
        "respeitando os limites de estoque."
    ),
)
def otimizar(stock: StockInput) -> OptimizeResult:
    """
    Resolve o problema de programação linear inteira e retorna a solução ótima.

    - Delega o cálculo ao `lp_solver.py` (PuLP + CBC, execução local)
    - Nenhum token de IA é consumido neste endpoint
    - Retorna erro 400 se o estoque for insuficiente para qualquer produção
    """
    try:
        resultado = resolver_otimizacao(stock)
        return resultado

    except ValueError as e:
        # Estoque insuficiente ou status inesperado do solver
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Erro inesperado — loga e retorna 500
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no solver: {str(e)}"
        )
