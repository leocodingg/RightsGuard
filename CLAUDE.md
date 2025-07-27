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
- [ ] LangGraph orchestration with state management
- [ ] Community Legal Memory system design

### ✅ Recently Completed
- [x] AnalyzerAgent skeleton with AI simulation
- [x] Legal prompt building for NVIDIA LLM
- [x] Clean NVIDIA LLM integration (removed simulation code)
- [x] Direct API call structure with self.llm.invoke()
- [x] LetterAgent with NVIDIA LLM integration
- [x] Formal complaint letter generation system

### 🚀 NEW BREAKTHROUGH FEATURE: Community Legal Memory
**The Game Changer:** Instead of just helping individual tenants, our system becomes a community platform that learns from every complaint.

**How it works:**
- User A complains about "123 Main St - illegal entry" → stored in building database
- User B later complains about "123 Main St - no heat" → system shows building history
- Result: "Warning: This building has 2 previous complaints. Risk score: HIGH"

**Why this beats ChatGPT:**
- Persistent memory across all users
- Community organizing potential  
- Building/landlord reputation tracking
- Collective legal intelligence

### ⚠️ Current Issues in AnalyzerAgent
- **Response parsing**: Currently returns raw text, needs structured parsing
- **Error handling**: No fallback if NVIDIA API fails
- **NeMo Guardrails**: Not yet integrated for safety

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

## Learning Approach
- Building step-by-step with understanding
- User writes code with guidance, not copy-paste
- Focus on understanding each component before moving forward

## Key Concepts Learned
- **APIs vs Web Scraping**: APIs give structured data, scraping parses HTML
- **Response objects**: `.text` for content, `.status_code` for success/failure
- **Virtual environments**: Isolate project dependencies
- **Agent architecture**: Each agent has specific responsibility

## AnalyzerAgent Design Questions
1. What information does this agent need to make decisions?
   - User's complaint
   - Lease text
   - Scraped laws
   - Building violation history
   
2. How should it compare complaint to laws?
   - Keyword matching (simple)
   - Semantic similarity (advanced)
   - NVIDIA NIM for understanding
   
3. What format for results?
   - Structured dict with violations found
   - Confidence scores
   - Recommended actions

## Timeline
- Tonight: Setup + basic scraper
- Tomorrow: 4-hour build sprint during hackathon