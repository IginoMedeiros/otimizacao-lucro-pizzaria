/**
 * [DOC-F06] services/api.js
 * --------------------------
 * Camada de comunicação HTTP entre o frontend Vue e o backend FastAPI.
 *
 * Em desenvolvimento (local): usa proxy do Vite → /api → localhost:8000
 * Em produção (Vercel):       usa VITE_API_BASE_URL definida nas env vars
 *
 * Métodos:
 * - postOptimize(stock)  → POST /api/otimizar
 * - postExplain(result)  → POST /api/explicar
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL
  ? `${import.meta.env.VITE_API_BASE_URL}/api`
  : '/api'

async function postJSON(path, body) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    let mensagem = `Erro ${response.status}`
    try {
      const erro = await response.json()
      mensagem = erro.detail ?? mensagem
    } catch { /* ignora se corpo não for JSON */ }
    throw new Error(mensagem)
  }

  return response.json()
}

export async function postOptimize(stock) {
  return postJSON('/otimizar', stock)
}

export async function postExplain(result) {
  return postJSON('/explicar', result)
}
