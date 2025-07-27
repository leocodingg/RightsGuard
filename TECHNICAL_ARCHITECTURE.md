# RightsGuard Technical Architecture

## Overview
RightsGuard is a multi-agent AI system that helps tenants identify lease violations and generate legal complaint letters using NVIDIA GPU-accelerated inference and LangGraph orchestration.

## Architecture Diagram
```
User Input (Streamlit UI)
    ↓
LangGraph Workflow Orchestration
    ↓
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Research   │ → │    Legal     │ → │    Document     │
│   Agent     │    │   Analyst    │    │     Writer      │
└─────────────┘    └──────────────┘    └─────────────────┘
       ↓                  ↓                      ↓
  NYC Open Data     NVIDIA AI API         NVIDIA AI API
  Violations DB     (Llama 3.1 70B)      (Llama 3.1 70B)
```

## Core Technologies

### 1. Multi-Agent System
**Framework:** LangGraph
- **Purpose:** Orchestrates autonomous agents with state management
- **Implementation:** `workflow.py` defines `StateGraph` with three nodes
- **State Management:** `WorkflowState` TypedDict passes data between agents

### 2. AI/LLM Integration
**Framework:** LangChain + NVIDIA AI Endpoints
- **Model:** Meta Llama 3.1 70B Instruct
- **Acceleration:** GPU-accelerated inference via NVIDIA cloud
- **Integration:** `langchain_nvidia_ai_endpoints.ChatNVIDIA`

### 3. User Interface
**Framework:** Streamlit
- **Hosting:** Streamlit Cloud (free tier)
- **Features:** Real-time agent progress, download functionality
- **Responsive:** Mobile-friendly design

### 4. Data Sources
**NYC Open Data API**
- **Endpoint:** `https://data.cityofnewyork.us/resource/wvxf-dwi5.json`
- **Data:** Building violation records from HPD
- **Integration:** Direct API calls via `requests`

**Community Legal Memory**
- **Storage:** JSON file (`community_memory.json`)
- **Features:** Complaint categorization, duplicate detection
- **Purpose:** Track building complaint patterns

## Agent Details

### Research Agent (`scraper_agent.py`)
- **Role:** Gathers building violation data
- **Capabilities:**
  - NYC Open Data API queries
  - Community memory retrieval
  - Data aggregation
- **Output:** Violation records and building history

### Legal Analyst (`analyzer_agent.py`)
- **Role:** Analyzes complaints against NYC tenant law
- **Capabilities:**
  - Legal violation identification
  - Case strength assessment
  - Evidence recommendation
- **Technology:** NVIDIA AI with structured JSON output
- **Safety:** Attempted NeMo Guardrails (fallback to prompt engineering)

### Document Writer (`letter_agent.py`)
- **Role:** Generates formal complaint letters
- **Capabilities:**
  - Professional letter formatting
  - Legal citation inclusion
  - Tenant information integration
- **Technology:** NVIDIA AI with explicit prompt instructions

## Key Design Decisions

### 1. API-Based GPU Acceleration
**Choice:** Use NVIDIA AI Endpoints instead of local GPU
**Rationale:**
- No GPU management overhead
- Automatic scaling
- Lower cost (pay per use vs. GPU rental)
- Easier deployment

### 2. Multi-Agent vs. Single Agent
**Choice:** Three specialized agents
**Rationale:**
- Separation of concerns
- Easier testing and debugging
- Modular architecture
- Clear responsibility boundaries

### 3. Community Memory Design
**Choice:** Local JSON storage with categorization
**Rationale:**
- Simple implementation for MVP
- Building-centric tracking
- Complaint pattern recognition
- Easy to upgrade to database later

### 4. Streamlit Cloud Deployment
**Choice:** Streamlit Cloud over Brev.dev
**Rationale:**
- Free for public repos
- Built for Streamlit apps
- No GPU needed (using API)
- Simpler deployment process

## Security Considerations

### API Key Management
- Local: `.env` file (gitignored)
- Production: Streamlit secrets
- Never exposed in code

### Legal Compliance
- Clear disclaimers: "Information only, not legal advice"
- No personal data stored permanently
- Defensive purpose only (tenant protection)

### Input Validation
- Complaint categorization prevents spam
- Duplicate detection within 24 hours
- Character limits on stored complaints

## Performance Optimization

### Caching Strategy
- Community memory loaded once per session
- NYC API results not cached (real-time data)
- LLM responses not cached (unique per complaint)

### Concurrent Processing
- Agents run sequentially (by design)
- Could parallelize Research + Analysis in future
- Current flow ensures data dependencies

## Scalability Considerations

### Current Limitations
- JSON file storage (single server)
- Sequential agent processing
- API rate limits

### Future Enhancements
- PostgreSQL for community memory
- Redis for session caching
- Parallel agent execution where possible
- Multi-region deployment

## Monitoring & Debugging

### Logging
- Agent progress printed to console
- Streamlit UI shows real-time status
- Error messages displayed to user

### Error Handling
- Graceful API failures
- Fallback to mock mode
- JSON parsing error recovery

## Technology Stack Summary

**Frontend:**
- Streamlit 1.28.0

**AI/ML:**
- LangChain
- LangGraph  
- langchain-nvidia-ai-endpoints

**Data Processing:**
- Pandas
- BeautifulSoup4
- Requests

**Infrastructure:**
- Streamlit Cloud (hosting)
- NVIDIA AI Cloud (GPU inference)
- GitHub (version control)

## Why This Architecture?

1. **Modern Cloud-Native:** Leverages cloud services over local compute
2. **Cost-Effective:** Pay-per-use GPU instead of dedicated hardware
3. **Scalable:** Can handle multiple users without infrastructure changes
4. **Maintainable:** Clear separation of concerns with specialized agents
5. **Accessible:** Free public deployment for community benefit

This architecture demonstrates best practices for building production-ready AI applications that balance sophistication with practical deployment constraints.