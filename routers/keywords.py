from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.keywords import KeywordBase, Keyword
from config.logger import logger
from utils.auth import get_supabase, get_current_user
from services.keyword_service import process_keyword

router = APIRouter(prefix="/keywords", tags=["keywords"])

@router.post("/", response_model=dict)
async def add_keyword(keyword: KeywordBase, supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        result = await process_keyword(keyword, current_user['id'], supabase)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "data": {
                    "keyword_id": result["keyword_id"],
                    "affected_videos": result["affected_videos"]
                }
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        logger.error(f"Error processing keyword for user {current_user['id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[Keyword])
async def get_keywords(supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('user_blocked_keywords').select(
            '*,keywords(*)'
        ).eq('user_id', current_user['id']).execute()
        
        keywords = []
        if response.data:
            for keyword_data in response.data:
                if 'keyword_id' in keyword_data and 'keywords' in keyword_data:
                    keyword = Keyword(
                        id=keyword_data['keyword_id'],
                        word=keyword_data['keywords']['word'],
                        user_id=keyword_data['user_id']
                    )
                    keywords.append(keyword)
                else:
                    logger.warning(f"Skipping invalid keyword data: {keyword_data}")
            logger.info(f"Fetched {len(keywords)} keywords for user {current_user['id']}")
        else:
            logger.info(f"No keywords found for user {current_user['id']}")
        
        return keywords
    except Exception as e:
        logger.error(f"Error fetching keywords for user {current_user['id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{keyword_id}", response_model=dict)
async def delete_keyword(keyword_id: str, supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('user_blocked_keywords').delete().eq('keyword_id', keyword_id).eq('user_id', current_user['id']).execute()
        
        if response.data:
            logger.info(f"Keyword {keyword_id} deleted for user {current_user['id']}")
            return {"status": "success", "message": f"Keyword {keyword_id} deleted successfully"}
        else:
            logger.warning(f"Keyword {keyword_id} not found for user {current_user['id']}")
            raise HTTPException(status_code=404, detail="Keyword not found")
    except Exception as e:
        logger.error(f"Error deleting keyword {keyword_id} for user {current_user['id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")