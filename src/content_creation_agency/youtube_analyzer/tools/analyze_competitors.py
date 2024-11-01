from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

class AnalyzeCompetitors(BaseTool):
    """
    A tool to analyze competitors on YouTube.
    """
    keywords: str = Field(..., description="Keywords to search for competitor channels.")
    max_results: int = Field(5, description="The number of competitor channels to analyze.")

    def run(self):
        """
        Analyze competitors based on the given keywords.
        """
        try:
            # Search for channels
            search_response = youtube.search().list(
                q=self.keywords,
                type='channel',
                part='id,snippet',
                maxResults=self.max_results
            ).execute()

            result = "Competitor Analysis:\n\n"
            for item in search_response['items']:
                channel_id = item['id']['channelId']
                channel_title = item['snippet']['title']

                # Get channel statistics
                channel_response = youtube.channels().list(
                    part='statistics',
                    id=channel_id
                ).execute()

                stats = channel_response['items'][0]['statistics']

                result += f"Channel ID: {channel_id}\n"
                result += f"Channel: {channel_title}\n"
                result += f"Subscribers: {stats['subscriberCount']}\n"
                result += f"Total Views: {stats['viewCount']}\n"
                result += f"Total Videos: {stats['videoCount']}\n\n"

            return result
        except Exception as e:
            return f"Error analyzing competitors: {str(e)}"

if __name__ == "__main__":
    tool = AnalyzeCompetitors(keywords="AI technology youtube channels")
    print(tool.run())
