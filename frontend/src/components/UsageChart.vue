<!--
  [DOC-F03] components/UsageChart.vue
  -------------------------------------
  Gráfico de barras comparando consumo real vs estoque disponível.

  Responsabilidades:
  - Renderizar gráfico de barras agrupadas por ingrediente
  - Eixo X: ingredientes (Massa, Queijo, Molho, Calabresa)
  - Eixo Y: quantidade em kg
  - Barra verde: estoque disponível informado pelo usuário
  - Barra laranja: consumo real calculado pelo solver
  - Oculto quando não há resultado calculado

  Biblioteca: Chart.js via vue-chartjs
  O gráfico é destruído e recriado reativamente quando o resultado muda.
-->

<template>
  <div class="card" v-if="store.hasResult">
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3 mb-5">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center"
           style="background: rgba(16,185,129,0.15);">
        <BarChart2 :size="20" style="color: var(--color-brand)" />
      </div>
      <div>
        <h2 class="text-base font-semibold" style="color: var(--color-text-primary)">
          Consumo de Ingredientes
        </h2>
        <p class="text-xs" style="color: var(--color-text-muted)">
          Disponível vs utilizado (em kg)
        </p>
      </div>
    </div>

    <!-- Legenda customizada -->
    <div class="flex items-center gap-4 mb-4">
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-sm" style="background: rgba(16,185,129,0.7);" />
        <span class="text-xs" style="color: var(--color-text-secondary)">Disponível</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-sm" style="background: rgba(245,158,11,0.8);" />
        <span class="text-xs" style="color: var(--color-text-secondary)">Utilizado</span>
      </div>
    </div>

    <!-- Gráfico -->
    <div style="position: relative; height: 200px;">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
/**
 * Script Setup — UsageChart.vue
 *
 * Constrói os dados do Chart.js de forma reativa usando computed().
 * Quando store.result muda, chartData é recalculado automaticamente
 * e o gráfico é atualizado pelo vue-chartjs.
 */
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'
import { BarChart2 } from 'lucide-vue-next'
import { useOptimizerStore } from '../stores/optimizer'

// Registrar componentes necessários do Chart.js
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const store = useOptimizerStore()

/** Labels e chaves dos ingredientes para o gráfico */
const ingredientes = [
  { label: 'Massa',     key: 'massa' },
  { label: 'Queijo',    key: 'queijo' },
  { label: 'Molho',     key: 'molho' },
  { label: 'Calabresa', key: 'calabresa' },
]

/** Dados reativos do gráfico — recalculados quando result muda */
const chartData = computed(() => ({
  labels: ingredientes.map((i) => i.label),
  datasets: [
    {
      label: 'Disponível (kg)',
      data: ingredientes.map((i) => store.stock[i.key] ?? 0),
      backgroundColor: 'rgba(16, 185, 129, 0.6)',
      borderColor: 'rgba(16, 185, 129, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
    {
      label: 'Utilizado (kg)',
      data: ingredientes.map((i) => store.result?.consumo?.[i.key] ?? 0),
      backgroundColor: 'rgba(245, 158, 11, 0.7)',
      borderColor: 'rgba(245, 158, 11, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
  ],
}))

/** Opções de estilo do gráfico — tema escuro */
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }, // legenda customizada no template
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#f1f5f9',
      bodyColor: '#94a3b8',
      borderColor: '#334155',
      borderWidth: 1,
      callbacks: {
        label: (ctx) => ` ${ctx.dataset.label}: ${ctx.parsed.y} kg`,
      },
    },
  },
  scales: {
    x: {
      ticks: { color: '#94a3b8', font: { size: 11 } },
      grid: { color: 'rgba(51, 65, 85, 0.5)' },
    },
    y: {
      ticks: {
        color: '#94a3b8',
        font: { size: 11 },
        callback: (v) => `${v} kg`,
      },
      grid: { color: 'rgba(51, 65, 85, 0.5)' },
      beginAtZero: true,
    },
  },
}
</script>
