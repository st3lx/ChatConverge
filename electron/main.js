// electron/main.js
import { app, BrowserWindow } from "electron";
import path from "path";
import { spawn } from "child_process";
import "./ipc/importer.js";

function startBackend() {
  // You should run npm start from a terminal where the venv is already activated.
  // Alternatively set the python path here to your venv Python executable.
  const backend = spawn("python", ["-m", "uvicorn", "src.server:app", "--port", "8000"], {
    cwd: path.join(process.cwd()),
    shell: true
  });

  backend.stdout.on("data", (d) => console.log("[backend]", d.toString()));
  backend.stderr.on("data", (d) => console.error("[backend err]", d.toString()));
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 900,
    show: false,
    backgroundColor: "#07060a",
    webPreferences: {
      preload: path.join(process.cwd(), "electron", "preload.js"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  win.loadFile(path.join(process.cwd(), "electron", "renderer", "index.html"));
  win.once("ready-to-show", () => win.show());
}

app.whenReady().then(() => {
  startBackend();
  createWindow();
});


