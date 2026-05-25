"""
[DOC-B06] main.py
------------------
Ponto de entrada da aplicação FastAPI.

Configuração CORS:
- Aceita origens definidas via variável de ambiente CORS_ORIGINS
- Fallback para localhost em desenvolvimento
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.optimizer import router as optimizer_router
from routers.explainer import router as explainer_router

load_dotenv()

app = FastAPI(
    title="Pizza Optimizer API",
    description=(
        "API de otimização de produção de pizzas usando Programação Linear Inteira. "
        "Maximiza o lucro respeitando os estoques disponíveis de ingredientes."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — lê origens do .env para funcionar tanto em dev quanto em produção
# ---------------------------------------------------------------------------
cors_env = os.getenv("CORS_ORIGINS", "")
origins_from_env = [o.strip() for o in cors_env.split(",") if o.strip()]

origins = list(set([
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
    *origins_from_env,   # adiciona URLs do Vercel vindas do .env
]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(optimizer_router)
app.include_router(explainer_router)


@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok", "versao": "1.0.0"}


@app.get("/", tags=["Sistema"])
def root():
    return {
        "mensagem": "Pizza Optimizer API está rodando.",
        "documentacao": "/docs",
        "health": "/health",
    }
