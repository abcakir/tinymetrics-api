from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime

class UrlCreate(BaseModel):
    original_url: HttpUrl

    @field_validator("original_url", mode="before")
    @classmethod
    def enforce_https(cls, v):
        if isinstance(v, str) and not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

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