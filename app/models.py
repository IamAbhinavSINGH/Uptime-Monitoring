from pydantic import BaseModel, HttpUrl, validator
import aiohttp
from typing import Optional

class Website(BaseModel):
    url: HttpUrl
    name: Optional[str] = None
    check_interval_seconds: Optional[int] = 300
    expected_status_code: Optional[int] = 200

    @validator('check_interval_seconds')
    def validate_interval(cls, v):
        if v is not None and v < 5:
            raise ValueError('Check interval must be at least 60 seconds')
        return v

    @validator('expected_status_code')
    def validate_status_code(cls, v):
        if v is not None and not (100 <= v <= 599):
            raise ValueError('Status code must be between 100 and 599')
        return v

class WebsiteResponse(BaseModel):
    id: str
    url: str
    name: Optional[str]
    check_interval_seconds: int
    expected_status_code: int

