from agency_swarm import Agent
from .tools.tavily_search import TavilySearch

class TrendAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="Trend Analyzer",
            description="Analyzes the latest AI trends and identifies content gaps.",
            instructions="./instructions.md",
            tools=[TavilySearch],
            temperature=0.5,
            max_prompt_tokens=25000,
        )
