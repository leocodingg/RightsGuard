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


# Test it - this only runs if we run this file directly
if __name__ == "__main__":
    agent = WebScraperAgent()
    print(f"Agent has these URLs: {agent.nyc_urls}")