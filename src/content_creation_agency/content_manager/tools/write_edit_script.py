from agency_swarm.tools import BaseTool
from pydantic import Field
import os

class WriteEditScript(BaseTool):
    """
    A tool to write and edit scripts in Markdown format and save them locally.
    """
    content: str = Field(..., description="The content of the script to write or edit.")
    filename: str = Field(..., description="The filename to save the script as (including .md extension).")

    def run(self):
        """
        Write or edit a script and save it locally.
        """
        try:
            script_dir = os.path.join(os.getcwd(), "scripts")
            os.makedirs(script_dir, exist_ok=True)
            file_path = os.path.join(script_dir, self.filename)
            
            with open(file_path, "w") as f:
                f.write(self.content)
            
            return f"Script successfully saved to {file_path}"
        except Exception as e:
            return f"Error writing/editing script: {str(e)}"

if __name__ == "__main__":
    tool = WriteEditScript(content="# Sample Script\n\nThis is a test script.", filename="test_script.md")
    print(tool.run())
