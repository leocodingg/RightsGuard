# RightsGuard - NVIDIA AI Agent Hackathon Project

## Project Overview
Multi-agent system that helps tenants identify lease violations and generate legal complaint letters using NVIDIA NeMo and GPU acceleration.

## Key Commands
```bash
# Setup
pip install -r requirements.txt

# Run application  
streamlit run app.py

# Test agents individually
python -m agents.scraper_agent
python -m agents.analyzer_agent  
python -m agents.letter_agent
```

## Architecture
```
User Input → WebScraperAgent → AnalyzerAgent → LetterAgent → Output
```

## Progress Tracking

### ✅ Completed
- [x] GitHub repo setup
- [x] Project structure created
- [x] Requirements.txt with NVIDIA stack (NeMo, Guardrails, LangChain)
- [x] .gitignore configured
- [x] CLAUDE.md created
- [x] Python virtual environment setup
- [x] WebScraperAgent (web scraping + NYC Open Data API)
- [x] HTML parsing with BeautifulSoup
- [x] Legal text extraction from multiple sources

### 🔄 In Progress
- [ ] Testing combined API + web scraping data
- [ ] Building AnalyzerAgent

### 📋 Todo
- [ ] AnalyzerAgent with NeMo Guardrails
- [ ] LetterAgent with templates
- [ ] LangGraph multi-agent orchestration
- [ ] Streamlit UI
- [ ] NVIDIA NeMo integration
- [ ] Brev.dev GPU deployment
- [ ] Demo preparation

## Technical Notes
- Using Brev.dev GPU for acceleration
- NeMo Guardrails for legal safety
- LangChain for agent orchestration
- Focus: NYC tenant rights only for MVP

## Demo Script
1. User pastes lease text
2. Show agents collaborating in real-time
3. Output professional letter with legal citations
4. Emphasize GPU acceleration and safety guardrails

## API Keys Needed
- NVIDIA NIM API key (from hackathon)
- Brev.dev GPU access

## Timeline
- Tonight: Setup + basic scraper
- Tomorrow: 4-hour build sprint during hackathon