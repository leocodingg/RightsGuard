# AnalyzerAgent - Compares tenant complaints to legal information
import os
from typing import Dict, List
from langchain_nvidia_ai_endpoints import ChatNVIDIA

try:
    from nemoguardrails import LLMRails, RailsConfig
    GUARDRAILS_AVAILABLE = True
except ImportError:
    GUARDRAILS_AVAILABLE = False
    print("⚠️ NeMo Guardrails not available (expected in cloud deployment), running without safety guardrails")

# Import mock responses for backup
try:
    from .mock_responses import MockNVIDIAResponses, MOCK_MODE
except ImportError:
    MOCK_MODE = False

class AnalyzerAgent:
    def __init__(self):
        # Give the agent a name
        self.name = "AnalyzerAgent"
        
        # Get API key from environment
        api_key = os.getenv("NVIDIA_API_KEY")
        
        # Check if we should use mock mode
        if not api_key:
            print("⚠️ No NVIDIA_API_KEY found - using MOCK MODE for demo")
            self.mock_mode = True
            self.llm = None
        else:
            self.mock_mode = False
        
        # Initialize NVIDIA LLM only if we have API key
        if not self.mock_mode:
            self.llm = ChatNVIDIA(
                model="meta/llama-3.1-70b-instruct",
                api_key=api_key,
                temperature=0.1  # Low temperature for consistent legal analysis
            )
        
        # Initialize NeMo Guardrails for safety
        self.guardrails = None
        if GUARDRAILS_AVAILABLE:
            try:
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
                rails_config = RailsConfig.from_path(config_path)
                self.guardrails = LLMRails(rails_config, llm=self.llm)
                print(f"{self.name} initialized with NVIDIA LLM + NeMo Guardrails!")
            except Exception as e:
                print(f"⚠️ Could not initialize guardrails: {e}")
                print(f"{self.name} initialized with NVIDIA LLM (no guardrails)")
        else:
            print(f"{self.name} initialized with NVIDIA LLM!")
    
    def analyze_complaint(self, user_complaint, scraped_laws, violations_data):
        """
        Uses NVIDIA LLM to analyze complaint against real legal data
        """
        # Check if we're in mock mode
        if self.mock_mode:
            print(f"\n{self.name} analyzing complaint [MOCK MODE]...")
            from .mock_responses import MockNVIDIAResponses
            mock_result = MockNVIDIAResponses.mock_analyzer_response(user_complaint)
            mock_result["source"] = "Mock Demo Mode"
            return mock_result
        
        print(f"\n{self.name} analyzing complaint with NVIDIA AI...")
        
        # Build the prompt for the LLM with JSON structure request
        prompt = f"""You are a legal document analyst specializing in NYC tenant law.
            Analyze this tenant complaint and identify which NYC housing laws apply.

            TENANT COMPLAINT: {user_complaint}

            BUILDING VIOLATION HISTORY: {violations_data[:3] if violations_data else "No violation history"}
            
            Based on your knowledge of NYC tenant law, identify the specific laws that apply to this complaint.
            Include statute numbers when possible (e.g., NYC Admin Code §27-2009)

            Respond in JSON format with these exact fields:
            {{
                "is_legitimate": "Yes" or "No",
                "applicable_laws": ["list", "of", "statute", "numbers"],
                "case_strength": "Weak" or "Moderate" or "Strong",
                "evidence_needed": ["list", "of", "evidence", "to", "collect"],
                "recommended_actions": ["list", "of", "actions", "to", "take"]
            }}

            Provide factual information only. Do not give legal advice."""

        # Call NVIDIA LLM with or without guardrails
        if self.guardrails:
            # Use NeMo Guardrails for safe AI interaction
            response_content = self.guardrails.generate(messages=[{"role": "user", "content": prompt}])
            response = type('Response', (), {'content': response_content})()
        else:
            # Direct LLM call
            response = self.llm.invoke(prompt)
        
        # Parse the structured response
        try:
            import json
            import re
            
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                parsed_data = json.loads(json_match.group())
                
                # Return structured analysis
                return {
                    "is_legitimate": parsed_data.get("is_legitimate", "Unknown"),
                    "applicable_laws": parsed_data.get("applicable_laws", []),
                    "case_strength": parsed_data.get("case_strength", "Unknown"),
                    "evidence_needed": parsed_data.get("evidence_needed", []),
                    "recommended_actions": parsed_data.get("recommended_actions", []),
                    "analysis": response.content,  # Keep raw response for fallback
                    "source": "NVIDIA Llama 3.1 70B"
                }
            else:
                raise ValueError("No JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️ Could not parse structured response: {e}")
            print("Falling back to raw text analysis...")
            
            # Fallback to original format
            return {
                "analysis": response.content,
                "source": "NVIDIA Llama 3.1 70B",
                "parsing_error": str(e)
            }

# Test the agent
if __name__ == "__main__":
    agent = AnalyzerAgent()
    
    # Test with sample complaint
    test_complaint = "My landlord entered without notice and there's no heat"
    result = agent.analyze_complaint(test_complaint, [], [])
    
    print("\nAnalysis Result:")
    for key, value in result.items():
        print(f"{key}: {value}")