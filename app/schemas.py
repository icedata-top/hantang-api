from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import date, datetime, timezone

class VideoStaticBase(BaseModel):
    aid: int
    bvid: str
    pubdate: datetime
    title: str
    description: Optional[str] = None
    tag: Optional[str] = None
    pic: Optional[str] = None
    type_id: Optional[int] = None
    user_id: Optional[int] = None
    priority: Optional[int] = None
    updated_at: Optional[datetime] = None

class VideoStaticCreate(VideoStaticBase):
    @field_validator("pubdate", mode="before")
    @classmethod
    def parse_pubdate(cls, v):
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v

class VideoStatic(VideoStaticBase):
    class Config:
        from_attributes = True

class VideoDynamicBase(BaseModel):
    record_date: date
    aid: int
    bvid: str
    coin: int
    favorite: int
    danmaku: int
    view: int
    reply: int
    share: int
    like: int

class VideoDynamicCreate(VideoDynamicBase):
    pass

class VideoDynamic(VideoDynamicBase):
    class Config:
        from_attributes = True

class VideoMinuteBase(BaseModel):
    time: datetime
    aid: int
    coin: int
    favorite: int
    danmaku: int
    view: int
    reply: int
    share: int
    like: int

class VideoMinuteCreate(VideoMinuteBase):
    @field_validator("time", mode="before")
    @classmethod
    def parse_time(cls, v):
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v

class VideoMinute(VideoMinuteBase):
    class Config:
        from_attributes = True

class SuccessResponse(BaseModel):
    result: Any
    time: float
    status: str

class ErrorResponse(BaseModel):
    status: str
    message: str