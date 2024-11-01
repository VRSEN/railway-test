from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

class TavilySearch(BaseTool):
    """
    A tool to search the web using the Tavily API.
    """
    query: str = Field(..., description="The search query to be used.")

    def run(self):
        """
        Perform a web search using the Tavily API.
        """
        try:
            response = tavily_client.search(self.query)
            return str(response)
        except Exception as e:
            return f"Error performing Tavily search: {str(e)}"

if __name__ == "__main__":
    tool = TavilySearch(query="Latest AI trends in 2023")
    print(tool.run())
