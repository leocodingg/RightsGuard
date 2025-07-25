# Let's build this together step by step!
import requests  # This lets us download web pages

class WebScraperAgent:
    def __init__(self):
        """
        This runs when we create a new WebScraperAgent
        Think of it like setting up your workspace before starting
        """
        # We'll need these later:
        self.name = "WebScraperAgent"
        
        # URLs we know are good for NYC tenant info
        self.nyc_urls = {
            'main': 'https://www1.nyc.gov/site/hpd/renters/your-rights.page',
            'complaints': 'https://www1.nyc.gov/site/hpd/renters/file-a-complaint.page'
        }
        
        print(f"{self.name} initialized!")
    def get_webpage(self, url):
        try:
            # get the webpage
            response = requests.get(url)
            return response.text
        except:
            print(f"Error getting {url}")
            return None
        
    def extract_legal_info(self, html_content, keywords):
        # Helps parse the html easier
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all paragraphs
        relevant_info = []

        for paragraph in soup.find_all("p"):
            text = paragraph.get_text().lower()

            for keyword in keywords:
                if keyword.lower() in text:
                    relevant_info.append(paragraph.get_text())
                    break # so don't add the same paragraph twice

        return relevant_info

# Test it - this only runs if we run this file directly
if __name__ == "__main__":
    agent = WebScraperAgent()
    print(f"Agent has these URLs: {agent.nyc_urls}")

    test_url = "https://github.com"
    content = agent.get_webpage(test_url)

    if not content:
        print("didnt get webpage")
    else: 
        print("success")

      # Test with NYC tenant rights page
    print("\n--- Testing legal info extraction ---")
    nyc_url = agent.nyc_urls['main']
    nyc_content = agent.get_webpage(nyc_url)

    if nyc_content:
        keywords = ['landlord', 'tenant', 'notice', 'entry', 'repair']
        legal_info = agent.extract_legal_info(nyc_content, keywords)

        print(f"Found {len(legal_info)} relevant paragraphs")

        # Show first 2 paragraphs
        for i, para in enumerate(legal_info[:2]):
            print(f"\nParagraph {i+1}:")
            print(para[:200] + "..." if len(para) > 200 else para)
    else:
        print("Failed to get NYC page")