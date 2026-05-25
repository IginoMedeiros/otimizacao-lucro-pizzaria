"""
[DOC-B02] routers/explainer.py
--------------------------------
Endpoint de explicação do resultado via API Claude.

Responsabilidades:
- Receber o resultado da otimização já calculado
- Chamar o serviço Claude de forma assíncrona para gerar explicação
- Retornar o texto explicativo em PT-BR

Importante:
- Este endpoint só é chamado quando o usuário clica em "Explicar Resultado"
- Nunca é chamado automaticamente — economia de tokens garantida por design
- O resultado já vem calculado no payload, Claude apenas narra em linguagem natural

Rota:
    POST /api/explicar

Request Body (ExplainRequest):
    {
        "mucarela": 8,
        "calabresa": 6,
        "lucro": 310.0,
        "consumo": { "massa": 7.0, "queijo": 3.6, "molho": 2.8, "calabresa": 0.9 }
    }

Response (ExplainResponse):
    {
        "explicacao": "Com base nos ingredientes disponíveis, ..."
    }

Erros tratados:
    422 — payload inválido (Pydantic valida automaticamente)
    503 — API Claude indisponível ou chave inválida
    500 — erro inesperado na chamada
"""

from fastapi import APIRouter, HTTPException
from schemas.models import ExplainRequest, ExplainResponse
from services.claude_service import gerar_explicacao

router = APIRouter(prefix="/api", tags=["Explicação Claude"])


@router.post(
    "/explicar",
    response_model=ExplainResponse,
    summary="Gerar explicação do resultado via Claude",
    description=(
        "Recebe o resultado da otimização e retorna uma explicação "
        "em linguagem natural gerada pelo Claude. "
        "Só deve ser chamado sob demanda explícita do usuário."
    ),
)
async def explicar(dados: ExplainRequest) -> ExplainResponse:
    """
    Chama a API Claude de forma assíncrona com um prompt compacto
    e retorna a explicação em português.

    - Consome ~80 tokens de input e ~150 tokens de output por chamada
    - Só é ativado por ação explícita do usuário no frontend
    """
    try:
        resposta = await gerar_explicacao(dados)
        return resposta

    except EnvironmentError as e:
        # Chave da API não configurada
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        # Erro na chamada à API Claude ou parsing da resposta
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar explicação: {str(e)}"
        )
