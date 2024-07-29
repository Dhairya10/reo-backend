from pydantic import BaseModel, UUID4
from datetime import date

class ProfileBase(BaseModel):
    full_name: str
    date_of_birth: date

class Profile(ProfileBase):
    id: UUID4