// electron/renderer/renderer.js
const importBtn = document.getElementById("importBtn");
const convPanel = document.getElementById("conversations");
const listPanel = document.getElementById("messageList");
const viewPanel = document.getElementById("messageView");
const searchInput = document.getElementById("search");

let currentMessages = [];

importBtn.onclick = async () => {
  importBtn.disabled = true;
  importBtn.textContent = "Importing...";
  const res = await window.electronAPI.importChat();
  importBtn.disabled = false;
  importBtn.textContent = "Import Chat";

  if (!res || res.error) {
    alert("Import failed: " + (res ? res.error : "no response"));
    return;
  }

  const payload = Array.isArray(res) ? res : (res.messages || res);
  currentMessages = Array.isArray(payload) ? payload : [];
  renderMessageList(currentMessages);
};

function renderMessageList(messages) {
  listPanel.innerHTML = "";
  messages.slice(0, 500).forEach((m, i) => {
    const el = document.createElement("div");
    el.className = "msg-row";
    el.innerHTML = `<div class="sender">${escapeHtml(m.sender || m.from || 'Unknown')}</div>
                    <div class="snippet">${escapeHtml((m.text || m.message || '').slice(0, 160))}</div>`;
    el.onclick = () => showMessage(m);
    listPanel.appendChild(el);
  });
}

function showMessage(m) {
  viewPanel.innerHTML = `
    <div class="msg-header">
      <div class="sender">${escapeHtml(m.sender || m.from || "Unknown")}</div>
      <div class="time">${escapeHtml((m.timestamp || "").toString())}</div>
    </div>
    <div class="msg-body">${escapeHtml(m.text || m.message || "")}</div>
  `;
}

function escapeHtml(s) {
  if (!s) return "";
  return s.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

searchInput.oninput = () => {
  const q = searchInput.value.trim().toLowerCase();
  if (!q) { renderMessageList(currentMessages); return; }
  const filtered = currentMessages.filter(m => (m.text || m.message || "").toLowerCase().includes(q) || (m.sender||"").toLowerCase().includes(q));
  renderMessageList(filtered);
};
