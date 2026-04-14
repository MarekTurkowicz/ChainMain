<script setup>
import { ref } from 'vue';
import { uploadFile } from '../services/api.js';

const emit = defineEmits(['uploaded']);

const dragover = ref(false);
const busy = ref(false);
const error = ref('');
const input = ref(null);

async function handleFiles(fileList) {
  if (!fileList || !fileList.length) return;
  error.value = '';
  busy.value = true;
  try {
    for (const f of fileList) {
      const info = await uploadFile(f);
      emit('uploaded', info);
    }
  } catch (e) {
    error.value = e.message || 'Upload failed';
  } finally {
    busy.value = false;
    if (input.value) input.value.value = '';
  }
}

function onDrop(e) {
  e.preventDefault();
  dragover.value = false;
  handleFiles(Array.from(e.dataTransfer.files));
}

function onPick() { input.value?.click(); }
</script>

<template>
  <div class="upload">
    <h2>Upload</h2>
    <div
      class="dropzone"
      :class="{ dragover, busy }"
      @dragover.prevent="dragover = true"
      @dragleave.prevent="dragover = false"
      @drop="onDrop"
      @click="onPick"
      data-testid="dropzone"
    >
      <div class="hint">
        <strong>Drop</strong> PDF or TXT here
        <div class="sub">or click to browse</div>
      </div>
      <input
        ref="input"
        type="file"
        accept=".pdf,.txt"
        multiple
        hidden
        data-testid="file-input"
        @change="handleFiles(Array.from($event.target.files))"
      />
    </div>
    <div class="progress" :class="{ active: busy }"></div>
    <div v-if="error" class="err">{{ error }}</div>
  </div>
</template>

<style scoped>
.upload { display: flex; flex-direction: column; gap: 8px; }
.dropzone {
  border: 1px dashed var(--border-strong);
  border-radius: var(--radius);
  background: var(--surface);
  padding: 18px 14px;
  text-align: center;
  cursor: pointer;
  transition: border-color var(--t), background var(--t), transform var(--t);
}
.dropzone:hover { border-color: var(--accent); }
.dropzone.dragover {
  border-color: var(--accent);
  background: var(--surface-2);
  transform: scale(1.01);
}
.dropzone.busy { opacity: 0.75; cursor: progress; }
.hint strong { color: var(--text); }
.hint .sub {
  color: var(--text-mute);
  font-size: 12px;
  margin-top: 3px;
}
.err {
  color: var(--danger);
  font-size: 12px;
}
</style>
