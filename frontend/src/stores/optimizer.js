/**
 * [DOC-F05] stores/optimizer.js
 * -------------------------------
 * Store Pinia — gerenciamento de estado global da aplicação.
 *
 * Responsabilidades:
 * - Centralizar todos os estados reativos da aplicação
 * - Expor actions que chamam a camada de serviço (api.js)
 * - Calcular valores derivados (getters) prontos para uso nos componentes
 *
 * Estados:
 * - stock       → valores atuais dos inputs de estoque (editados pelo usuário)
 * - result      → resposta da última otimização executada
 * - explanation → texto gerado pelo Claude (null até ser solicitado)
 * - loading     → controla exibição de spinners nos componentes
 * - error       → mensagem de erro a ser exibida (null se sem erro)
 *
 * Actions:
 * - runOptimizer()      → chama POST /api/otimizar com o stock atual
 * - fetchExplanation()  → chama POST /api/explicar com o result atual
 * - resetResult()       → limpa resultado e explicação
 *
 * Getters:
 * - hasResult     → true se há resultado calculado
 * - hasExplanation → true se há explicação gerada
 * - totalPizzas   → soma de muçarela + calabresa
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { postOptimize, postExplain } from '../services/api'

export const useOptimizerStore = defineStore('optimizer', () => {

  // -------------------------------------------------------------------------
  // Estado
  // -------------------------------------------------------------------------

  /** Estoques de ingredientes — valores padrão do enunciado (imagem) */
  const stock = ref({
    massa: 10.0,
    queijo: 5.0,
    molho: 4.0,
    calabresa: 2.0,
  })

  /** Resultado da última otimização (null até ser executada) */
  const result = ref(null)

  /** Explicação gerada pelo Claude (null até ser solicitada) */
  const explanation = ref(null)

  /** Estado de carregamento — { optimize: bool, explain: bool } */
  const loading = ref({ optimize: false, explain: false })

  /** Mensagem de erro atual (null se sem erro) */
  const error = ref(null)

  // -------------------------------------------------------------------------
  // Getters (computed)
  // -------------------------------------------------------------------------

  /** true se há resultado de otimização disponível */
  const hasResult = computed(() => result.value !== null)

  /** true se há explicação do Claude disponível */
  const hasExplanation = computed(() => explanation.value !== null)

  /** Total de pizzas a produzir (muçarela + calabresa) */
  const totalPizzas = computed(() =>
    hasResult.value
      ? result.value.mucarela + result.value.calabresa
      : 0
  )

  // -------------------------------------------------------------------------
  // Actions
  // -------------------------------------------------------------------------

  /**
   * Envia os estoques atuais ao backend e armazena a solução ótima.
   * Limpa resultado e explicação anteriores antes de executar.
   */
  async function runOptimizer() {
    loading.value.optimize = true
    error.value = null
    result.value = null
    explanation.value = null

    try {
      result.value = await postOptimize(stock.value)
    } catch (err) {
      error.value = err.message ?? 'Erro ao calcular a otimização.'
    } finally {
      loading.value.optimize = false
    }
  }

  /**
   * Solicita explicação do resultado atual ao Claude via backend.
   * Só deve ser chamada após runOptimizer() ter retornado um resultado.
   * A explicação fica em cache no store — nova chamada só ocorre se
   * o resultado mudar (resultado limpo no próximo runOptimizer).
   */
  async function fetchExplanation() {
    if (!hasResult.value) return

    loading.value.explain = true
    error.value = null

    try {
      const payload = {
        mucarela: result.value.mucarela,
        calabresa: result.value.calabresa,
        lucro: result.value.lucro,
        consumo: result.value.consumo,
      }
      const response = await postExplain(payload)
      explanation.value = response.explicacao
    } catch (err) {
      error.value = err.message ?? 'Erro ao gerar explicação.'
    } finally {
      loading.value.explain = false
    }
  }

  /**
   * Reseta resultado e explicação sem alterar os inputs de estoque.
   * Útil para permitir nova otimização com os mesmos ou novos valores.
   */
  function resetResult() {
    result.value = null
    explanation.value = null
    error.value = null
  }

  // -------------------------------------------------------------------------
  // Expose
  // -------------------------------------------------------------------------
  return {
    // Estado
    stock,
    result,
    explanation,
    loading,
    error,
    // Getters
    hasResult,
    hasExplanation,
    totalPizzas,
    // Actions
    runOptimizer,
    fetchExplanation,
    resetResult,
  }
})
