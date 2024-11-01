from agency_swarm import Agent
from .tools.write_edit_script import WriteEditScript
from .tools.generate_content_ideas import GenerateContentIdeas
class ContentManager(Agent):
    def __init__(self):
        super().__init__(
            name="Content Manager",
            description="Responsible for generating content ideas and managing the content creation process.",
            instructions="./instructions.md",
            tools=[WriteEditScript, GenerateContentIdeas],
            temperature=0.7,
            max_prompt_tokens=25000,
        )
