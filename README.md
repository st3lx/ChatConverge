# ChatConverge — Electron + React + TypeScript + FastAPI scaffold

A local-first, privacy-centric system that enables cross-platform message search, analysis, and safety auditing. 
Unifies message history across platforms, enables intelligent search and analysis, and integrates optional forensic-grade security scanning all under user control.

This privacy-first desktop app that lets you **import**, **search**, and **analyze** your chat history across multiple messaging apps (starting with WhatsApp).  
It works entirely **on your device** — no message data ever leaves your system unless you explicitly enable optional cloud sync.

## Quick start (development)

1. Python backend (use a virtualenv)
```powershell
cd python-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# start backend:
python -m uvicorn src.server:app --reload --port 8000


### Core Features
-  Import from exported chat files (.txt, .json)
-  Full-text search using SQLite FTS5
-  Smart conversation analytics (frequency, sentiment, etc.)
-  Multi-platform parsing (WhatsApp → Telegram → Messenger)
-  File safety scan via VirusTotal (hash only, with consent)
-  End-to-end encryption for local data storage

### Architecture
Built with:
- Python (backend + SQLite FTS5)
- Electron (UI)
- SQLCipher (encryption)
- Optional integration: VirusTotal API for file scans

