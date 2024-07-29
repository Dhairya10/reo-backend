from pydantic import BaseModel, UUID4
from typing import List
from datetime import datetime, timedelta

class GeneratedStory(BaseModel):
    id: UUID4
    child_id: UUID4
    title: str
    topic: str
    characters: List[str]
    audio_url: str
    audio_duration: timedelta
    created_at: datetime
    updated_at: datetime

class GeneratedStoryCreate(BaseModel):
    child_id: UUID4
    title: str
    topic: str
    characters: List[str]
    audio_url: str
    audio_duration: timedelta