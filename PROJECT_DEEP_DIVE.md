# 🏛️ RightsGuard: Complete Project Deep Dive

## Table of Contents
1. [Project Overview](#project-overview)
2. [Problem & Solution](#problem--solution)
3. [Technical Architecture](#technical-architecture)
4. [Agent System Breakdown](#agent-system-breakdown)
5. [Key Features](#key-features)
6. [Code Walkthrough](#code-walkthrough)
7. [Data Flow](#data-flow)
8. [Technologies Used](#technologies-used)
9. [Setup & Deployment](#setup--deployment)
10. [Demo Script](#demo-script)

---

## Project Overview

**RightsGuard** is a multi-agent AI system that empowers NYC tenants to understand their rights and generate formal complaint letters when landlords violate housing laws. Built for the NVIDIA AI Agent Hackathon, it showcases GPU-accelerated legal text processing with community-driven intelligence.

### Key Stats
- **3 AI Agents** working in orchestration
- **NVIDIA LLM Integration** for legal analysis
- **Community Legal Memory** for collective intelligence
- **Real-time UI** showing agent collaboration
- **Production-ready** with Brev.dev GPU deployment

---

## Problem & Solution

### 🔴 The Problem
1. **Tenants don't know their rights** - NYC housing law is complex
2. **Power imbalance** - Landlords have lawyers, tenants don't
3. **Isolated complaints** - Each tenant fights alone
4. **Language barriers** - Legal jargon is intimidating

### 🟢 Our Solution
1. **AI Legal Assistant** - Analyzes complaints against actual NYC laws
2. **Automated Letter Generation** - Professional complaint letters
3. **Community Memory** - Learn from all tenant complaints
4. **Plain English** - Translates legalese to understandable advice

---

## Technical Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│  LangGraph      │────▶│  Community      │
│   (app.py)      │     │  Orchestration  │     │  Memory (JSON)  │
└─────────────────┘     │  (workflow.py)  │     └─────────────────┘
                        └────────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
        │ WebScraper   │ │  Analyzer   │ │   Letter    │
        │    Agent     │ │   Agent     │ │   Agent     │
        └──────────────┘ └─────────────┘ └─────────────┘
                │                │                │
                │                │                │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
        │ NYC Open     │ │ NVIDIA LLM  │ │ NVIDIA LLM  │
        │ Data API     │ │ (Llama 3.1) │ │ (Llama 3.1) │
        └──────────────┘ └─────────────┘ └─────────────┘
```

### Component Relationships
1. **User Input** → Streamlit UI → LangGraph Workflow
2. **Workflow** → Orchestrates 3 agents in sequence
3. **Each Agent** → Specialized task with state sharing
4. **Community Memory** → Persists across sessions

---

## Agent System Breakdown

### 🕷️ WebScraperAgent (`agents/scraper_agent.py`)
**Purpose**: Gathers legal information and building violation history

**Key Functions**:
- `scrape_legal_info()` - Gets NYC tenant laws from websites
- `search_nyc_open_data()` - Queries NYC violation database
- `get_building_violations()` - Returns violation history

**Data Sources**:
- NYC Open Data API (real violations)
- Legal websites (simulated for demo)
- Community Memory (previous complaints)

### 🧠 AnalyzerAgent (`agents/analyzer_agent.py`)
**Purpose**: Uses NVIDIA LLM to analyze complaints against laws

**Key Features**:
- **NVIDIA Llama 3.1 70B** integration
- **Structured JSON output** parsing
- **NeMo Guardrails** for safety
- **Mock mode** for demos without API

**Analysis Output**:
```json
{
  "is_legitimate": "Yes",
  "applicable_laws": ["NYC Admin Code §27-2009"],
  "case_strength": "Strong",
  "evidence_needed": ["Photos", "Written notices"],
  "recommended_actions": ["Send certified letter", "Call 311"]
}
```

### 📝 LetterAgent (`agents/letter_agent.py`)
**Purpose**: Generates formal complaint letters

**Features**:
- Professional legal formatting
- Cites specific statutes
- Includes evidence requirements
- CC's relevant agencies

---

## Key Features

### 🏘️ Community Legal Memory
**What makes us special** - Not just individual help, but collective intelligence!

**How it works**:
1. Every complaint is stored by building address
2. Future tenants see: "This building has 5 previous complaints!"
3. Risk scoring: HIGH (2+ complaints), MODERATE (1 complaint)
4. Landlord tracking across multiple properties

**Storage Structure** (`community_memory.json`):
```json
{
  "buildings": {
    "123 main st, new york, ny 10001": [
      {
        "date": "2024-01-15T10:30:00",
        "complaint": "No heat for 3 days",
        "landlord": "ABC Management"
      }
    ]
  },
  "landlords": {
    "abc management": ["123 main st", "456 oak ave"]
  },
  "statistics": {
    "total_complaints": 127
  }
}
```

### 🛡️ NeMo Guardrails Integration
**Safety first** - Prevents giving actual legal advice

**Guardrails Config** (`config/guardrails_config.yaml`):
- Blocks off-topic questions
- Adds legal disclaimers
- Ensures informational tone
- Prevents financial/medical advice

### 🎨 Real-time Agent Visualization
**Streamlit UI** shows agents working in real-time:
- Progress indicators for each agent
- Status messages during processing
- Final results in two columns
- Download button for letters

---

## Code Walkthrough

### 1. Entry Point (`app.py`)
```python
# Streamlit UI initialization
st.set_page_config(page_title="RightsGuard", icon="⚖️")

# Sidebar for user input
complaint = st.sidebar.text_area("Describe your issue")
address = st.sidebar.text_input("Building address")

# Process button triggers workflow
if st.button("Analyze My Rights"):
    workflow = RightsGuardWorkflow()
    result = workflow.process_complaint(...)
```

### 2. Orchestration (`workflow.py`)
```python
class RightsGuardWorkflow:
    def build_workflow(self):
        workflow = StateGraph(WorkflowState)
        
        # Define agent flow
        workflow.add_node("web_scraper", self.web_scraper_node)
        workflow.add_node("analyzer", self.analyzer_node)
        workflow.add_node("letter_generator", self.letter_generator_node)
        
        # Connect in sequence
        workflow.add_edge("web_scraper", "analyzer")
        workflow.add_edge("analyzer", "letter_generator")
```

### 3. State Management
```python
class WorkflowState(TypedDict):
    user_complaint: str
    building_address: str
    tenant_info: Dict
    scraped_laws: List[str]
    violation_data: List[Dict]
    building_history: List[Dict]
    analysis_result: Dict
    final_letter: Dict
    status: str
```

---

## Data Flow

1. **User Input** 
   - Complaint: "Landlord enters without notice"
   - Address: "123 Main St"
   - Tenant info: Name, date

2. **WebScraperAgent**
   - Fetches: NYC Admin Code §27-2009 (48hr notice law)
   - Finds: 3 previous violations at address
   - Retrieves: 2 past complaints from Community Memory

3. **AnalyzerAgent**
   - Processes with NVIDIA LLM
   - Returns: Legitimate=Yes, Strong case, Need photos
   - Adds: Community insight about building risk

4. **LetterAgent**
   - Generates formal complaint letter
   - Cites: Specific statutes
   - Includes: Next steps and deadlines

5. **Community Memory**
   - Stores this complaint
   - Updates building risk score
   - Available for future tenants

---

## Technologies Used

### Core Framework
- **Streamlit** - Web UI framework
- **LangChain** - LLM application framework
- **LangGraph** - Multi-agent orchestration

### NVIDIA Stack
- **NVIDIA NIM** - LLM API endpoints
- **Llama 3.1 70B** - Large language model
- **NeMo Guardrails** - AI safety framework
- **Brev.dev** - GPU deployment platform

### Data & Storage
- **NYC Open Data API** - Real violation data
- **JSON** - Community memory storage
- **Python-dotenv** - Environment management

### Development Tools
- **Git** - Version control
- **Virtual environments** - Dependency isolation
- **VSCode** - IDE with Python support

---

## Setup & Deployment

### Local Development
```bash
# Clone repository
git clone [repo-url]
cd RightsGuard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export NVIDIA_API_KEY="your-key-here"

# Run application
streamlit run app.py
```

### Brev.dev GPU Deployment
```bash
# Install Brev CLI
pip install brev

# Login
brev login

# Deploy
brev create rightsguard-demo

# Access at: https://rightsguard-demo-[id].brev.dev
```

---

## Demo Script

### 1. Problem Introduction (30 seconds)
"NYC tenants face illegal landlord behavior daily but don't know their rights. ChatGPT gives generic advice. We built RightsGuard - a specialized multi-agent system for NYC tenant protection."

### 2. Live Demo (3 minutes)
1. **Show complaint form**: "My landlord entered my apartment without notice three times this month"
2. **Click Analyze**: Watch agents work in real-time
3. **WebScraper runs**: "Finding relevant NYC laws and building history..."
4. **Analyzer processes**: "Using NVIDIA Llama 3.1 to analyze your case..."
5. **Show results**: "Strong case! Violation of NYC Admin Code §27-2009"
6. **Community insight**: "⚠️ This building has 4 previous complaints!"
7. **Download letter**: Professional complaint ready to send

### 3. Technical Deep Dive (1 minute)
- "Three specialized agents using LangGraph orchestration"
- "NVIDIA GPU acceleration for instant analysis"
- "Community Legal Memory - turning individual complaints into collective power"
- "NeMo Guardrails ensuring safe, informational responses"

### 4. Impact & Vision (30 seconds)
"Imagine every tenant having an AI legal assistant. Bad landlords can't exploit ignorance anymore. Community memory means patterns of abuse are tracked and exposed."

---

## Current Limitations & Acknowledgments

### Technical Limitations
1. **JSON Storage** - Not scalable for thousands of users
   - Single file can become bottleneck
   - No concurrent write protection
   - Limited query capabilities

2. **API Dependency** - Requires NVIDIA API key
   - Costs scale with usage
   - Network latency for each request
   - No offline capability

3. **Single City Focus** - NYC laws only
   - Would need retraining for other cities
   - Legal variations by state not handled

4. **Language Support** - English only currently
   - Many NYC tenants speak other languages
   - Legal terms particularly challenging to translate

### Legal & Ethical Considerations
1. **Not Legal Advice** - Information only
   - Cannot replace actual lawyer
   - Disclaimer required but users might ignore
   - Risk of misinterpretation

2. **Data Privacy** - Complaints stored in system
   - Sensitive tenant information
   - No encryption currently
   - GDPR/privacy compliance needed

3. **Accuracy Concerns** - LLM hallucination risk
   - Laws change frequently
   - Need regular updates
   - No real-time law verification

### UX Limitations
1. **Desktop Focused** - Streamlit not mobile-optimized
   - Many tenants only have phones
   - UI could be more accessible

2. **Technical Barriers** - Requires some tech literacy
   - Form filling might intimidate some users
   - No voice interface yet

### Scalability Issues
1. **Single Instance** - No load balancing
   - Would crash with many concurrent users
   - No caching layer
   - Memory limits on free hosting

2. **Manual Updates** - Laws must be updated manually
   - No automated scraping of law changes
   - Community memory needs moderation

---

## Future Enhancements

### Technical Upgrades
1. **PostgreSQL** for scalable memory storage
2. **Redis** caching for performance
3. **Multi-language** support (Spanish, Chinese)
4. **Mobile app** for easier access

### Feature Additions
1. **Document scanner** for lease analysis
2. **Voice interface** for accessibility  
3. **Automated 311 complaint filing**
4. **Tenant union integration**

### Social Impact
1. **Open source** the core system
2. **Partner with legal aid** organizations
3. **Expand to other cities** (LA, Chicago)
4. **Track citywide violation patterns**

---

## Conclusion

RightsGuard demonstrates how AI agents can empower vulnerable communities. By combining NVIDIA's GPU-accelerated LLMs with multi-agent orchestration and community memory, we've created more than a chatbot - we've built a movement for tenant justice.

**The future is collective intelligence helping individual tenants.**

---

*Built with ❤️ for the NVIDIA AI Agent Hackathon*