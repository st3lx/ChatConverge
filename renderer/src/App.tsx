import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatList from "./components/ChatList";
import MessageViewer from "./components/MessageViewer";
import ImportManager from "./components/ImportManager";
import type { NormalizedMessage } from "./types/chat";

export default function App() {
  const [messages, setMessages] = useState<NormalizedMessage[]>([]);
  const [selected, setSelected] = useState<NormalizedMessage | null>(null);

  return (
    <div className="app">
      <Sidebar />
      <div className="main">
        <ImportManager onImported={(msgs) => { setMessages(msgs); setSelected(msgs[0] ?? null); }} />
        <div className="panes">
          <ChatList messages={messages} onSelect={(m) => setSelected(m)} />
          <MessageViewer message={selected} />
        </div>
      </div>
    </div>
  );
}
