from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List
from models.keywords import KeywordBase, Keyword
from config.logger import logger
from utils.auth import get_supabase, get_current_user
from services.keyword_service import process_keyword

router = APIRouter(prefix="/keywords", tags=["keywords"])

@router.post("/", response_model=dict)
async def add_keyword(keyword: KeywordBase, background_tasks: BackgroundTasks, supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        # Schedule the processing task in the background
        background_tasks.add_task(process_keyword, keyword, current_user.id, supabase)
        
        logger.info(f"Keyword processing initiated for user {current_user.id}: {keyword.word}")
        return {"message": "Keyword processing initiated"}
    except Exception as e:
        logger.error(f"Error initiating keyword processing for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[Keyword])
async def get_keywords(supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('user_keywords').select('*').eq('user_id', current_user.id).execute()
        
        if response.data:
            keywords = [Keyword(**keyword) for keyword in response.data]
            logger.info(f"Fetched {len(keywords)} keywords for user {current_user.id}")
            return keywords
        else:
            logger.info(f"No keywords found for user {current_user.id}")
            return []
    except Exception as e:
        logger.error(f"Error fetching keywords for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")