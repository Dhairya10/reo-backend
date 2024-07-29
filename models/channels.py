from pydantic import BaseModel, UUID4

class BlockedChannel(BaseModel):
    user_id: UUID4
    channel_id: UUID4

    class Config:
        from_attributes = True

class ChannelResponse(BaseModel):
    id: UUID4
    name: str
    description: str | None = None
    external_id: str
    is_blocked: bool

    class Config:
        from_attributes = True