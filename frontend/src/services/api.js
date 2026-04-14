const API_BASE = '/api';

export async function uploadFile(file) {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Upload failed (${res.status})`);
  }
  return res.json();
}

export async function listDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error(`Failed to list documents (${res.status})`);
  return (await res.json()).documents;
}

export async function getChunk(chunkId, window = 2) {
  const res = await fetch(`${API_BASE}/chunks/${encodeURIComponent(chunkId)}?window=${window}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Failed to load chunk (${res.status})`);
  }
  return res.json();
}

export async function deleteDocument(docId) {
  const res = await fetch(`${API_BASE}/documents/${docId}`, { method: 'DELETE' });
  if (!res.ok && res.status !== 404) throw new Error(`Delete failed (${res.status})`);
}

/**
 * Stream an answer via SSE. Calls `onEvent` with each parsed JSON event:
 *   { type: 'token',   data: string }
 *   { type: 'sources', data: SourceChunk[] }
 *   { type: 'done' }
 *   { type: 'error',   data: string }
 *
 * Returns a function you can call to abort the stream.
 */
export function askStream({ question, docIds, onEvent }) {
  const controller = new AbortController();

  (async () => {
    let res;
    try {
      res = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, doc_ids: docIds?.length ? docIds : null }),
        signal: controller.signal,
      });
    } catch (e) {
      if (e.name !== 'AbortError') onEvent({ type: 'error', data: e.message });
      return;
    }
    if (!res.ok || !res.body) {
      onEvent({ type: 'error', data: `Request failed (${res.status})` });
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        let idx;
        while ((idx = buffer.indexOf('\n\n')) !== -1) {
          const rawEvent = buffer.slice(0, idx);
          buffer = buffer.slice(idx + 2);
          const line = rawEvent.split('\n').find((l) => l.startsWith('data: '));
          if (!line) continue;
          const payload = line.slice(6).trim();
          if (!payload) continue;
          try {
            onEvent(JSON.parse(payload));
          } catch {
            // ignore malformed event
          }
        }
      }
    } catch (e) {
      if (e.name !== 'AbortError') onEvent({ type: 'error', data: e.message });
    }
  })();

  return () => controller.abort();
}
