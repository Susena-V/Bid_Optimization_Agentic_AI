from crewai.tools import BaseTool
from typing import Type,Union,Dict,Any
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: Union[str, Dict[str, Any]] = Field(..., description="Tell us what the users wants to answer")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
class HumanTool(BaseTool):
    name: str = "Human interact"
    description: str = "Ask questions to the user to collect information"
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: Union[str, Dict[str, Any]]) -> str:
        if isinstance(argument, dict):
            description = argument.get("description")
            if not description:  # If "description" key is missing or empty
                return "Invalid input: Missing description key. Please provide a valid prompt."
            return input(f"{description} \n")
    
        if isinstance(argument, str) and argument.strip():
            return input(f"{argument.strip()} \n")
    
    # Fallback if argument is neither string nor dict or is invalid
        return "Invalid input provided. Please check the input format."
