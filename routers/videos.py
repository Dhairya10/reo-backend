from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from models.videos import AllowedVideo
from config.logger import logger
from utils.auth import get_supabase, get_current_user

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/videos/feed", response_model=List[AllowedVideo])
async def get_allowed_videos(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    supabase=Depends(get_supabase),
    current_user=Depends(get_current_user)
):
    try:
        # Calculate offset
        offset = (page - 1) * page_size

        # Prepare RPC parameters
        rpc_params = {
            'user_uuid': str(current_user.id),
            'p_limit': page_size,
            'p_offset': offset
        }

        # Call the RPC function
        response = supabase.rpc('get_allowed_videos_for_user_paginated', rpc_params).execute()
        
        if response.data:
            allowed_videos = [AllowedVideo(**video) for video in response.data]
            logger.info(f"Fetched {len(allowed_videos)} allowed videos for user {current_user.id} (page {page})")
            return allowed_videos
        else:
            logger.info(f"No allowed videos found for user {current_user.id} (page {page})")
            return []
    except Exception as e:
        logger.error(f"Error fetching allowed videos for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")





'''

# TODO : Remove after testing
import random
from uuid import uuid4


def generate_test_data() -> List[AllowedVideo]:
    external_ids = [
        "aWVwBHK99qk",
        "KUwqZAEfT00",
        "5nQ_Y4A_jhg",
        "RdgvZfDHyN8",
        "GJ8f60HFGLo",
        "iTxUIwXRTTg"
    ]
    
    channel_names = ["Ben and Holly", "Curious George"]
    title_list = ["Ben and Holly's Magical Adventures 1", "Curious George's Adventures 1", "Ben and Holly's Magical Adventures 2", "Curious George's Adventures 2", "Ben and Holly's Magical Adventures 3", "Curious George's Adventures 3"]
    
    test_data = []
    
    for external_id in external_ids:
        video = AllowedVideo(
            video_id=uuid4(),
            external_id=external_id,
            title=random.choice(title_list),
            channel_name=random.choice(channel_names),
            category="entertainment",
            language="english",
            description="Sample description",
            thumbnail_url="https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
        )
        test_data.append(video)
    
    return test_data


@router.get("/feed", response_model=List[AllowedVideo])
async def get_allowed_videos(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    supabase=Depends(get_supabase),
    current_user=Depends(get_current_user)
):
    try:
        # Generate test data instead of fetching from Supabase
        all_test_data = generate_test_data()
        
        # Calculate start and end indices for pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        # Slice the test data based on pagination
        paginated_data = all_test_data[start_index:end_index]
        
        # Ensure that each item in paginated_data is an instance of AllowedVideo
        allowed_videos = [
            AllowedVideo(
                video_id=str(video.video_id),
                external_id=video.external_id,
                title=video.title,
                channel_name=video.channel_name,
                category=video.category,
                language=video.language,
                description=video.description,
                thumbnail_url=video.thumbnail_url
            ) for video in paginated_data
        ]
        
        logger.info(f"Fetched {len(allowed_videos)} test videos")
        return allowed_videos
    except Exception as e:
        logger.error(f"Error in get_allowed_videos: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

'''