# 🍕 Pizza Optimizer

Sistema de otimização de produção de pizzas usando **Programação Linear Inteira (PLI)**.  
Dado o estoque de ingredientes disponíveis, calcula a combinação de pizzas de **Muçarela** e **Calabresa** que maximiza o lucro da pizzaria.

---

## Modelo Matemático

**Variáveis de decisão:**
- `x` = número de pizzas de Muçarela (inteiro, ≥ 0)
- `y` = número de pizzas de Calabresa (inteiro, ≥ 0)

**Função Objetivo:**
```
Maximizar Z = 20x + 25y
```

**Restrições:**
```
0.5x + 0.5y  ≤ massa_disponivel
0.3x + 0.2y  ≤ queijo_disponivel
0.2x + 0.2y  ≤ molho_disponivel
0.15y        ≤ calabresa_disponivel
x, y ∈ ℤ⁺
```

---

## Stack

| Camada    | Tecnologia                              |
|-----------|-----------------------------------------|
| Frontend  | Vue 3, Vite, Tailwind CSS, PrimeVue     |
| Estado    | Pinia                                   |
| Gráficos  | Chart.js + vue-chartjs                  |
| Backend   | Python 3.11, FastAPI, Uvicorn           |
| Solver    | PuLP + CBC (local, sem custo de tokens) |
| IA        | Claude (opcional, sob demanda)          |
| Containers| Docker + Docker Compose                 |

---

## Como Rodar

### Pré-requisitos
- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) v2+

### 1. Clonar e configurar

```bash
git clone https://github.com/seu-usuario/pizza-optimizer
cd pizza-optimizer
cp .env.example .env
# Editar .env com sua ANTHROPIC_API_KEY
```

### 2. Subir todos os serviços

```bash
docker compose up --build
```

### 3. Acessar

| Recurso       | URL                          |
|---------------|------------------------------|
| Aplicação     | http://localhost             |
| Swagger API   | http://localhost:8000/docs   |
| Health Check  | http://localhost:8000/health |

---

## Endpoints da API

### `POST /api/otimizar`
Calcula a produção ótima de pizzas.

**Request:**
```json
{ "massa": 10.0, "queijo": 5.0, "molho": 4.0, "calabresa": 2.0 }
```

**Response:**
```json
{
  "mucarela": 8,
  "calabresa": 6,
  "lucro": 310.0,
  "consumo": { "massa": 7.0, "queijo": 3.6, "molho": 2.8, "calabresa": 0.9 },
  "status": "Optimal"
}
```

---

### `POST /api/explicar`
Gera explicação do resultado via Claude *(requer ANTHROPIC_API_KEY)*.

**Request:**
```json
{
  "mucarela": 8, "calabresa": 6, "lucro": 310.0,
  "consumo": { "massa": 7.0, "queijo": 3.6, "molho": 2.8, "calabresa": 0.9 }
}
```

**Response:**
```json
{ "explicacao": "Com os ingredientes disponíveis, a melhor combinação..." }
```

---

## Estrutura do Projeto

```
pizza-optimizer/
├── frontend/               # Vue 3 + Vite
│   ├── src/
│   │   ├── components/     # StockForm, ResultCard, UsageChart, ExplainPanel
│   │   ├── stores/         # Pinia — estado global
│   │   ├── services/       # api.js — chamadas HTTP
│   │   └── views/          # HomeView
│   ├── nginx.conf
│   └── Dockerfile
├── backend/                # Python + FastAPI
│   ├── routers/            # optimizer.py, explainer.py
│   ├── services/           # lp_solver.py, claude_service.py
│   ├── schemas/            # models.py (Pydantic)
│   ├── tests/              # test_optimizer.py, test_routes.py
│   ├── main.py
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Estratégia de Tokens

| Operação              | Tokens consumidos |
|-----------------------|-------------------|
| Cálculo PLI (PuLP)    | **0** — local     |
| Validação (Pydantic)  | **0** — local     |
| Explicação (Claude)   | ~80 input / ~150 output — só sob demanda |
