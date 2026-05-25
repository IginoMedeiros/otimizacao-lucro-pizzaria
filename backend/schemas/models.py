"""
[DOC-B05] schemas/models.py
----------------------------
Define os modelos de dados usados na API utilizando Pydantic v2.

Responsabilidades:
- Validar e tipar os dados de entrada (request) e saída (response)
- Garantir que valores inválidos (negativos, nulos) sejam rejeitados antes
  de chegar às camadas de serviço
- Servir como contrato entre frontend e backend

Modelos:
- StockInput       → payload enviado pelo frontend com os estoques disponíveis
- OptimizeResult   → resposta do solver com quantidades e lucro
- ExplainRequest   → payload enviado ao endpoint de explicação
- ExplainResponse  → resposta com o texto gerado pelo Claude
"""

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------------------

class StockInput(BaseModel):
    """
    Representa os estoques de ingredientes disponíveis na pizzaria.

    Todos os campos são obrigatórios, do tipo float e devem ser >= 0.
    Os valores padrão refletem o enunciado do problema da imagem.

    Campos:
        massa     (float): estoque de massa em kg      — padrão: 10.0 kg
        queijo    (float): estoque de queijo em kg     — padrão:  5.0 kg
        molho     (float): estoque de molho em kg      — padrão:  4.0 kg
        calabresa (float): estoque de calabresa em kg  — padrão:  2.0 kg
    """

    massa: float = Field(default=10.0, ge=0, description="Estoque de massa disponível em kg")
    queijo: float = Field(default=5.0, ge=0, description="Estoque de queijo disponível em kg")
    molho: float = Field(default=4.0, ge=0, description="Estoque de molho disponível em kg")
    calabresa: float = Field(default=2.0, ge=0, description="Estoque de calabresa disponível em kg")

    model_config = {
        "json_schema_extra": {
            "example": {"massa": 10.0, "queijo": 5.0, "molho": 4.0, "calabresa": 2.0}
        }
    }


class ExplainRequest(BaseModel):
    """
    Payload enviado ao endpoint /api/explicar.

    Contém o resultado da otimização já calculado para que o Claude
    possa gerar uma explicação em linguagem natural sem precisar
    recalcular nada — mantendo o prompt compacto.
    """

    mucarela: int = Field(ge=0, description="Quantidade de pizzas de muçarela produzidas")
    calabresa: int = Field(ge=0, description="Quantidade de pizzas de calabresa produzidas")
    lucro: float = Field(ge=0, description="Lucro máximo alcançado em R$")
    consumo: dict = Field(description="Consumo real por ingrediente em kg")

    model_config = {
        "json_schema_extra": {
            "example": {
                "mucarela": 8, "calabresa": 6, "lucro": 310.0,
                "consumo": {"massa": 7.0, "queijo": 3.6, "molho": 2.8, "calabresa": 0.9}
            }
        }
    }


# ---------------------------------------------------------------------------
# RESPONSE MODELS
# ---------------------------------------------------------------------------

class ConsumoIngredientes(BaseModel):
    """
    Sub-modelo que representa o consumo real de cada ingrediente
    após a otimização. Utilizado dentro de OptimizeResult.
    """

    massa: float = Field(description="Consumo de massa em kg")
    queijo: float = Field(description="Consumo de queijo em kg")
    molho: float = Field(description="Consumo de molho em kg")
    calabresa: float = Field(description="Consumo de calabresa em kg")


class OptimizeResult(BaseModel):
    """
    Resposta completa retornada pelo endpoint /api/otimizar.

    Contém a solução ótima encontrada pelo solver PuLP/CBC, incluindo
    quantidades de cada pizza, lucro máximo e detalhamento do consumo
    de ingredientes — usado pelo frontend para exibir ResultCard e UsageChart.
    """

    mucarela: int = Field(ge=0, description="Quantidade ótima de pizzas de muçarela")
    calabresa: int = Field(ge=0, description="Quantidade ótima de pizzas de calabresa")
    lucro: float = Field(ge=0, description="Lucro máximo em R$")
    consumo: ConsumoIngredientes = Field(description="Consumo real por ingrediente em kg")
    status: str = Field(description="Status retornado pelo solver")

    model_config = {
        "json_schema_extra": {
            "example": {
                "mucarela": 8, "calabresa": 6, "lucro": 310.0,
                "consumo": {"massa": 7.0, "queijo": 3.6, "molho": 2.8, "calabresa": 0.9},
                "status": "Optimal"
            }
        }
    }


class ExplainResponse(BaseModel):
    """
    Resposta retornada pelo endpoint /api/explicar.

    Contém o texto gerado pelo Claude em português brasileiro,
    explicando o resultado da otimização em linguagem natural.
    """

    explicacao: str = Field(description="Explicação em linguagem natural gerada pelo Claude")

    model_config = {
        "json_schema_extra": {
            "example": {
                "explicacao": (
                    "Com base nos ingredientes disponíveis, a melhor combinação "
                    "é produzir 8 pizzas de muçarela e 6 de calabresa, gerando "
                    "um lucro máximo de R$ 310,00."
                )
            }
        }
    }
