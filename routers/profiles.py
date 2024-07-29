from fastapi import APIRouter, HTTPException, Depends
from models.profiles import ProfileBase, Profile
from config.logger import logger
from utils.auth import get_supabase, get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/", response_model=Profile)
async def add_profile(profile: ProfileBase, supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('profiles').insert({
            'id': str(current_user.id),
            'full_name': profile.full_name,
            'date_of_birth': profile.date_of_birth
        }).execute()
        
        if response.data:
            new_profile = Profile(**response.data[0])
            logger.info(f"Profile added successfully for user {current_user.id}")
            return new_profile
        else:
            logger.error(f"Failed to add profile for user {current_user.id}")
            raise HTTPException(status_code=400, detail="Failed to add profile")
    except Exception as e:
        logger.error(f"Error adding profile for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=Profile)
async def get_profile(supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('profiles').select('*').eq('id', str(current_user.id)).execute()
        
        if response.data:
            profile = Profile(**response.data[0])
            logger.info(f"Fetched profile for user {current_user.id}")
            return profile
        else:
            logger.info(f"No profile found for user {current_user.id}")
            raise HTTPException(status_code=404, detail="Profile not found")
    except Exception as e:
        logger.error(f"Error fetching profile for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")