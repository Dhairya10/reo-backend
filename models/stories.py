from pydantic import BaseModel
from typing import List
from datetime import datetime

class GeneratedStoryBase(BaseModel):
    topic: str
    characters: List[str]
    duration: int

class GeneratedStoryCreate(GeneratedStoryBase):
    pass

class GeneratedStory(GeneratedStoryBase):
    id: str
    user_id: str
    story_text: str
    audio_url: str
    created_at: datetime

    class Config:
        from_attributes = True