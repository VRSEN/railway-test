from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

class AnalyzeDemographics(BaseTool):
    """
    A tool to analyze demographics of a YouTube channel.
    """
    channel_id: str = Field("UCSv4qL8vmoSH7GaPjuqRiCQ", description="The ID of the YouTube channel to analyze. Default is Arsenii Shatokhin's channel.")

    def run(self):
        """
        Analyze demographics of the specified YouTube channel.
        """
        try:
            # Get channel statistics
            channel_response = youtube.channels().list(
                part='statistics',
                id=self.channel_id
            ).execute()

            # Get channel's top videos
            search_response = youtube.search().list(
                channelId=self.channel_id,
                type='video',
                part='id,snippet',
                order='viewCount',
                maxResults=10
            ).execute()

            # Compile results
            channel_stats = channel_response['items'][0]['statistics']
            top_videos = [item['snippet']['title'] for item in search_response['items']]

            result = f"Channel Statistics:\n"
            result += f"Subscribers: {channel_stats['subscriberCount']}\n"
            result += f"Total Views: {channel_stats['viewCount']}\n"
            result += f"Total Videos: {channel_stats['videoCount']}\n\n"
            result += "Top 10 Videos:\n"
            for i, title in enumerate(top_videos, 1):
                result += f"{i}. {title}\n"

            return result
        except Exception as e:
            return f"Error analyzing demographics: {str(e)}"

if __name__ == "__main__":
    tool = AnalyzeDemographics(channel_id="UCSv4qL8vmoSH7GaPjuqRiCQ")
    print(tool.run())
