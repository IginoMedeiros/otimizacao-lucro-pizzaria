"""
[DOC-B04] services/claude_service.py
--------------------------------------
Integração assíncrona com a API da Anthropic (Claude).

Responsabilidades:
- Montar um prompt compacto (~80 tokens de input) com os dados do resultado
- Chamar a API Claude de forma assíncrona usando httpx
- Extrair e retornar apenas o texto da explicação gerada
- Só é invocado quando o usuário clicar em "Explicar Resultado" no frontend

Estratégia de economia de tokens:
- O modelo recebe apenas os dados numéricos do resultado já calculado
- Não recebe contexto do problema, histórico ou instruções longas
- Prompt estruturado e fixo — apenas os valores mudam por chamada
- Modelo utilizado: claude-sonnet-4-20250514 (melhor custo-benefício)

Variáveis de ambiente necessárias:
- ANTHROPIC_API_KEY: chave da API Anthropic (definida no .env)
"""

import os
import httpx
from schemas.models import ExplainRequest, ExplainResponse


# ---------------------------------------------------------------------------
# CONSTANTES
# ---------------------------------------------------------------------------

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 300  # suficiente para um parágrafo explicativo


# ---------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ---------------------------------------------------------------------------

async def gerar_explicacao(dados: ExplainRequest) -> ExplainResponse:
    """
    Gera uma explicação em linguagem natural do resultado da otimização
    utilizando a API Claude de forma assíncrona.

    O prompt é mantido compacto, passando apenas os valores numéricos
    necessários para a explicação — sem contexto redundante.

    Parâmetros:
        dados (ExplainRequest): resultado da otimização (quantidades, lucro, consumo)

    Retorna:
        ExplainResponse: objeto com o campo `explicacao` em PT-BR

    Raises:
        httpx.HTTPStatusError: se a API retornar erro HTTP
        KeyError: se a resposta da API vier em formato inesperado
        EnvironmentError: se ANTHROPIC_API_KEY não estiver definida
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY não definida. "
            "Verifique o arquivo .env na raiz do projeto."
        )

    # ------------------------------------------------------------------
    # Montar prompt compacto — apenas dados numéricos relevantes
    # ------------------------------------------------------------------
    prompt = (
        f"Pizzaria otimizou produção: {dados.mucarela} pizzas de muçarela e "
        f"{dados.calabresa} de calabresa. Lucro máximo: R${dados.lucro:.2f}. "
        f"Consumo: massa={dados.consumo.get('massa', 0)}kg, "
        f"queijo={dados.consumo.get('queijo', 0)}kg, "
        f"molho={dados.consumo.get('molho', 0)}kg, "
        f"calabresa={dados.consumo.get('calabresa', 0)}kg. "
        "Explique este resultado em 2 frases simples em português."
    )

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    # ------------------------------------------------------------------
    # Chamada assíncrona à API — timeout de 30s para não travar o server
    # ------------------------------------------------------------------
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            ANTHROPIC_API_URL,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

    data = response.json()

    # ------------------------------------------------------------------
    # Extrair texto da resposta
    # ------------------------------------------------------------------
    texto = data["content"][0]["text"].strip()

    return ExplainResponse(explicacao=texto)
