from agency_swarm.tools import BaseTool
from pydantic import Field
from pytrends.request import TrendReq
import pandas as pd

class AnalyzeTrends(BaseTool):
    """
    A tool to analyze keyword trends using pytrends.
    """
    keywords: str = Field(..., description="Comma-separated list of keywords to analyze.")
    timeframe: str = Field("today 3-m", description="Timeframe for the trend analysis.")

    def run(self):
        """
        Analyze keyword trends using pytrends.
        """
        try:
            pytrends = TrendReq(hl='en-US', tz=360)
            kw_list = [kw.strip() for kw in self.keywords.split(',')]
            pytrends.build_payload(kw_list, cat=0, timeframe=self.timeframe, geo='', gprop='')
            
            interest_over_time_df = pytrends.interest_over_time()
            
            # Calculate average interest for each keyword
            avg_interest = interest_over_time_df.mean().sort_values(ascending=False)
            
            result = "Trend Analysis Results:\n\n"
            for kw, score in avg_interest.items():
                if kw != 'isPartial':
                    result += f"{kw}: {score:.2f}\n"
            
            return result
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"

if __name__ == "__main__":
    tool = AnalyzeTrends(keywords="artificial intelligence, machine learning, deep learning")
    print(tool.run())
