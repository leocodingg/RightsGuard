# AnalyzerAgent - Compares tenant complaints to legal information
import os
from typing import Dict, List
from langchain_nvidia_ai_endpoints import ChatNVIDIA

class AnalyzerAgent:
    def __init__(self):
        # Give the agent a name
        self.name = "AnalyzerAgent"
        
        # Get API key from environment
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")
        
        # Initialize NVIDIA LLM - this is our connection to the AI
        self.llm = ChatNVIDIA(
            model="meta/llama-3.1-70b-instruct",
            api_key=api_key,
            temperature=0.1  # Low temperature for consistent legal analysis
        )
        
        print(f"{self.name} initialized with NVIDIA LLM!")
    
    def analyze_complaint(self, user_complaint, scraped_laws, violations_data):
        """
        Uses NVIDIA LLM to analyze complaint against real legal data
        """
        print(f"\n{self.name} analyzing complaint with NVIDIA AI...")
        
        # Build the prompt for the LLM
        prompt = f"""You are a legal document analyst specializing in NYC tenant law.
            Analyze this tenant complaint against NYC housing laws and provide a structured analysis.

            TENANT COMPLAINT: {user_complaint}

            RELEVANT NYC LAWS: {scraped_laws if scraped_laws else "No specific laws provided"}

            BUILDING VIOLATION HISTORY: {violations_data[:3] if violations_data else "No violation history"}

            Please analyze and provide:
            1. Is this a legitimate legal issue? (Yes/No)
            2. What specific NYC laws apply? (List statute numbers)
            3. How strong is the case? (Weak/Moderate/Strong)
            4. What evidence should the tenant collect?
            5. What action should they take?

            Provide factual information only. Do not give legal advice."""

        # Call NVIDIA LLM - this is where we talk to the AI
        response = self.llm.invoke(prompt)
        
        # Parse and return the AI's response
        return {
            "analysis": response.content,
            "source": "NVIDIA Llama 3.1 70B"
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