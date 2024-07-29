from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import UUID4
from models.channels import ChannelResponse
from config.logger import logger
from utils.auth import get_supabase, get_current_user

router = APIRouter(prefix="/channels", tags=["channels"])

@router.post("/block/{channel_id}", response_model=bool)
async def block_user_channel(channel_id: UUID4, supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('user_blocked_channels').insert({
            'user_id': current_user.id,
            'channel_id': str(channel_id)
        }).execute()
        
        if response.data:
            logger.info(f"Channel {channel_id} blocked for user {current_user.id}")
            return True
        else:
            logger.error(f"Failed to block channel {channel_id} for user {current_user.id}")
            return False
    except Exception as e:
        logger.error(f"Error blocking channel {channel_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/unblock/{channel_id}", response_model=bool)
async def unblock_user_channel(channel_id: UUID4, supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        response = supabase.table('user_blocked_channels').delete().match({
            'user_id': current_user.id,
            'channel_id': str(channel_id)
        }).execute()
        
        if response.data:
            logger.info(f"Channel {channel_id} unblocked for user {current_user.id}")
            return True
        else:
            logger.info(f"Channel {channel_id} not found in blocked list for user {current_user.id}")
            return False
    except Exception as e:
        logger.error(f"Error unblocking channel {channel_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[ChannelResponse])
async def get_user_channels(supabase=Depends(get_supabase), current_user=Depends(get_current_user)):
    try:
        # Fetch all channels
        channels_response = supabase.table('channels').select('id, name, description, external_id').execute()
        
        # Fetch blocked channels for the user
        blocked_channels_response = supabase.table('user_blocked_channels').select('channel_id').eq('user_id', current_user.id).execute()
        
        if channels_response.data:
            blocked_channel_ids = {item['channel_id'] for item in blocked_channels_response.data}
            
            user_channels = [
                ChannelResponse(
                    id=channel['id'],
                    name=channel['name'],
                    description=channel['description'],
                    external_id=channel['external_id'],
                    is_blocked=channel['id'] in blocked_channel_ids
                )
                for channel in channels_response.data
            ]
            
            logger.info(f"Fetched {len(user_channels)} channels for user {current_user.id}")
            return user_channels
        else:
            logger.info(f"No channels found")
            return []
    except Exception as e:
        logger.error(f"Error fetching channels for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")