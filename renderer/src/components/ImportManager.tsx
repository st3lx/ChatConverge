import React from "react";
import type { NormalizedMessage } from "../types/chat";

declare global {
  interface Window {
    electronAPI?: {
      importChat: () => Promise<any>;
    };
  }
}

export default function ImportManager({ onImported }:{ onImported:(m:NormalizedMessage[])=>void }) {
  async function onClick() {
    const res = await window.electronAPI?.importChat();
    if (!res) { alert("No response"); return; }
    if (res.error) { alert("Import error: " + res.error); return; }

    // Expect backend returns { platform, messages: [] } or array of messages
    const msgs = Array.isArray(res) ? res : (res.messages ?? []);
    onImported(msgs);
  }

  return (
    <div style={{display:"flex",gap:12,alignItems:"center"}}>
      <button className="btn" onClick={onClick}>Import Chat</button>
      <div style={{color:"#8a8aa0"}}>Click to import a WhatsApp/Telegram/Messenger export.</div>
    </div>
  );
}
