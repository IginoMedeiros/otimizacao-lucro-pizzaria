# [DOC-D03] backend/Dockerfile
# --------------------------------
# Imagem Docker do backend FastAPI + PuLP.
#
# - Usa python:3.11-slim (imagem mínima sem pacotes desnecessários)
# - Instala dependências do requirements.txt
# - Copia o código da aplicação
# - Expõe porta 8000
# - Roda com uvicorn em modo produção (sem --reload)
#
# O solver CBC é instalado como dependência do PuLP — sem binário externo.

FROM python:3.11-slim

# Metadados
LABEL maintainer="pizza-optimizer"
LABEL description="Backend FastAPI + PuLP para otimização de pizzaria"

WORKDIR /app

# Instalar dependências do sistema necessárias para o PuLP/CBC
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python primeiro (cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

EXPOSE 8000

# Health check do container
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Inicializar servidor uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
