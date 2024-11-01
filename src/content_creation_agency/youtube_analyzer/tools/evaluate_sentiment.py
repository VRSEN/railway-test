from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from textblob import TextBlob

load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

class EvaluateSentiment(BaseTool):
    """
    A tool to evaluate sentiment in YouTube video comments.
    """
    video_id: str = Field(..., description="The ID of the YouTube video to analyze comments from.")
    max_comments: int = Field(100, description="The maximum number of comments to analyze.")
    top_n: int = Field(5, description="The number of top comments to return based on sentiment.")

    def run(self):
        """
        Evaluate sentiment in comments of the specified YouTube video and return top comments.
        """
        try:
            comments = []
            nextPageToken = None

            while len(comments) < self.max_comments:
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=self.video_id,
                    maxResults=min(100, self.max_comments - len(comments)),
                    pageToken=nextPageToken,
                    textFormat='plainText'
                ).execute()

                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)

                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break

            # Perform sentiment analysis
            sentiments = [(comment, TextBlob(comment).sentiment.polarity) for comment in comments]
            avg_sentiment = sum(sentiment for _, sentiment in sentiments) / len(sentiments)

            # Sort comments by sentiment score
            top_comments = sorted(sentiments, key=lambda x: x[1], reverse=True)[:self.top_n]

            result = f"Sentiment Analysis for Video ID: {self.video_id}\n"
            result += f"Number of comments analyzed: {len(comments)}\n"
            result += f"Average sentiment score: {avg_sentiment:.2f}\n"
            result += f"Sentiment interpretation: "
            if avg_sentiment > 0.05:
                result += "Positive"
            elif avg_sentiment < -0.05:
                result += "Negative"
            else:
                result += "Neutral"
            result += "\n\nTop Comments:\n"

            for comment, sentiment in top_comments:
                result += f"Sentiment: {sentiment:.2f} - Comment: {comment}\n"

            return result
        except Exception as e:
            return f"Error evaluating sentiment: {str(e)}"

if __name__ == "__main__":
    tool = EvaluateSentiment(video_id="hb0j9Qn-KjM", top_n=5)
    print(tool.run())
