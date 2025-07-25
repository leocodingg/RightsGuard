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
            'main': 'https://www.nyc.gov/site/rentguidelinesboard/tenants/tenants-rights.page',
            'complaints': 'https://www.nyc.gov/site/hpd/services-and-information/tenants.page'
        }
        
        print(f"{self.name} initialized!")
    def get_webpage(self, url):
        try:
            # Make request look like it's from a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(url, headers=headers, timeout=10)
            return response.text
        except Exception as e:
            print(f"Error getting {url}: {e}")
            return None
        
    def extract_legal_info(self, html_content, keywords):
        # Helps parse the html easier
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all paragraphs
        relevant_info = []

        # Look in multiple tag types, not just <p>
        for element in soup.find_all(['p', 'div', 'li', 'span']):
            text = element.get_text().lower()

            for keyword in keywords:
                if keyword.lower() in text:
                    content = element.get_text().strip()
                    if len(content) > 20:  # Skip tiny snippets
                        relevant_info.append(content)
                        break # so don't add the same element twice

        return relevant_info

# Test it - this only runs if we run this file directly
if __name__ == "__main__":
    agent = WebScraperAgent()
    print(f"Agent has these URLs: {agent.nyc_urls}")

    # Test with a simple page first
    test_url = "https://en.wikipedia.org/wiki/Landlord"
    content = agent.get_webpage(test_url)

    if not content:
        print("didnt get webpage")
    else: 
        print("success")
        # Test extraction on Wikipedia
        wiki_keywords = ['tenant', 'landlord', 'rent']
        wiki_info = agent.extract_legal_info(content, wiki_keywords)
        print(f"\nWikipedia test - Found {len(wiki_info)} paragraphs")

      # Test with NYC tenant rights page
    print("\n--- Testing legal info extraction ---")
    nyc_url = agent.nyc_urls['main']
    nyc_content = agent.get_webpage(nyc_url)

    if nyc_content:
        keywords = ['landlord', 'tenant', 'notice', 'entry', 'repair']
        legal_info = agent.extract_legal_info(nyc_content, keywords)

        print(f"Found {len(legal_info)} relevant paragraphs")
        
        # Debug: Let's see what tags the page uses
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(nyc_content, 'html.parser')
        print(f"\nDebug - Total <p> tags: {len(soup.find_all('p'))}")
        print(f"Debug - Total <div> tags: {len(soup.find_all('div'))}")
        
        # Check if content is in divs instead
        print("\nFirst 500 chars of page text:")
        print(soup.get_text()[:500])

        # Show first 2 paragraphs
        for i, para in enumerate(legal_info[:2]):
            print(f"\nParagraph {i+1}:")
            print(para[:200] + "..." if len(para) > 200 else para)
    else:
        print("Failed to get NYC page")