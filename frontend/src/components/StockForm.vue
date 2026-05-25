<!--
  [DOC-F01] components/StockForm.vue
  ------------------------------------
  Formulário de entrada dos estoques de ingredientes.

  Responsabilidades:
  - Renderizar 4 inputs numéricos editáveis (massa, queijo, molho, calabresa)
  - Pré-preencher com os valores padrão do enunciado (imagem)
  - Validar: impede valores negativos antes de submeter
  - Emitir ação de otimização via store Pinia ao clicar em "Calcular"
  - Exibir spinner e desabilitar botão durante o carregamento

  Componentes PrimeVue utilizados:
  - InputNumber  → input numérico com controle de min/step/decimais
  - Button       → botão de submit com ícone e estado de loading
-->

<template>
  <div class="card">
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3 mb-6">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center"
           style="background-color: var(--color-brand); opacity: 0.15; position: absolute;"/>
      <div class="w-10 h-10 rounded-lg flex items-center justify-center relative"
           style="background: rgba(16,185,129,0.15);">
        <PackageOpen :size="20" style="color: var(--color-brand)" />
      </div>
      <div>
        <h2 class="text-base font-semibold" style="color: var(--color-text-primary)">
          Estoque de Ingredientes
        </h2>
        <p class="text-xs" style="color: var(--color-text-muted)">
          Informe a quantidade disponível de cada ingrediente
        </p>
      </div>
    </div>

    <!-- Inputs de ingredientes -->
    <div class="grid grid-cols-1 gap-4 mb-6">
      <div
        v-for="field in fields"
        :key="field.key"
        class="flex items-center justify-between gap-4 p-3 rounded-lg"
        style="background: rgba(255,255,255,0.03); border: 1px solid var(--color-surface-line);"
      >
        <!-- Ícone + label -->
        <div class="flex items-center gap-3 min-w-0">
          <span class="text-xl">{{ field.emoji }}</span>
          <div>
            <p class="text-sm font-medium" style="color: var(--color-text-primary)">
              {{ field.label }}
            </p>
            <p class="text-xs" style="color: var(--color-text-muted)">kg disponíveis</p>
          </div>
        </div>

        <!-- Input numérico -->
        <input
          type="number"
          :min="0"
          :step="0.1"
          v-model.number="store.stock[field.key]"
          class="w-24 text-right text-sm font-mono rounded-md px-3 py-2 outline-none focus:ring-2"
          style="
            background: var(--color-surface);
            border: 1px solid var(--color-surface-line);
            color: var(--color-text-primary);
            --tw-ring-color: var(--color-brand);
          "
          @input="store.resetResult()"
        />
      </div>
    </div>

    <!-- Botão calcular -->
    <button
      @click="handleCalcular"
      :disabled="store.loading.optimize || hasNegativeStock"
      class="w-full py-3 px-6 rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition-all duration-200"
      :style="{
        background: store.loading.optimize || hasNegativeStock
          ? 'var(--color-surface-line)'
          : 'var(--color-brand)',
        color: store.loading.optimize || hasNegativeStock
          ? 'var(--color-text-muted)'
          : '#fff',
        cursor: store.loading.optimize || hasNegativeStock ? 'not-allowed' : 'pointer',
      }"
    >
      <span v-if="store.loading.optimize" class="spinner" style="width:1rem; height:1rem;" />
      <TrendingUp v-else :size="16" />
      {{ store.loading.optimize ? 'Calculando...' : 'Calcular Produção Ótima' }}
    </button>

    <!-- Aviso de estoque negativo -->
    <p
      v-if="hasNegativeStock"
      class="text-xs text-center mt-2"
      style="color: var(--color-error)"
    >
      ⚠ Nenhum valor pode ser negativo
    </p>
  </div>
</template>

<script setup>
/**
 * Script Setup — StockForm.vue
 *
 * Usa o store Pinia para leitura e escrita dos estoques.
 * A action runOptimizer() é chamada diretamente — sem props ou emits,
 * pois o estado é compartilhado globalmente via store.
 */
import { computed } from 'vue'
import { PackageOpen, TrendingUp } from 'lucide-vue-next'
import { useOptimizerStore } from '../stores/optimizer'

const store = useOptimizerStore()

/** Mapeamento dos campos com metadados para renderização dinâmica */
const fields = [
  { key: 'massa',     label: 'Massa',     emoji: '🍚' },
  { key: 'queijo',    label: 'Queijo',    emoji: '🧀' },
  { key: 'molho',     label: 'Molho',     emoji: '🍅' },
  { key: 'calabresa', label: 'Calabresa', emoji: '🌶️' },
]

/** true se qualquer campo estiver com valor negativo */
const hasNegativeStock = computed(() =>
  Object.values(store.stock).some((v) => v < 0)
)

/** Dispara a otimização via store */
async function handleCalcular() {
  if (hasNegativeStock.value) return
  await store.runOptimizer()
}
</script>
