from fastapi.security import HTTPBearer
from fastapi import Request
from config.settings import TEST_USER_ID

security = HTTPBearer()

async def get_supabase(request: Request):
    return request.app.state.supabase

async def get_current_user():
    return {"id": TEST_USER_ID}


'''
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase)
):
    token = credentials.credentials
    try:
        # Verify the token with Supabase
        user = supabase.auth.get_user(token)
        return user.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
'''