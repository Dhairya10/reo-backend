from models.keywords import KeywordBase
from utils.auth import get_supabase
from fastapi import Depends
from config.logger import logger

async def process_keyword(keyword: KeywordBase, user_id: str, supabase=Depends(get_supabase)):
    """
    Calls a Supabase Edge Function to process a keyword asynchronously.
    """
    try:
        # Call the Supabase Edge Function without waiting for the response
        supabase.functions().invoke(
            'process-keyword',
            {
                'keyword': keyword.word,
                'user_id': user_id
            },
            invoke_options={"sync": False}  # This makes the call asynchronous
        )
    except Exception as e:
        # Log the error but don't raise an exception
        logger.error(f"Error calling keyword processing function: {str(e)}")