<!--
  [DOC-F04] components/ExplainPanel.vue
  ---------------------------------------
  Painel de explicação do resultado gerado pelo Claude.

  Responsabilidades:
  - Exibir botão "Explicar Resultado" apenas quando há resultado calculado
  - Chamar store.fetchExplanation() ao clicar — única ação que consome tokens Claude
  - Mostrar spinner durante a chamada à API Claude
  - Renderizar o texto explicativo em PT-BR com formatação suave
  - Exibir erro específico se a chamada falhar (ex: chave inválida)
  - Esconder o botão após a explicação ser gerada (evita chamadas duplicadas)

  Estratégia de tokens:
  - Só é ativado por ação explícita do usuário
  - Nunca é chamado automaticamente
  - A explicação fica em cache no store durante a sessão
-->

<template>
  <div class="card" v-if="store.hasResult">
    <!-- Explicação ainda não solicitada -->
    <div v-if="!store.hasExplanation && !store.loading.explain">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-lg flex items-center justify-center"
             style="background: rgba(99,102,241,0.15);">
          <Sparkles :size="20" style="color: #818cf8" />
        </div>
        <div>
          <h2 class="text-base font-semibold" style="color: var(--color-text-primary)">
            Explicação com IA
          </h2>
          <p class="text-xs" style="color: var(--color-text-muted)">
            Claude explica o resultado em linguagem simples
          </p>
        </div>
      </div>

      <button
        @click="store.fetchExplanation()"
        class="w-full py-2.5 px-4 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-all duration-200"
        style="
          background: rgba(99,102,241,0.15);
          border: 1px solid rgba(99,102,241,0.3);
          color: #818cf8;
        "
        @mouseover="($event.currentTarget.style.background = 'rgba(99,102,241,0.25)')"
        @mouseleave="($event.currentTarget.style.background = 'rgba(99,102,241,0.15)')"
      >
        <Sparkles :size="14" />
        Explicar Resultado
      </button>
    </div>

    <!-- Carregando explicação -->
    <div
      v-else-if="store.loading.explain"
      class="flex items-center gap-3 py-4"
    >
      <span class="spinner" />
      <p class="text-sm" style="color: var(--color-text-secondary)">
        Claude está gerando a explicação...
      </p>
    </div>

    <!-- Explicação disponível -->
    <div v-else-if="store.hasExplanation">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-lg flex items-center justify-center"
             style="background: rgba(99,102,241,0.15);">
          <Sparkles :size="20" style="color: #818cf8" />
        </div>
        <div>
          <h2 class="text-base font-semibold" style="color: var(--color-text-primary)">
            Explicação com IA
          </h2>
          <p class="text-xs" style="color: var(--color-text-muted)">Gerado pelo Claude</p>
        </div>
      </div>

      <div
        class="rounded-lg p-4 text-sm leading-relaxed"
        style="
          background: rgba(99,102,241,0.08);
          border: 1px solid rgba(99,102,241,0.2);
          color: var(--color-text-secondary);
        "
      >
        {{ store.explanation }}
      </div>
    </div>

    <!-- Erro ao buscar explicação -->
    <div v-else-if="store.error" class="flex items-center gap-3 py-2">
      <AlertCircle :size="18" style="color: var(--color-error); flex-shrink: 0;" />
      <p class="text-xs" style="color: var(--color-error)">{{ store.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { Sparkles, AlertCircle } from 'lucide-vue-next'
import { useOptimizerStore } from '../stores/optimizer'

const store = useOptimizerStore()
</script>
