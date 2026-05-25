<!--
  [DOC-F02] components/ResultCard.vue
  -------------------------------------
  Exibe o resultado da otimização com destaque visual.

  Responsabilidades:
  - Estado vazio: placeholder enquanto nenhum cálculo foi realizado
  - Estado de carregamento: skeleton durante a requisição
  - Estado de erro: mensagem amigável com ícone
  - Estado de sucesso: quantidade de cada pizza + lucro máximo em destaque
  - Badge de status do solver (Optimal / Feasible)

  Dados exibidos (vindos do store):
  - Pizzas de Muçarela (qtd)
  - Pizzas de Calabresa (qtd)
  - Total de pizzas produzidas
  - Lucro máximo em R$
  - Status do solver
-->

<template>
  <div class="card">
    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg flex items-center justify-center"
             style="background: rgba(16,185,129,0.15);">
          <ChartBar :size="20" style="color: var(--color-brand)" />
        </div>
        <div>
          <h2 class="text-base font-semibold" style="color: var(--color-text-primary)">
            Resultado Ótimo
          </h2>
          <p class="text-xs" style="color: var(--color-text-muted)">
            Produção que maximiza o lucro
          </p>
        </div>
      </div>

      <!-- Badge de status -->
      <span
        v-if="store.hasResult"
        class="text-xs font-medium px-2 py-1 rounded-full"
        :style="{
          background: store.result.status === 'Optimal'
            ? 'rgba(16,185,129,0.15)'
            : 'rgba(245,158,11,0.15)',
          color: store.result.status === 'Optimal'
            ? 'var(--color-brand)'
            : 'var(--color-warning)',
        }"
      >
        {{ store.result.status }}
      </span>
    </div>

    <!-- Estado: carregando -->
    <div v-if="store.loading.optimize" class="space-y-3">
      <div v-for="i in 3" :key="i"
           class="h-16 rounded-lg animate-pulse"
           style="background: var(--color-surface-line);" />
    </div>

    <!-- Estado: erro -->
    <div
      v-else-if="store.error && !store.hasResult"
      class="flex flex-col items-center gap-3 py-8 text-center"
    >
      <AlertCircle :size="32" style="color: var(--color-error)" />
      <p class="text-sm" style="color: var(--color-error)">{{ store.error }}</p>
      <p class="text-xs" style="color: var(--color-text-muted)">
        Verifique os estoques informados e tente novamente.
      </p>
    </div>

    <!-- Estado: vazio (sem resultado ainda) -->
    <div
      v-else-if="!store.hasResult"
      class="flex flex-col items-center gap-3 py-8 text-center"
    >
      <Pizza :size="40" style="color: var(--color-text-muted)" />
      <p class="text-sm" style="color: var(--color-text-secondary)">
        Informe os estoques e clique em<br>
        <strong style="color: var(--color-brand)">Calcular Produção Ótima</strong>
      </p>
    </div>

    <!-- Estado: resultado disponível -->
    <div v-else class="space-y-4">

      <!-- Lucro máximo — destaque principal -->
      <div
        class="rounded-xl p-4 text-center"
        style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3);"
      >
        <p class="text-xs font-medium uppercase tracking-wider mb-1"
           style="color: var(--color-brand)">
          Lucro Máximo
        </p>
        <p class="text-4xl font-bold" style="color: var(--color-brand)">
          R$ {{ formatCurrency(store.result.lucro) }}
        </p>
        <p class="text-xs mt-1" style="color: var(--color-text-muted)">
          {{ store.totalPizzas }} pizzas produzidas no total
        </p>
      </div>

      <!-- Detalhamento por sabor -->
      <div class="grid grid-cols-2 gap-3">
        <!-- Muçarela -->
        <div
          class="rounded-lg p-3 text-center"
          style="background: var(--color-surface); border: 1px solid var(--color-surface-line);"
        >
          <p class="text-2xl mb-1">🍕</p>
          <p class="text-2xl font-bold" style="color: var(--color-text-primary)">
            {{ store.result.mucarela }}
          </p>
          <p class="text-xs" style="color: var(--color-text-muted)">Muçarela</p>
          <p class="text-xs font-medium mt-1" style="color: var(--color-brand)">
            R$ {{ formatCurrency(store.result.mucarela * 20) }}
          </p>
        </div>

        <!-- Calabresa -->
        <div
          class="rounded-lg p-3 text-center"
          style="background: var(--color-surface); border: 1px solid var(--color-surface-line);"
        >
          <p class="text-2xl mb-1">🍕</p>
          <p class="text-2xl font-bold" style="color: var(--color-text-primary)">
            {{ store.result.calabresa }}
          </p>
          <p class="text-xs" style="color: var(--color-text-muted)">Calabresa</p>
          <p class="text-xs font-medium mt-1" style="color: var(--color-brand)">
            R$ {{ formatCurrency(store.result.calabresa * 25) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ChartBar, AlertCircle, Pizza } from 'lucide-vue-next'
import { useOptimizerStore } from '../stores/optimizer'

const store = useOptimizerStore()

/** Formata número como moeda brasileira (ex: 310,00) */
function formatCurrency(value) {
  return Number(value).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}
</script>
