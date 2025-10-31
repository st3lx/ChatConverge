# ChatConverge
A local-first, privacy-centric system that enables cross-platform message search, analysis, and safety auditing. 
Unifies message history across platforms, enables intelligent search and analysis, and integrates optional forensic-grade security scanning all under user control.

### Overview
ChatConverge is a privacy-first desktop app that lets you **import**, **search**, and **analyze** your chat history across multiple messaging apps (starting with WhatsApp).  
It works entirely **on your device** — no message data ever leaves your system unless you explicitly enable optional cloud sync.

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
- Electron or Flutter (UI)
- SQLCipher (encryption)
- Optional integration: VirusTotal API for file scans

