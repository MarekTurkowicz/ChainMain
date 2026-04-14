<script setup>
import { ref, watch } from 'vue';
import { getChunk } from '../services/api.js';

const props = defineProps({
  source: { type: Object, default: null }, // { chunk_id, filename, page, ... } or null
});
const emit = defineEmits(['close']);

const loading = ref(false);
const error = ref('');
const target = ref(null);
const neighbors = ref([]);

watch(
  () => props.source?.chunk_id,
  async (chunkId) => {
    if (!chunkId) {
      target.value = null;
      neighbors.value = [];
      error.value = '';
      return;
    }
    loading.value = true;
    error.value = '';
    try {
      const data = await getChunk(chunkId, 2);
      target.value = data.target;
      neighbors.value = data.neighbors;
    } catch (e) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  },
  { immediate: true },
);

function ordered() {
  if (!target.value) return [];
  return [...neighbors.value, target.value].sort((a, b) => a.chunk_index - b.chunk_index);
}

function onBackdrop() { emit('close'); }
function onPanelClick(e) { e.stopPropagation(); }
</script>

<template>
  <div v-if="source" class="backdrop" @click="onBackdrop" data-testid="chunk-preview-backdrop">
    <aside class="panel" @click.stop>
      <header class="head">
        <div class="title">
          <div class="file">{{ source.filename }}</div>
          <div v-if="source.page" class="page">page {{ source.page }}</div>
        </div>
        <button class="close" @click="emit('close')" aria-label="Close">×</button>
      </header>

      <div class="body">
        <div v-if="loading" class="state">Loading…</div>
        <div v-else-if="error" class="state err">{{ error }}</div>
        <div v-else-if="!target" class="state">Chunk not found.</div>
        <template v-else>
          <div
            v-for="c in ordered()"
            :key="c.chunk_id"
            class="chunk"
            :class="{ target: c.is_target }"
          >
            <div class="meta">
              <span class="idx">#{{ c.chunk_index }}</span>
              <span v-if="c.page" class="pg">p.{{ c.page }}</span>
              <span v-if="c.is_target" class="badge">match</span>
            </div>
            <div class="text">{{ c.text }}</div>
          </div>
        </template>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: flex-end;
  z-index: 50;
  animation: fade var(--t) ease;
}
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }

.panel {
  width: min(560px, 92vw);
  height: 100%;
  background: var(--bg-2);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  box-shadow: -8px 0 24px rgba(0, 0, 0, 0.35);
  animation: slide var(--t) ease;
}
@keyframes slide { from { transform: translateX(20px); } to { transform: translateX(0); } }

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--border);
}
.title .file { font-weight: 600; font-size: 14px; }
.title .page { font-size: 12px; color: var(--text-mute); margin-top: 2px; }
.close {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
}
.close:hover { border-color: var(--accent); }

.body {
  overflow-y: auto;
  padding: 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.state { color: var(--text-mute); font-size: 13px; padding: 8px 0; }
.state.err { color: var(--danger); }

.chunk {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
}
.chunk.target {
  border-color: var(--accent);
  background: linear-gradient(135deg, rgba(122,162,255,0.10), rgba(181,139,255,0.06));
}
.meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 11px;
  color: var(--text-mute);
  margin-bottom: 6px;
}
.badge {
  background: var(--accent);
  color: #0b0d10;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 10px;
}
.text {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px;
  white-space: pre-wrap;
  color: var(--text-dim);
  line-height: 1.5;
}
</style>
