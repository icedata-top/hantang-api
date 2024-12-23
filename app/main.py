from fastapi import FastAPI
import pymysql
from . import crud, schemas
from .schemas import SuccessResponse, ErrorResponse
import time
from typing import List, Union

pymysql.install_as_MySQLdb()

app = FastAPI()


@app.get("/", response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse])
def read_root():
    return {"Ping": "Pong", "time": 0.0, "status": "success"}


@app.get("/get_video_static_by_priority", response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse])
async def get_video_static_by_priority(piority: int = 0):
    try:
        time_start = time.time()
        result: List[schemas.VideoStatic] = await crud.get_video_static_by_priority(
            piority
        )
        time_end = time.time()
        data = {
            "result": result,
            "time": time_end - time_start,
            "status": "success",
        }
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/add_video_minute", response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse])
async def add_video_minute(
    video_minute: schemas.VideoMinuteCreate,
):
    try:
        time_start = time.time()
        result = await crud.add_video_minute(
            video_minute.model_dump()
        )
        time_end = time.time()
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/add_video_minute_bulk", response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse])
async def add_video_minute_bulk(
    data: List[schemas.VideoMinuteCreate],
):
    try:
        time_start = time.time()
        result = await crud.add_video_minute_bulk(
            [item.model_dump() for item in data]
        )
        time_end = time.time()
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
