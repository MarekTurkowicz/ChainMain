<script setup>
import { nextTick, ref, watch } from 'vue';
import Message from './Message.vue';
import { askStream } from '../services/api.js';

const props = defineProps({
  selectedDocIds: { type: Array, required: true },
});

const emit = defineEmits(['preview']);

const messages = ref([]);
const input = ref('');
const busy = ref(false);
const scrollRef = ref(null);
let abort = null;

async function scrollToBottom() {
  await nextTick();
  if (scrollRef.value) scrollRef.value.scrollTop = scrollRef.value.scrollHeight;
}

function onSubmit() {
  const q = input.value.trim();
  if (!q || busy.value) return;

  messages.value.push({ role: 'user', text: q });
  const assistantMsg = { role: 'assistant', text: '', sources: [], streaming: true };
  messages.value.push(assistantMsg);
  input.value = '';
  busy.value = true;
  scrollToBottom();

  abort = askStream({
    question: q,
    docIds: props.selectedDocIds,
    onEvent: (ev) => {
      if (ev.type === 'token') {
        assistantMsg.text += ev.data;
        scrollToBottom();
      } else if (ev.type === 'sources') {
        assistantMsg.sources = ev.data;
      } else if (ev.type === 'done') {
        assistantMsg.streaming = false;
        busy.value = false;
        abort = null;
      } else if (ev.type === 'error') {
        assistantMsg.text += `\n\n⚠ ${ev.data}`;
        assistantMsg.streaming = false;
        busy.value = false;
        abort = null;
      }
    },
  });
}

function stop() {
  if (abort) {
    abort();
    abort = null;
    busy.value = false;
    const last = messages.value[messages.value.length - 1];
    if (last && last.role === 'assistant') last.streaming = false;
  }
}

function onKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    onSubmit();
  }
}

watch(messages, scrollToBottom, { deep: true });
</script>

<template>
  <div class="chat">
    <div class="scroll" ref="scrollRef">
      <div v-if="!messages.length" class="empty">
        <div class="empty-title">Ask anything about your documents.</div>
        <div class="empty-sub">
          Upload files on the left, then type a question below.
          <span v-if="selectedDocIds.length">
            Filter active: {{ selectedDocIds.length }} document(s) selected.
          </span>
        </div>
      </div>
      <Message
        v-for="(m, i) in messages"
        :key="i"
        :role="m.role"
        :text="m.text"
        :sources="m.sources || []"
        :streaming="m.streaming"
        @preview="(s) => emit('preview', s)"
      />
    </div>

    <div class="composer">
      <textarea
        v-model="input"
        rows="2"
        placeholder="Ask a question… (Enter to send, Shift+Enter for newline)"
        :disabled="busy"
        data-testid="question-input"
        @keydown="onKeydown"
      ></textarea>
      <div class="actions">
        <button
          v-if="busy"
          @click="stop"
          class="stop"
          title="Stop generating"
        >Stop</button>
        <button
          v-else
          class="primary"
          @click="onSubmit"
          :disabled="!input.trim()"
          data-testid="ask-button"
        >Ask</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat {
  display: grid;
  grid-template-rows: 1fr auto;
  height: 100%;
  min-height: 0;
}
.scroll {
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.empty {
  margin: auto;
  text-align: center;
  max-width: 420px;
  padding: 24px;
}
.empty-title { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.empty-sub { color: var(--text-mute); font-size: 13px; }

.composer {
  padding: 12px 16px 16px;
  border-top: 1px solid var(--border);
  background: var(--bg-2);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: end;
}
.composer textarea { min-height: 44px; max-height: 180px; }

.actions { display: flex; }
.stop {
  border-color: var(--danger);
  color: var(--danger);
}
</style>
