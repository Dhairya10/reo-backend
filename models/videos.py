from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

class VideoLanguage(str, Enum):
    english = 'english'
    hindi = 'hindi'
    other = 'other'

class VideoCategory(str, Enum):
    entertainment = 'entertainment'
    learning = 'learning'
    sports = 'sports'
    news = 'news'
    music = 'music'
    gaming = 'gaming'
    other = 'other'

class Video(BaseModel):
    id: UUID4
    channel_id: UUID4
    title: str
    description: Optional[str]
    external_id: str
    keywords: List[UUID4]
    transcript: Optional[str]
    summary: Optional[str]
    category: VideoCategory
    language: VideoLanguage
    duration: Optional[timedelta]
    created_at: datetime
    updated_at: datetime

class AllowedVideo(BaseModel):
    video_id: UUID4
    external_id: str
    title: str
    channel_name: str
    category: VideoCategory
    language: VideoLanguage