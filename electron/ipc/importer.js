// electron/ipc/importer.js
import { ipcMain, dialog } from "electron";
import axios from "axios";

ipcMain.handle("import-chat", async () => {
  const { canceled, filePaths } = await dialog.showOpenDialog({
    filters: [
      { name: "Chat Exports", extensions: ["txt", "json", "html"] }
    ],
    properties: ["openFile"]
  });

  if (canceled || filePaths.length === 0) return { error: "User canceled" };

  const filePath = filePaths[0];

  try {
    const resp = await axios.post("http://127.0.0.1:8000/import", { path: filePath }, { timeout: 30000 });
    return resp.data;
  } catch (err) {
    console.error("Import error:", err.toString());
    return { error: err.toString() };
  }
});



