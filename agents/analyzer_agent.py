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
        Takes user's complaint and legal data, returns analysis
        """
        print(f"\n{self.name} analyzing complaint...")
        
        # Simple analysis for now
        found_violations = []
        
        # Check if complaint mentions any violation keywords
        complaint_lower = user_complaint.lower()
        
        for keyword, violation_type in self.violation_types.items():
            if keyword in complaint_lower:
                found_violations.append({
                    "type": violation_type,
                    "keyword": keyword,
                    "found": True
                })
        
        # Return results
        return {
            "complaint": user_complaint,
            "violations_found": found_violations,
            "total_found": len(found_violations)
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