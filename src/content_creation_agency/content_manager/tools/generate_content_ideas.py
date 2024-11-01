from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from openai import OpenAI
import time
from typing import List
import openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHANNEL_INFO = """
Arsenii Shatokhin runs a YouTube channel focused on AI, sharing content related to AI agents and their development. The channel features two main types of videos:
1. Walkthrough/coding tutorials: Detailed guides on AI-related topics
2. Perspective videos: Insights on new releases, features, and predictions for the future of AI

Key aspects:
- Target Audience: Primarily individuals aged 25 and older, with a significant portion in the 35-plus demographic
- High-Performing Content: Videos presenting a business perspective perform particularly well
- Growth Goal: Aiming to reach 50,000 subscribers
- Notable Success: One of the most successful videos discusses how GPT-4 will transform technology
- Content Appeal: Designed for both AI enthusiasts and professionals looking to leverage AI technology in business
- Business Integration: The channel drives interest in Arsenii's AI consultancy and product offerings, including the flagship platform, Agencii AI
"""

class GenerateContentIdeas(BaseTool):
    """
    A tool to generate content ideas using OpenAI's latest model, tailored for Arsenii Shatokhin's YouTube channel.
    It receives comprehensive reports from the Content Manager, which include trend analysis and YouTube channel insights,
    and generates content ideas that align with the channel's audience and style.
    """
    prompt: str = Field(..., description="Full prompt to generate content ideas, focusing on what could perform best based on research.")
    successful_video_titles: List[str] = Field(..., description="List of titles of videos that have performed well on the channel.")
    content_gap_topics: str = Field(..., description="Topics identified as content gaps in the market.")
    recent_trends: str = Field(..., description="Recent trends in AI and related fields.")

    def run(self):
        """
        Generate content ideas using OpenAI's latest model, incorporating channel-specific information.
        """
        full_prompt = f"""
        {CHANNEL_INFO}

        Based on the above channel information and the following additional context, generate 5 content ideas:
        {self.prompt}

        Consider these successful video titles: {', '.join(self.successful_video_titles)}
        Content gap topics to address: {self.content_gap_topics}
        Recent trends to incorporate: {self.recent_trends}

        For each idea, provide:
        1. A catchy title
        2. A brief description of the content
        3. Potential business tie-ins (if applicable)
        """

        max_retries = 5
        retry_delay = 1  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="o1-preview",
                    messages=[
                        {"role": "user", "content": full_prompt}
                    ],
                )
                return response.choices[0].message.content.strip()
            except openai.error.RateLimitError:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    return "Error: Rate limit exceeded. Please try again later."
            except Exception as e:
                return f"Error generating content ideas: {str(e)}"

if __name__ == "__main__":
    tool = GenerateContentIdeas(
        prompt="Focus on recent advancements in AI agents and their potential impact on businesses.",
        successful_video_titles=["How GPT-4 Will Transform Technology", "AI Agents: The Future of Business Automation"],
        content_gap_topics="Practical applications of AI in small businesses, Ethical considerations in AI development",
        recent_trends="Advancements in multimodal AI models, Emergence of AI-powered personal assistants"
    )
    print(tool.run())
