from pydantic import BaseModel
from typing import Optional, Any
from datetime import date

class VideoStaticBase(BaseModel):
    aid: int
    bvid: str
    pubdate: int
    title: str
    description: Optional[str] = None
    tag: Optional[str] = None
    pic: Optional[str] = None
    type_id: Optional[int] = None
    user_id: Optional[int] = None
    priority: Optional[int] = None

class VideoStaticCreate(VideoStaticBase):
    pass

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
    time: int
    aid: int
    bvid: str
    coin: int
    favorite: int
    danmaku: int
    view: int
    reply: int
    share: int
    like: int

class VideoMinuteCreate(VideoMinuteBase):
    pass

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