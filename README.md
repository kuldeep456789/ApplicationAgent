
An autonomous AI agent that streamlines your job search by intelligently scraping job postings, analyzing requirements, matching your skills, and automating applications.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)


- **🔍 Intelligent Job Scraping**: Automatically scrape jobs from LinkedIn, Indeed, and other platforms
- **🤖 AI-Powered Analysis**: Use Claude/GPT-4/Gemini to analyze job requirements and match with your skills
- **✍️ Cover Letter Generation**: Generate customized cover letters for each application
- **📝 Automated Form Filling**: Intelligently fill job application forms using Playwright
- **📊 Application Tracking**: Track all your applications in one place
- **🎨 Modern UI**: Beautiful Streamlit interface with glassmorphism design
## 🚀 How to Run

### Windows
1. **Setup (First time only)**:
   ```cmd
   scripts\windows\setup.bat
   ```
2. **Start Backend**:
   ```cmd
   scripts\windows\start_backend.bat
   ```
3. **Start Frontend**:
   ```cmd
   scripts\windows\start_frontend.bat
   ```

### Linux/Mac
1. **Setup (First time only)**:
   ```bash
   chmod +x scripts/shell/*.sh
   ./scripts/shell/setup.sh
   ```
2. **Start Backend**:
   ```bash
   ./scripts/shell/start_backend.sh
   ```
3. **Start Frontend**:
   ```bash
   ./scripts/shell/start_frontend.sh
   ```

Access the UI at: `http://localhost:8501`

