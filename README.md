# LeaseAssist

AI-powered lease agreement analyzer that detects red flags, green flags, and generates negotiation emails using CrewAI multi-agent system.

## Prerequisites

- Node.js (v18+)
- Python 3.12
- OpenAI API key

## Setup

### 1. Environment Variables

Create `backend/.env`:

```
OPENAI_API_KEY=your-openai-key
OPENAI_DEFAULT_MODEL=gpt-3.5-turbo
GMAIL_SENDER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
GMAIL_RECIPIENT=recipient@gmail.com
```

### 2. Backend (AI Service)

```bash
cd backend/ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install "setuptools<81"
python -m uvicorn main:app --port 8000
```

Backend runs at http://localhost:8000

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## Usage

1. Start the backend (port 8000)
2. Start the frontend (port 5173)
3. Go to http://localhost:5173
4. Click **Analysis** in the navbar
5. Paste lease text or upload a PDF/DOCX/TXT file
6. Enter city name and landlord email
7. Click **Analyze Lease**
8. View red flags, green flags, and draft email

## Project Structure

```
leaseAssist/
  backend/
    ai-service/          # CrewAI multi-agent backend
      agents/            # 5 agents (extractor, clause, red flag, comparison, negotiation)
      tasks/             # 5 sequential tasks with context chaining
      tools/             # Email tool
      guardrails/        # Input/output validation
      crew.py            # Crew orchestration
      main.py            # FastAPI endpoints
    api-service/         # REST API (listings, search)
    .env                 # Environment variables
  frontend/
    src/
      AnalysisUploadView/  # Upload/paste lease text
      AnalysisResultView/  # Red/green flags + email draft
      App.tsx              # Main app with routing
```

## API Endpoints

| Method | Endpoint          | Description                    |
|--------|-------------------|--------------------------------|
| POST   | /analyze-lease    | Analyze lease with AI agents   |
| POST   | /analyze-contract | Contract analysis               |
| POST   | /eligibility      | Eligibility calculator          |
| POST   | /property-match   | Property matcher                |
| POST   | /chat             | Chatbot                         |
