from fastapi import FastAPI
import pymysql
from . import crud, schemas
import time
from typing import List, Union
from .biliapi import getSingleVideoInfo

pymysql.install_as_MySQLdb()

app = FastAPI()


@app.get("/", response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse])
def read_root():
    return {"Ping": "Pong", "time": 0.0, "status": "success", "result": "Hello World"}


@app.head("/health")
def health_check_head():
    return {"status": "success"}


@app.get(
    "/add_video_static",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
@app.post(
    "/add_video_static",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
async def add_video_static(avid: int = 0, bv: str = "", priority: int = 0):
    try:
        time_start = time.time()
        video_data = getSingleVideoInfo(avid, bv)
        result = await crud.add_video_static(video_data)
        if priority:
            video_data["priority"] = priority
        time_end = time.time()
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get(
    "/get_video_static_by_priority",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
async def get_video_static_by_priority(piority: int = 0):
    try:
        time_start = time.time()
        db_results = await crud.get_video_static_by_priority(piority)
        # Convert SQLAlchemy models to Pydantic models
        result = [schemas.VideoStatic.model_validate(video) for video in db_results]
        time_end = time.time()
        data = {
            "result": result,
            "time": time_end - time_start,
            "status": "success",
        }
        print(f"Time: {time_end - time_start}")
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post(
    "/add_video_minute",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
async def add_video_minute(
    video_minute: schemas.VideoMinuteCreate,
):
    try:
        time_start = time.time()
        result = await crud.add_video_minute(video_minute)
        time_end = time.time()
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post(
    "/add_video_minute_bulk",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
async def add_video_minute_bulk(
    data: List[schemas.VideoMinuteCreate],
):
    try:
        time_start = time.time()
        result = await crud.add_video_minute_bulk(data)
        time_end = time.time()
        print(f"Time: {time_end - time_start}")
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
