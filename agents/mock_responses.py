# Mock responses for demo if NVIDIA API is unavailable
import time
import random

class MockNVIDIAResponses:
    """Simulated responses that look like real NVIDIA LLM output"""
    
    @staticmethod
    def mock_analyzer_response(complaint):
        """Simulate AnalyzerAgent response"""
        time.sleep(1)  # Simulate API delay
        
        responses = {
            "entry": {
                "is_legitimate": "Yes",
                "applicable_laws": ["NYC Admin Code §27-2009", "NYS Real Property Law §235-b"],
                "case_strength": "Strong",
                "evidence_needed": ["Photos of entries", "Written notices", "Witness statements"],
                "recommended_actions": ["Send certified letter", "File complaint with HPD", "Contact tenant union"]
            },
            "heat": {
                "is_legitimate": "Yes", 
                "applicable_laws": ["NYC Housing Code §27-2029", "Heat Season Oct 1 - May 31"],
                "case_strength": "Strong",
                "evidence_needed": ["Temperature readings", "Date/time logs", "Photos of thermostat"],
                "recommended_actions": ["Call 311 immediately", "Document all incidents", "Request HPD inspection"]
            },
            "default": {
                "is_legitimate": "Yes",
                "applicable_laws": ["NYC Housing Maintenance Code", "NYS Tenant Protection Act"],
                "case_strength": "Moderate",
                "evidence_needed": ["Documentation of issue", "Communication with landlord", "Photos"],
                "recommended_actions": ["Document everything", "Send written notice", "Seek legal consultation"]
            }
        }
        
        # Detect complaint type
        complaint_lower = complaint.lower()
        if "entry" in complaint_lower or "enter" in complaint_lower:
            return responses["entry"]
        elif "heat" in complaint_lower or "cold" in complaint_lower:
            return responses["heat"]
        else:
            return responses["default"]
    
    @staticmethod
    def mock_letter_response(analysis, tenant_info):
        """Simulate LetterAgent response"""
        time.sleep(1)  # Simulate API delay
        
        date = tenant_info.get("date", "January 15, 2024")
        name = tenant_info.get("name", "Tenant")
        landlord = tenant_info.get("landlord", "Landlord")
        address = tenant_info.get("address", "Property Address")
        
        laws = analysis.get("applicable_laws", ["NYC Housing Code"])
        law_text = ", ".join(laws)
        
        letter = f"""
{date}

{landlord}
Re: {address}

Dear {landlord},

I am writing to formally notify you of serious violations of my tenant rights at the above-referenced property.

The following issues constitute violations of {law_text}:

{analysis.get('recommended_actions', ['Please address these issues immediately'])[0]}

This letter serves as formal notice of these violations. I request immediate action to remedy these issues within the timeframe required by law.

Please contact me within 5 business days to discuss resolution of these matters.

Sincerely,
{name}

cc: NYC Housing Preservation & Development
    Tenant Union Representative
        """
        
        return {
            "letter_content": letter.strip(),
            "status": "success"
        }

# Modify agents to use mock mode
MOCK_MODE = False  # Set to True if no API key

def enable_mock_mode():
    """Enable mock mode for demo"""
    global MOCK_MODE
    MOCK_MODE = True
    print("⚠️ Running in MOCK MODE - simulated responses for demo")