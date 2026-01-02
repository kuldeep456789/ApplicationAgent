# 💼 Job Application Assistant Agent

An autonomous AI agent that streamlines your job search by intelligently scraping job postings, analyzing requirements, matching your skills, and automating applications.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

- **🔍 Intelligent Job Scraping**: Automatically scrape jobs from LinkedIn, Indeed, and other platforms
- **🤖 AI-Powered Analysis**: Use Claude/GPT-4/Gemini to analyze job requirements and match with your skills
- **✍️ Cover Letter Generation**: Generate customized cover letters for each application
- **📝 Automated Form Filling**: Intelligently fill job application forms using Playwright
- **📊 Application Tracking**: Track all your applications in one place
- **🎨 Modern UI**: Beautiful Streamlit interface with glassmorphism design
- **🗄️ Flexible Database**: Support for SQLite (local) and Neon PostgreSQL (production)
- **🔄 Multiple LLM Providers**: Choose between Anthropic Claude, OpenAI GPT-4, or Google Gemini

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (CLI/Web)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Job Scraper │  │  LLM Engine  │  │  Form Filler │      │
│  │   Module     │  │   Module     │  │   Module     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Data Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   SQLite DB  │  │  Job Cache   │  │  User Profile│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              External Services                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Playwright │  │  Claude API  │  │  Job Sites   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js (for Playwright)
- API Keys (Gemini, Claude, or OpenAI)

### Setup & Execution

We provide organized scripts to handle setup and execution for you.

#### Windows
1. **Setup**: `scripts\windows\setup.bat` (Run once to install everything)
2. **Start Backend**: `scripts\windows\start_backend.bat`
3. **Start Frontend**: `scripts\windows\start_frontend.bat`

#### Linux/Mac
1. **Setup**: `chmod +x scripts/shell/*.sh && ./scripts/shell/setup.sh`
2. **Start Backend**: `./scripts/shell/start_backend.sh`
3. **Start Frontend**: `./scripts/shell/start_frontend.sh`

Access the application at `http://localhost:8501` once frontend is started.

## 📚 Tech Stack

### Backend & Core
- **Python 3.11+**: Main programming language
- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **asyncio**: Asynchronous programming

### Browser Automation
- **Playwright**: Modern browser automation
- **BeautifulSoup4**: HTML parsing
- **lxml**: Fast XML/HTML processing

### AI/LLM Integration
- **Anthropic Claude API**: Intelligent reasoning (optional)
- **OpenAI GPT-4**: Alternative LLM provider (optional)
- **Google Gemini**: Free-tier AI provider (recommended)
- **tiktoken**: Token counting

### Database & Storage
- **SQLite**: Lightweight database for local development
- **Neon PostgreSQL**: Serverless PostgreSQL for production
- **SQLAlchemy**: ORM for database operations
- **asyncpg**: Async PostgreSQL driver

### Testing & Quality
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-playwright**: Browser automation testing

### Monitoring & Logging
- **loguru**: Enhanced logging
- **prometheus_client**: Metrics collection

### Frontend
- **Streamlit**: Modern web UI

## 📖 API Documentation

### Endpoints

#### Job Search
```http
POST /api/jobs/search
Content-Type: application/json

{
  "keywords": "Software Engineer",
  "location": "San Francisco, CA",
  "platforms": ["linkedin", "indeed"],
  "max_results_per_platform": 50
}
```

#### Analyze Job
```http
POST /api/jobs/analyze
Content-Type: application/json

{
  "job_id": "12345"
}
```

#### Generate Cover Letter
```http
POST /api/cover-letter/generate
Content-Type: application/json

{
  "job_id": "12345",
  "tone": "professional"
}
```

#### Submit Application
```http
POST /api/applications/submit
Content-Type: application/json

{
  "job_id": "12345",
  "auto_submit": false
}
```

## 🎨 Frontend Features

- **Modern Glassmorphism Design**: Beautiful UI with blur effects
- **Gradient Animations**: Smooth transitions and hover effects
- **Responsive Layout**: Works on all screen sizes
- **Real-time Updates**: Live job search and application tracking
- **Interactive Charts**: Visualize your job search progress

## 🔧 Configuration

Edit `.env` file:

```env
# API Keys (choose one or more)
GEMINI_API_KEY=your_key_here        # Recommended: Free tier
ANTHROPIC_API_KEY=your_key_here     # Optional
OPENAI_API_KEY=your_key_here        # Optional

# Database (choose one)
# SQLite for local development
DATABASE_URL=sqlite+aiosqlite:///./data/job_assistant.db

# Neon PostgreSQL for production
# DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require

# LLM Provider Selection
LLM_PROVIDER=gemini  # Options: gemini, anthropic, openai

# Browser Settings
HEADLESS_BROWSER=True
BROWSER_TIMEOUT=30000

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=10
SCRAPER_DELAY_SECONDS=2
```

**Configure your API keys in the .env file to enable AI features.**

## 🧪 Testing

Run tests:
```bash
pytest backend/tests/ -v
```

Run with coverage:
```bash
pytest backend/tests/ --cov=backend --cov-report=html
```

## 📝 Usage Examples

### 1. Search for Jobs
```python
import requests

response = requests.post("http://localhost:8000/api/jobs/search", json={
    "keywords": "Python Developer",
    "location": "Remote",
    "platforms": ["linkedin", "indeed"]
})

jobs = response.json()['jobs']
```

### 2. Analyze Job Match
```python
response = requests.post("http://localhost:8000/api/jobs/analyze", json={
    "job_id": "12345"
})

analysis = response.json()['analysis']
print(f"Match Score: {analysis['match_score']}%")
```

### 3. Generate Cover Letter
```python
response = requests.post("http://localhost:8000/api/cover-letter/generate", json={
    "job_id": "12345",
    "tone": "professional"
})

cover_letter = response.json()['cover_letter']
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for educational purposes. Always review applications before submission. Respect job sites' terms of service and rate limits.

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Anthropic for Claude API
- Playwright for browser automation
- Streamlit for the beautiful UI framework

## 📧 Contact

For questions or support, please open an issue on GitHub.



