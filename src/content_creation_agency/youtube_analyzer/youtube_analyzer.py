from agency_swarm import Agent
from .tools.analyze_demographics import AnalyzeDemographics
from .tools.assess_video_performance import AssessVideoPerformance
from .tools.analyze_competitors import AnalyzeCompetitors
from .tools.evaluate_sentiment import EvaluateSentiment
from .tools.extract_keywords import ExtractKeywords

class YouTubeAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="YouTube Analyzer",
            description="Analyzes YouTube channel performance, identifies content gaps, and evaluates competitors.",
            instructions="./instructions.md",
            tools=[AnalyzeDemographics, AssessVideoPerformance, AnalyzeCompetitors, EvaluateSentiment, ExtractKeywords],
            temperature=0.5,
            max_prompt_tokens=25000,
        )
