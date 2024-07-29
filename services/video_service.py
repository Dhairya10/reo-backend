from supabase import Client
from models.videos import AllowedVideo
from typing import List
from config.logger import logger

class VideoService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    async def get_allowed_videos(self, child_id: str) -> List[AllowedVideo]:
        try:
            # Fetch blocked channels for the child
            blocked_channels = await self._get_blocked_channels(child_id)
            
            # Fetch blocked keywords for the child
            blocked_keywords = await self._get_blocked_keywords(child_id)
            
            # Fetch all videos
            all_videos = await self._get_all_videos()
            
            # Filter videos
            allowed_videos = [
                video for video in all_videos
                if video.channel_id not in blocked_channels and
                not any(keyword in video.title.lower() or keyword in video.description.lower() 
                        for keyword in blocked_keywords)
            ]
            
            logger.info(f"Retrieved {len(allowed_videos)} allowed videos for child {child_id}")
            return allowed_videos
        except Exception as e:
            logger.error(f"Error getting allowed videos: {str(e)}")
            raise

    async def _get_blocked_channels(self, child_id: str) -> List[str]:
        # Implementation to fetch blocked channels from Supabase
        pass

    async def _get_blocked_keywords(self, child_id: str) -> List[str]:
        # Implementation to fetch blocked keywords from Supabase
        pass

    async def _get_all_videos(self) -> List[AllowedVideo]:
        # Implementation to fetch all videos from Supabase
        pass