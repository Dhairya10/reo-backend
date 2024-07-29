from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class AnonymousSignUpRequest(BaseModel):
    metadata: Optional[Dict] = None
    captcha_token: Optional[str] = None

class AuthResponse(BaseModel):
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    is_anonymous: bool = False