<script setup>
import { ref } from 'vue';
import { uploadFile } from '../services/api.js';

const emit = defineEmits(['uploaded']);

const ALLOWED_EXT = new Set(['.pdf', '.txt']);

const dragover = ref(false);
const busy = ref(false);
const toasts = ref([]);
const input = ref(null);

let toastId = 0;

function showToast(message, type = 'error') {
  const id = ++toastId;
  toasts.value.push({ id, message, type });
  setTimeout(() => dismissToast(id), 4500);
}

function dismissToast(id) {
  toasts.value = toasts.value.filter((t) => t.id !== id);
}

function getExt(filename) {
  const dot = filename.lastIndexOf('.');
  return dot === -1 ? '' : filename.slice(dot).toLowerCase();
}

async function handleFiles(fileList) {
  if (!fileList || !fileList.length) return;

  const files = Array.from(fileList);
  const invalid = files.filter((f) => !ALLOWED_EXT.has(getExt(f.name)));
  if (invalid.length) {
    const names = invalid.map((f) => f.name).join(', ');
    showToast(`Nieobsługiwany format: ${names}. Dozwolone: PDF, TXT.`);
    if (input.value) input.value.value = '';
    return;
  }

  busy.value = true;
  try {
    for (const f of files) {
      const info = await uploadFile(f);
      emit('uploaded', info);
    }
  } catch (e) {
    showToast(e.message || 'Błąd przesyłania pliku.');
  } finally {
    busy.value = false;
    if (input.value) input.value.value = '';
  }
}

function onDrop(e) {
  e.preventDefault();
  dragover.value = false;
  handleFiles(e.dataTransfer.files);
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
        @change="handleFiles($event.target.files)"
      />
    </div>

    <div class="progress" :class="{ active: busy }"></div>

    <TransitionGroup name="toast" tag="div" class="toasts">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast"
        :class="t.type"
        data-testid="upload-toast"
      >
        <span class="toast-icon">⚠</span>
        <span class="toast-msg">{{ t.message }}</span>
        <button class="toast-close" @click="dismissToast(t.id)" aria-label="Zamknij">×</button>
      </div>
    </TransitionGroup>
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

.toasts { display: flex; flex-direction: column; gap: 6px; }

.toast {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.4;
}
.toast.error {
  background: rgba(239, 68, 68, 0.10);
  border: 1px solid rgba(239, 68, 68, 0.40);
  color: var(--danger);
}
.toast-icon { flex-shrink: 0; }
.toast-msg { flex: 1; }
.toast-close {
  flex-shrink: 0;
  background: transparent;
  border: none;
  color: inherit;
  opacity: 0.6;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0 2px;
}
.toast-close:hover { opacity: 1; }

.toast-enter-active { transition: all 0.2s ease; }
.toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateY(-6px); }
.toast-leave-to   { opacity: 0; transform: translateY(-4px); }
</style>
