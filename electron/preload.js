// electron/preload.js
import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronAPI", {
  importChat: () => ipcRenderer.invoke("import-chat")
});
