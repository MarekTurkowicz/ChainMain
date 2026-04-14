<script setup>
import { deleteDocument } from '../services/api.js';

const props = defineProps({
  documents: { type: Array, required: true },
  selected: { type: Array, required: true },
});
const emit = defineEmits(['toggle', 'deleted', 'clear']);

function onToggle(doc) { emit('toggle', doc.doc_id); }

async function onDelete(doc, ev) {
  ev.stopPropagation();
  if (!confirm(`Delete "${doc.filename}"?`)) return;
  await deleteDocument(doc.doc_id);
  emit('deleted', doc.doc_id);
}
</script>

<template>
  <div class="docs">
    <div class="head">
      <h2>Documents</h2>
      <button
        v-if="selected.length"
        class="clear"
        @click="emit('clear')"
        title="Clear filter — search all documents"
      >
        Clear filter
      </button>
    </div>

    <div v-if="!documents.length" class="empty">No documents yet.</div>

    <ul class="list">
      <li
        v-for="doc in documents"
        :key="doc.doc_id"
        :class="{ selected: selected.includes(doc.doc_id) }"
        @click="onToggle(doc)"
        data-testid="doc-item"
      >
        <div class="row">
          <input
            type="checkbox"
            :checked="selected.includes(doc.doc_id)"
            @click.stop
            @change="onToggle(doc)"
          />
          <div class="meta">
            <div class="name" :title="doc.filename">{{ doc.filename }}</div>
            <div class="sub">{{ doc.chunk_count }} chunks</div>
          </div>
          <button class="del" @click="onDelete(doc, $event)" title="Delete">×</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.docs { display: flex; flex-direction: column; gap: 8px; min-height: 0; }
.head { display: flex; align-items: center; justify-content: space-between; }
.clear {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 4px;
}
.empty {
  color: var(--text-mute);
  font-size: 12px;
  padding: 6px 2px;
}
.list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.list li {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px 10px;
  cursor: pointer;
  transition: border-color var(--t), background var(--t);
}
.list li:hover { border-color: var(--border-strong); }
.list li.selected {
  border-color: var(--accent);
  background: var(--surface-2);
}
.row { display: flex; align-items: center; gap: 10px; }
.meta { flex: 1; min-width: 0; }
.name {
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sub { color: var(--text-mute); font-size: 11px; }
.del {
  background: transparent;
  border: none;
  color: var(--text-mute);
  padding: 2px 6px;
  font-size: 16px;
  line-height: 1;
}
.del:hover { color: var(--danger); transform: none; }
input[type="checkbox"] { width: auto; accent-color: var(--accent); }
</style>
