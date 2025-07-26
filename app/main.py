from fastapi import FastAPI, HTTPException
import pymysql
from . import crud, schemas
import time
from typing import List, Union
from .biliapi import getSingleVideoInfo
from sqlalchemy.exc import IntegrityError
import logging

pymysql.install_as_MySQLdb()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    time_start = time.time()
    try:
        video_data = getSingleVideoInfo(avid, bv)
        
        # Convert dict to Pydantic model
        if priority:
            video_data["priority"] = priority
        video_create = schemas.VideoStaticCreate(**video_data)
        
        result = await crud.add_video_static(video_create)
        time_end = time.time()
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except IntegrityError as e:
        # Handle duplicate key errors - treat as success
        error_msg = str(e.orig).lower()
        if "duplicate entry" in error_msg or "duplicate key" in error_msg:
            logger.info(f"Duplicate entry for video {avid}/{bv}, treating as success")
            time_end = time.time()
            return {"result": "Video already exists", "time": time_end - time_start, "status": "success"}
        else:
            # Other integrity errors (foreign key violations, etc.)
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        # Handle permission errors
        if "command denied" in error_msg or "access denied" in error_msg:
            logger.error(f"Database permission error: {str(e)}")
            raise HTTPException(status_code=403, detail="Database permission error: insufficient privileges")
        # Handle other database errors
        elif "operational error" in error_msg or "database" in error_msg:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database operation failed")
        else:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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
        logger.error(f"Error getting video static by priority: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post(
    "/add_video_minute",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
async def add_video_minute(
    video_minute: schemas.VideoMinuteCreate,
):
    time_start = time.time()
    try:
        result = await crud.add_video_minute(video_minute)
        time_end = time.time()
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except IntegrityError as e:
        # Handle duplicate key errors - treat as success for minute data too
        error_msg = str(e.orig).lower()
        if "duplicate entry" in error_msg or "duplicate key" in error_msg:
            logger.info("Duplicate entry for video minute data, treating as success")
            time_end = time.time()
            return {"result": "Video minute data already exists", "time": time_end - time_start, "status": "success"}
        else:
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        if "command denied" in error_msg or "access denied" in error_msg:
            logger.error(f"Database permission error: {str(e)}")
            raise HTTPException(status_code=403, detail="Database permission error: insufficient privileges")
        elif "operational error" in error_msg or "database" in error_msg:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database operation failed")
        else:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post(
    "/add_video_minute_bulk",
    response_model=Union[schemas.SuccessResponse, schemas.ErrorResponse],
)
async def add_video_minute_bulk(
    data: List[schemas.VideoMinuteCreate],
):
    time_start = time.time()
    try:
        result = await crud.add_video_minute_bulk(data)
        time_end = time.time()
        print(f"Time: {time_end - time_start}")
        return {"result": result, "time": time_end - time_start, "status": "success"}
    except IntegrityError as e:
        error_msg = str(e.orig).lower()
        if "duplicate entry" in error_msg or "duplicate key" in error_msg:
            logger.info("Some duplicate entries in bulk video minute data, treating as partial success")
            time_end = time.time()
            return {"result": "Bulk operation completed with some duplicates", "time": time_end - time_start, "status": "success"}
        else:
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        if "command denied" in error_msg or "access denied" in error_msg:
            logger.error(f"Database permission error: {str(e)}")
            raise HTTPException(status_code=403, detail="Database permission error: insufficient privileges")
        elif "operational error" in error_msg or "database" in error_msg:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database operation failed")
        else:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
