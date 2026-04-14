<script setup>
import { onMounted, ref } from 'vue';
import Upload from './components/Upload.vue';
import DocumentList from './components/DocumentList.vue';
import Chat from './components/Chat.vue';
import ChunkPreview from './components/ChunkPreview.vue';
import { listDocuments } from './services/api.js';

const docs = ref([]);
const selected = ref([]);
const loadError = ref('');
const previewSource = ref(null);

async function refresh() {
  try {
    docs.value = await listDocuments();
  } catch (e) {
    loadError.value = e.message;
  }
}

function onUploaded(info) {
  refresh();
}
function onToggle(id) {
  const i = selected.value.indexOf(id);
  if (i === -1) selected.value.push(id);
  else selected.value.splice(i, 1);
}
function onDeleted(id) {
  docs.value = docs.value.filter((d) => d.doc_id !== id);
  selected.value = selected.value.filter((x) => x !== id);
}
function onClear() { selected.value = []; }

onMounted(refresh);
</script>

<template>
  <div class="app">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-logo"></div>
        <div>
          <div class="brand-name">ChainMain</div>
          <div class="brand-sub">Chat with your documents</div>
        </div>
      </div>

      <Upload @uploaded="onUploaded" />

      <DocumentList
        :documents="docs"
        :selected="selected"
        @toggle="onToggle"
        @deleted="onDeleted"
        @clear="onClear"
      />

      <div v-if="loadError" class="err">{{ loadError }}</div>
    </aside>

    <main class="main">
      <Chat :selected-doc-ids="selected" @preview="(s) => previewSource = s" />
    </main>

    <ChunkPreview :source="previewSource" @close="previewSource = null" />
  </div>
</template>

<style scoped>
.err { color: var(--danger); font-size: 12px; }
</style>
