from agency_swarm import Agency
from .content_manager.content_manager import ContentManager
from .trend_analyzer.trend_analyzer import TrendAnalyzer
from .youtube_analyzer.youtube_analyzer import YouTubeAnalyzer

content_manager = ContentManager()
trend_analyzer = TrendAnalyzer()
youtube_analyzer = YouTubeAnalyzer()

agency = Agency([
    content_manager,  # Content Manager will be the entry point for communication with the user
    [content_manager, trend_analyzer],  # Content Manager can communicate with Trend Analyzer
    [content_manager, youtube_analyzer],  # Content Manager can communicate with YouTube Analyzer
    ],
    shared_instructions='agency_manifesto.md',
    temperature=0.7,
    max_prompt_tokens=25000
)

if __name__ == "__main__":
    agency.demo_gradio()