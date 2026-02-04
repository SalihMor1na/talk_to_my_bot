# 🤖 Talk to my BOT

Talk to my BOT är ett AI-engineering-projekt där användaren kan ladda upp sitt CV och andra dokument och sedan interagera med en chatbot som **imiterar personens profil**.

Projektet är utvecklat som en del av ett AI-engineering-kursprojekt och följer ett agilt arbetssätt med backend, frontend, API och LLM-integration.

---

## 🎯 Syfte

Syftet med projektet är att:
- använda AI-engineering-koncept för att lösa ett verkligt problem
- bygga en fullstack-applikation med backend + frontend
- arbeta agilt i grupp med Git, issues och pull requests
- använda LLM:er på ett kontrollerat och förståeligt sätt

---

## 🧠 Funktionalitet

- 📄 Ladda upp CV, personliga brev eller liknande dokument
- 🧾 Extrahera och sammanfatta information från dokument
- 📊 Visa profil-sammanfattning, till exempel:
  - antal års erfarenhet
  - roller/yrken
  - kort personlig sammanfattning
- 💬 Chatta med en bot som **imiterar profilen**
- 🔊 (Valfritt) Prata med boten via röst

---

## 🏗️ Arkitektur

Projektet är uppdelat i följande delar:

```talk_to_my_bot/
│
├── backend/ # API, AI-logik och dokumenthantering
├── frontend/ # Webbgränssnitt för användaren
├── data/ # Dokument, embeddings eller testdata
├── api.py # API-entrypoint
├── pdfs_to_text.py # PDF → text-konvertering
├── explorations.ipynb# Experiment och tester
├── pyproject.toml # Python-projektkonfiguration
└── README.md```


---

## ⚙️ Tekniker

**Backend**
- Python
- FastAPI
- LLM (t.ex. OpenAI)
- Text-extraktion & eventuell RAG

**Frontend**
- JavaScript / React (eller liknande)
- API-kommunikation

**Övrigt**
- Git & GitHub
- Agilt arbetssätt (Kanban, issues)
- Docker (planerat)
- Deployment till Azure (planerat)

---

## 🚀 Installation & körning

### 1. Klona repot
```bash
git clone https://github.com/SalihMor1na/talk_to_my_bot.git
cd talk_to_my_bot
2. Skapa virtuell miljö (backend)
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Installera beroenden
pip install -r backend/requirements.txt
4. Starta backend
uvicorn api:app --reload
5. Starta frontend
cd frontend
npm install
npm start
🧪 Exempel på API-anrop
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Berätta om min erfarenhet"}'
👥 Teamarbete
3–4 personer per grupp

GitHub-repo med branches & pull requests

Issues + Kanban

Alla medlemmar bidrar med commits

📸 Screenshots
(Lägg in screenshots här när projektet är klart)

📦 Deployment
Projektet dockeriseras

Deployas till Azure (planerat)

📝 Licens
MIT License (valfritt att lägga till)

📚 Notering om LLM-användning
LLM:er har använts som stöd för:

idéer

mindre koddelar

All LLM-genererad kod är kommenterad och förstådd av teamet.
