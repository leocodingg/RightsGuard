# AnalyzerAgent - Compares tenant complaints to legal information

class AnalyzerAgent:
    def __init__(self):
        # Give the agent a name
        self.name = "AnalyzerAgent"
        
        # Common violation types we know about
        self.violation_types = {
            "heat": "Heat/Hot Water Issues",
            "entry": "Illegal Entry",
            "repair": "Maintenance Issues", 
            "notice": "Notice Violations"
        }
        
        print(f"{self.name} initialized!")
    
    def analyze_complaint(self, user_complaint, scraped_laws, violations_data):
        """
        Uses AI logic to analyze complaint against real legal data
        """
        print(f"\n{self.name} analyzing complaint with AI...")
        
        # Build analysis prompt for NVIDIA LLM (we'll use this later)
        analysis_prompt = f"""
Analyze this tenant complaint against NYC housing laws:

COMPLAINT: {user_complaint}
LAWS: {scraped_laws if scraped_laws else "No laws provided"}
VIOLATIONS: {violations_data if violations_data else "No violation history"}

Determine:
1. Is this legitimate? 
2. What law applies?
3. Case strength?
4. Evidence needed?
"""
        
        # For now, smart analysis (later: real NVIDIA API call)
        complaint_lower = user_complaint.lower()
        violations = []
        
        if "heat" in complaint_lower:
            violations.append("NYC Housing Code §27-2029 - Heat requirements")
        if "entry" in complaint_lower:
            violations.append("NYC Admin Code §27-2009 - Entry notice")
        
        return {
            "legitimate_issue": len(violations) > 0,
            "applicable_laws": violations,
            "case_strength": "Strong" if violations else "Weak",
            "evidence_needed": "Photos, dates, communications",
            "recommended_action": "Send complaint letter" if violations else "Gather evidence",
            "prompt_for_nvidia": analysis_prompt
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