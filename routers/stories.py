from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.stories import GeneratedStoryCreate, GeneratedStory
from supabase import Client
from utils.auth import get_current_user, get_supabase
from config.logger import logger
from services.story_service import StoryService

router = APIRouter(prefix="/stories", tags=["stories"])

async def get_story_service(supabase: Client = Depends(get_supabase)):
    return StoryService(supabase)

@router.post("/create", response_model=GeneratedStory)
async def create_story(
    story: GeneratedStoryCreate, 
    story_service: StoryService = Depends(get_story_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        logger.info(f"Attempting to create story for user {current_user['id']}")
        created_story = await story_service.create_story(story, current_user['id'])
        return created_story
    except Exception as e:
        logger.error(f"Error creating story: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the story")

@router.get("/", response_model=List[GeneratedStory])
async def get_stories(
    child_id: str, 
    supabase: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    try:
        logger.info(f"Fetching stories for child {child_id} (user {current_user['id']})")
        response = supabase.table("generated_stories").select("*").eq("child_id", child_id).eq("user_id", current_user['id']).execute()
        stories = [GeneratedStory(**story) for story in response.data]
        logger.info(f"Successfully fetched {len(stories)} stories")
        return stories
    except Exception as e:
        logger.error(f"Error fetching stories: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching stories")