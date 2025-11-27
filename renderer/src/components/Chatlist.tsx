import React from "react";
import type { NormalizedMessage } from "../types/chat";

export default function ChatList({ messages, onSelect }:{ messages:NormalizedMessage[], onSelect:(m:NormalizedMessage)=>void }){
  return (
    <div className="chat-list">
      {messages.map((m,i)=>(
        <div className="msg-row" key={i} onClick={()=>onSelect(m)}>
          <div className="from">{m.sender}</div>
          <div style={{color:"#8a8aa0", marginTop:6}}>{m.text?.slice(0,120)}</div>
        </div>
      ))}
      {messages.length===0 && <div style={{color:"#6b6b80"}}>No messages yet</div>}
    </div>
  );
}
