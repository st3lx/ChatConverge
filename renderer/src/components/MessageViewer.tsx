import React from "react";
import type { NormalizedMessage } from "../types/chat";

export default function MessageViewer({ message }:{ message:NormalizedMessage | null }){
  if (!message) return <div className="viewer">No message selected</div>;
  return (
    <div className="viewer">
      <div style={{display:"flex",justifyContent:"space-between",marginBottom:12}}>
        <div style={{fontWeight:700,color:"#ff3ecb"}}>{message.sender}</div>
        <div style={{color:"#8a8aa0"}}>{message.timestamp}</div>
      </div>
      <div style={{whiteSpace:"pre-wrap"}}>{message.text}</div>
    </div>
  );
}
