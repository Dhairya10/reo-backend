from fastapi import APIRouter, HTTPException, Depends, Body
from models.auth import SignUpRequest, SignInRequest, AuthResponse
from config.logger import logger
from utils.auth import get_supabase, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/sign-up-anonymous", response_model=AuthResponse)
# async def sign_up_anonymous(request: AnonymousSignUpRequest = Body(...), supabase=Depends(get_supabase)):
#     try:
#         response = supabase.auth.sign_in_anonymously(
#             credentials={
#                 "options": {
#                     "data": request.metadata,
#                     "captcha_token": request.captcha_token
#                 }
#             }
#         )
        
#         if response.user:
#             logger.info(f"Anonymous user signed up successfully: {response.user.id}")
#             return AuthResponse(
#                 user_id=response.user.id,
#                 email=response.user.email,
#                 name=response.user.user_metadata.get('name'),
#                 is_anonymous=True
#             )
#         else:
#             logger.error("Anonymous sign-up failed")
#             raise HTTPException(status_code=400, detail="Anonymous sign-up failed")
#     except Exception as e:
#         logger.error(f"Error during anonymous sign-up: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")
    
    
@router.post("/sign-up", response_model=AuthResponse)
async def sign_up(request: SignUpRequest = Body(...), supabase=Depends(get_supabase)):
    try:
        user = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password, 
            "options": {
                "data": {
                    "name": request.name
                }
            }
        })
        
        if user.user:
            logger.info(f"User signed up successfully: {user.user.id}")
            return AuthResponse(user_id=user.user.id, email=user.user.email, name=user.user.user_metadata['name'])
        else:
            logger.error("Sign-up failed")
            raise HTTPException(status_code=400, detail="Sign-up failed")
    except Exception as e:
        logger.error(f"Error during sign-up: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/sign-in", response_model=AuthResponse)
async def sign_in(request: SignInRequest, supabase=Depends(get_supabase)):
    try:
        user = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if user.user:
            logger.info(f"User signed in successfully: {user.user.id}")
            return AuthResponse(user_id=user.user.id, email=user.user.email, name=user.user.user_metadata['name'])
        else:
            logger.error("Sign-in failed")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"Error during sign-in: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/sign-out")
async def sign_out(supabase=Depends(get_supabase), current_user: dict = Depends(get_current_user)):
    supabase.auth.sign_out()
    logger.info(f"User signed out successfully: {current_user.id}")
    return {"message": "Signed out successfully"}


@router.get("/me", response_model=AuthResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return AuthResponse(user_id=current_user.id, email=current_user.email, name=current_user.user_metadata['name'])