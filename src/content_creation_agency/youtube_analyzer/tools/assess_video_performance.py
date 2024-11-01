from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

class AssessVideoPerformance(BaseTool):
    """
    A tool to assess the performance of videos on a YouTube channel.
    """
    channel_id: str = Field(..., description="The ID of the YouTube channel to analyze.")
    max_results: int = Field(10, description="The number of videos to analyze.")

    def run(self):
        """
        Assess the performance of recent videos on the specified YouTube channel.
        """
        try:
            # Get channel's recent videos
            search_response = youtube.search().list(
                channelId=self.channel_id,
                type='video',
                part='id,snippet',
                order='date',
                maxResults=self.max_results
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response['items']]

            # Get video statistics
            videos_response = youtube.videos().list(
                part='statistics,snippet',
                id=','.join(video_ids)
            ).execute()

            result = "Video Performance Analysis:\n\n"
            for item in videos_response['items']:
                video_id = item['id']
                title = item['snippet']['title']
                views = item['statistics']['viewCount']
                likes = item['statistics'].get('likeCount', 'N/A')
                comments = item['statistics'].get('commentCount', 'N/A')

                result += f"Video ID: {video_id}\n"
                result += f"Title: {title}\n"
                result += f"Views: {views}\n"
                result += f"Likes: {likes}\n"
                result += f"Comments: {comments}\n\n"

            return result
        except Exception as e:
            return f"Error assessing video performance: {str(e)}"

if __name__ == "__main__":
    tool = AssessVideoPerformance(channel_id="UCSv4qL8vmoSH7GaPjuqRiCQ")
    print(tool.run())
