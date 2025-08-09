from typing import List, Dict, Any,Optional
from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the story option shown to user")
    nextNode: Dict[str, Any] = Field(description="The next node in the story that this option leads to")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether this node is an ending node")
    isWinningEnding: bool = Field(description="Whether this ending node is a winning ending")
    options: Optional[List[StoryOptionLLM]] = Field(description="List of options available at this node")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story, containing the starting situation and options")
    