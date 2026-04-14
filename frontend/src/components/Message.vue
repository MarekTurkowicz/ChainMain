<script setup>
import { ref } from 'vue';

defineProps({
  role: { type: String, required: true },   // 'user' | 'assistant'
  text: { type: String, required: true },
  sources: { type: Array, default: () => [] },
  streaming: { type: Boolean, default: false },
});

const expanded = ref({});
function toggle(i) { expanded.value[i] = !expanded.value[i]; }
</script>

<template>
  <div class="msg" :class="role" data-testid="message">
    <div class="bubble">
      <div class="text">
        {{ text }}<span v-if="streaming" class="cursor">▍</span>
      </div>

      <div v-if="sources.length" class="sources">
        <div class="s-head">Sources</div>
        <div class="s-list">
          <div
            v-for="(s, i) in sources"
            :key="s.chunk_id || i"
            class="s-item"
            @click="toggle(i)"
            data-testid="source-chip"
          >
            <div class="s-title">
              <span class="tag">[{{ i + 1 }}]</span>
              <span class="file">{{ s.filename }}</span>
              <span v-if="s.page" class="page">p.{{ s.page }}</span>
              <span v-if="s.score != null" class="score">{{ Math.round(s.score * 100) }}%</span>
            </div>
            <div v-if="expanded[i]" class="s-body">{{ s.text }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.msg {
  display: flex;
  padding: 6px 0;
}
.msg.user { justify-content: flex-end; }

.bubble {
  max-width: 80%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
  box-shadow: var(--shadow);
}
.msg.user .bubble {
  background: linear-gradient(135deg, rgba(122,162,255,0.15), rgba(181,139,255,0.12));
  border-color: rgba(122,162,255,0.4);
}

.text {
  white-space: pre-wrap;
  font-size: 14px;
}

.cursor {
  display: inline-block;
  margin-left: 2px;
  animation: blink 900ms steps(2) infinite;
  color: var(--accent);
}
@keyframes blink { to { opacity: 0; } }

.sources { margin-top: 10px; border-top: 1px solid var(--border); padding-top: 8px; }
.s-head {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-mute);
  margin-bottom: 6px;
}
.s-list { display: flex; flex-direction: column; gap: 4px; }
.s-item {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 8px;
  cursor: pointer;
  transition: border-color var(--t);
  font-size: 12px;
}
.s-item:hover { border-color: var(--accent); }
.s-title { display: flex; align-items: center; gap: 8px; }
.tag { color: var(--accent); font-weight: 600; }
.file { color: var(--text); }
.page, .score { color: var(--text-mute); font-size: 11px; }
.score { margin-left: auto; }
.s-body {
  margin-top: 6px;
  color: var(--text-dim);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11.5px;
  white-space: pre-wrap;
  max-height: 220px;
  overflow: auto;
}
</style>
