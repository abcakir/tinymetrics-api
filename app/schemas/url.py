from pydantic import BaseModel, HttpUrl
from datetime import datetime

class UrlCreate(BaseModel):
    original_url: HttpUrl

# Was die API zurückgibt
class UrlResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    click_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class UrlStats(UrlResponse):
    pass