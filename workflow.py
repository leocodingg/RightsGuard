# LangGraph Workflow - Orchestrates our three agents
import json
import os
from typing import Dict, List, TypedDict
from datetime import datetime

from langgraph.graph import StateGraph, END
from agents.scraper_agent import WebScraperAgent
from agents.analyzer_agent import AnalyzerAgent 
from agents.letter_agent import LetterAgent

# Define the state that flows between agents
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

class RightsGuardWorkflow:
    def __init__(self):
        """Initialize the multi-agent workflow"""
        print("🚀 Initializing RightsGuard Multi-Agent Workflow...")
        
        # Initialize all our agents
        self.scraper = WebScraperAgent()
        self.analyzer = AnalyzerAgent()
        self.letter = LetterAgent()
        
        # Community Legal Memory database (simple JSON for now)
        self.memory_db_path = "community_memory.json"
        self.load_community_memory()
        
        # Build the LangGraph workflow
        self.graph = self.build_workflow()
        
        print("✅ Workflow initialized with Community Legal Memory!")
    
    def load_community_memory(self):
        """Load the community memory database"""
        if os.path.exists(self.memory_db_path):
            with open(self.memory_db_path, 'r') as f:
                self.community_memory = json.load(f)
        else:
            self.community_memory = {
                "buildings": {},  # address -> complaint history
                "landlords": {},  # landlord -> building list
                "statistics": {"total_complaints": 0}
            }
            self.save_community_memory()
    
    def save_community_memory(self):
        """Save the community memory to disk"""
        with open(self.memory_db_path, 'w') as f:
            json.dump(self.community_memory, f, indent=2)
    
    def get_building_history(self, address: str) -> List[Dict]:
        """Get complaint history for a building"""
        address_key = address.lower().strip()
        return self.community_memory["buildings"].get(address_key, [])
    
    def store_complaint(self, address: str, complaint: str, landlord: str = None):
        """Store a new complaint in community memory"""
        address_key = address.lower().strip()
        
        complaint_record = {
            "date": datetime.now().isoformat(),
            "complaint": complaint,
            "landlord": landlord
        }
        
        # Add to building history
        if address_key not in self.community_memory["buildings"]:
            self.community_memory["buildings"][address_key] = []
        
        self.community_memory["buildings"][address_key].append(complaint_record)
        
        # Update landlord tracking
        if landlord:
            landlord_key = landlord.lower().strip()
            if landlord_key not in self.community_memory["landlords"]:
                self.community_memory["landlords"][landlord_key] = []
            
            if address_key not in self.community_memory["landlords"][landlord_key]:
                self.community_memory["landlords"][landlord_key].append(address_key)
        
        # Update statistics
        self.community_memory["statistics"]["total_complaints"] += 1
        
        # Save to disk
        self.save_community_memory()
        
        print(f"💾 Stored complaint for {address} in Community Legal Memory")
    
    def web_scraper_node(self, state: WorkflowState) -> WorkflowState:
        """Node 1: Web scraping for legal information"""
        print("\n🕷️ WebScraper Agent: Gathering legal information...")
        
        # Let the LLM determine relevant laws based on the complaint
        # This is smarter than web scraping!
        scraped_laws = []  # We'll let the AnalyzerAgent handle law identification
        
        # Get NYC violation data
        violation_data = self.scraper.search_nyc_open_data(state["building_address"])
        
        # Get building history from Community Legal Memory
        building_history = self.get_building_history(state["building_address"])
        
        # Update state
        state["scraped_laws"] = scraped_laws
        state["violation_data"] = violation_data
        state["building_history"] = building_history
        state["status"] = "scraping_complete"
        
        print(f"✅ Found {len(scraped_laws)} laws, {len(violation_data)} violations, {len(building_history)} community complaints")
        
        return state
    
    def analyzer_node(self, state: WorkflowState) -> WorkflowState:
        """Node 2: AI analysis of the complaint"""
        print("\n🧠 Analyzer Agent: Analyzing complaint with NVIDIA AI...")
        
        # Use our AnalyzerAgent to analyze the complaint
        analysis_result = self.analyzer.analyze_complaint(
            user_complaint=state["user_complaint"],
            scraped_laws=state["scraped_laws"],
            violations_data=state["violation_data"]
        )
        
        # Add community insights
        building_history = state["building_history"]
        if building_history:
            community_insight = f"\n🏢 COMMUNITY INSIGHT: This building has {len(building_history)} previous complaints. Risk level: {'HIGH' if len(building_history) >= 2 else 'MODERATE'}"
            analysis_result["analysis"] += community_insight
        
        state["analysis_result"] = analysis_result
        state["status"] = "analysis_complete"
        
        print("✅ Analysis complete with community insights")
        
        return state
    
    def letter_generator_node(self, state: WorkflowState) -> WorkflowState:
        """Node 3: Generate legal complaint letter"""
        print("\n📝 Letter Agent: Generating complaint letter...")
        
        # Generate the letter using our LetterAgent
        final_letter = self.letter.generate_complaint_letter(
            analysis_data=state["analysis_result"],
            tenant_info=state["tenant_info"]
        )
        
        # Add community memory reference if relevant
        if state["building_history"]:
            community_addendum = f"\n\nNote: Community records show {len(state['building_history'])} similar complaints at this address."
            final_letter["letter_content"] += community_addendum
        
        state["final_letter"] = final_letter
        state["status"] = "letter_complete"
        
        # Store this complaint in community memory
        self.store_complaint(
            address=state["building_address"],
            complaint=state["user_complaint"],
            landlord=state["tenant_info"].get("landlord")
        )
        
        print("✅ Letter generated and complaint stored in Community Legal Memory")
        
        return state
    
    def build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)
        
        # Add our three agent nodes
        workflow.add_node("web_scraper", self.web_scraper_node)
        workflow.add_node("analyzer", self.analyzer_node)
        workflow.add_node("letter_generator", self.letter_generator_node)
        
        # Define the flow: WebScraper -> Analyzer -> LetterGenerator -> END
        workflow.set_entry_point("web_scraper")
        workflow.add_edge("web_scraper", "analyzer")
        workflow.add_edge("analyzer", "letter_generator")
        workflow.add_edge("letter_generator", END)
        
        return workflow.compile()
    
    def process_complaint(self, user_complaint: str, building_address: str, tenant_info: Dict) -> Dict:
        """Main entry point - process a tenant complaint end-to-end"""
        print(f"\n🏛️ Processing complaint for {building_address}...")
        
        # Initialize the workflow state
        initial_state = WorkflowState(
            user_complaint=user_complaint,
            building_address=building_address,
            tenant_info=tenant_info,
            scraped_laws=[],
            violation_data=[],
            building_history=[],
            analysis_result={},
            final_letter={},
            status="initialized"
        )
        
        # Run the workflow
        final_state = self.graph.invoke(initial_state)
        
        # Return the complete result
        return {
            "letter": final_state["final_letter"],
            "analysis": final_state["analysis_result"],
            "community_insights": {
                "building_history": final_state["building_history"],
                "violation_count": len(final_state["violation_data"]),
                "total_community_complaints": self.community_memory["statistics"]["total_complaints"]
            },
            "sources": {
                "laws": final_state["scraped_laws"],
                "violations": final_state["violation_data"]
            }
        }

# Test the workflow
if __name__ == "__main__":
    # Test data
    test_complaint = "My landlord keeps entering my apartment without giving me notice. This has happened 3 times this month."
    test_address = "123 Main St, New York, NY 10001"
    test_tenant_info = {
        "name": "John Doe",
        "address": test_address,
        "landlord": "ABC Property Management",
        "date": "January 15, 2024"
    }
    
    try:
        # Initialize workflow
        workflow = RightsGuardWorkflow()
        
        # Process complaint
        result = workflow.process_complaint(
            user_complaint=test_complaint,
            building_address=test_address,
            tenant_info=test_tenant_info
        )
        
        print("\n" + "="*50)
        print("🎉 WORKFLOW COMPLETE!")
        print("="*50)
        print(f"Generated letter: {len(result['letter']['letter_content'])} characters")
        print(f"Community complaints for this building: {len(result['community_insights']['building_history'])}")
        print(f"Total community complaints: {result['community_insights']['total_community_complaints']}")
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        print("Make sure NVIDIA_API_KEY is set in your environment")