from sqlalchemy import select
from datetime import date
from . import models, schemas
from typing import List, Union
from .database import SessionLocal
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


# Get by aid
async def get_video_static(aid: int) -> models.VideoStatic:
    """Get static information for a video by AV ID."""
    async with SessionLocal() as db:
        query = select(models.VideoStatic).where(models.VideoStatic.aid == aid)
        result = await db.execute(query)
        return result.scalar_one_or_none()


async def get_video_static_bulk(aids: List[int]) -> List[models.VideoStatic]:
    """Get static information for multiple videos by their AV IDs."""
    if not aids:
        return []
    async with SessionLocal() as db:
        query = select(models.VideoStatic).where(models.VideoStatic.aid.in_(aids))
        result = await db.execute(query)
        return result.scalars().all()


# get video static by priority
async def get_video_static_by_priority(priority: int = 0) -> List[models.VideoStatic]:
    """Get static information for a video by AV ID and priority."""
    async with SessionLocal() as db:
        if priority == 0:
            query = select(models.VideoStatic).where(
                models.VideoStatic.priority.isnot(None)
            )
        else:
            query = select(models.VideoStatic).where(
                models.VideoStatic.priority == priority
            )
        result = await db.execute(query)
        return result.scalars().all()


async def get_video_dynamic(
    aid: int, record_date: date = date.today(), record_time: int = 0
):
    """Get dynamic information for a video by AV ID and date."""
    async with SessionLocal() as db:
        if record_time:
            record_date = date.fromtimestamp(record_time)
        query = select(models.VideoDynamic).where(
            models.VideoDynamic.aid == aid,
            models.VideoDynamic.record_date == record_date,
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


async def get_video_minute(aid: int, time: int):
    """Get minute-level statistics for a video."""
    async with SessionLocal() as db:
        if time:
            query = select(models.VideoMinute).where(
                models.VideoMinute.aid == aid, models.VideoMinute.time == time
            )
        else:
            query = select(models.VideoMinute).where(models.VideoMinute.aid == aid)
        result = await db.execute(query)
        return result.scalar()


# Get by other fields
async def get_user(user_id: int):
    """Get user information by user ID."""
    async with SessionLocal() as db:
        query = select(models.DimUser).where(models.DimUser.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()


async def get_type(type_id: int):
    """Get type information by type ID."""
    async with SessionLocal() as db:
        query = select(models.DimType).where(models.DimType.type_id == type_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()


async def get_identifier_map(identifier: str):
    """Get identifier mapping by identifier string."""
    async with SessionLocal() as db:
        query = select(models.IdentifierMap).where(
            models.IdentifierMap.identifier == identifier
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


async def get_video_vocals(aid: int):
    """Get all vocals associated with a video."""
    async with SessionLocal() as db:
        query = select(models.OlapRelVideoVocal).where(
            models.OlapRelVideoVocal.aid == aid
        )
        result = await db.execute(query)
        return result.scalars().all()


# Add


async def add_record(model_cls, data: schemas.BaseModel):
    async with SessionLocal() as db:
        try:
            db_instance = model_cls(
                **data.model_dump()
            )
            db.add(db_instance)
            await db.commit()
            await db.refresh(db_instance)
            return db_instance
        except IntegrityError as e:
            await db.rollback()
            # Re-raise the error to be handled by the caller
            raise e
        except Exception as e:
            await db.rollback()
            logger.error(f"Database error in add_record: {str(e)}")
            raise e


async def add_records(
    model_cls, data_list
):
    async with SessionLocal() as db:
        try:
            db_instances = [
                model_cls(**item.model_dump()) for item in data_list
            ]
            for db_instance in db_instances:
                assert isinstance(db_instance, model_cls)
            db.add_all(db_instances)
            await db.commit()
            for instance in db_instances:
                await db.refresh(instance)
            return db_instances
        except IntegrityError as e:
            await db.rollback()
            # Re-raise the error to be handled by the caller
            raise e
        except Exception as e:
            await db.rollback()
            logger.error(f"Database error in add_records: {str(e)}")
            raise e

async def add_video_static(video: schemas.VideoStaticCreate):
    """Add new video static information."""
    db_instance = await add_record(models.VideoStatic, video)
    return schemas.VideoStatic.model_validate(db_instance)

async def add_video_static_bulk(
    videos: List[schemas.VideoStaticCreate],
):
    """Add new video static information in bulk."""
    db_instances = await add_records(models.VideoStatic, videos)
    return [schemas.VideoStatic.model_validate(instance) for instance in db_instances]


async def add_video_dynamic(dynamic: schemas.VideoDynamicCreate):
    """Add new video dynamic information."""
    db_instance =  await add_record(models.VideoDynamic, dynamic)
    return schemas.VideoDynamic.model_validate(db_instance)


async def add_video_dynamic_bulk(
    dynamics: List[schemas.VideoDynamicCreate],
):
    """Add new video dynamic information in bulk."""
    db_instances = await add_records(models.VideoDynamic, dynamics)
    return [schemas.VideoDynamic.model_validate(instance) for instance in db_instances]


async def add_video_minute(minute: schemas.VideoMinuteCreate):
    """Add new video minute statistics."""
    db_instance = await add_record(models.VideoMinute, minute)
    return schemas.VideoMinute.model_validate(db_instance)


async def add_video_minute_bulk(
    minutes: List[schemas.VideoMinuteCreate],
):
    """Add new video minute statistics in bulk."""
    db_instances = await add_records(models.VideoMinute, minutes)
    return [schemas.VideoMinute.model_validate(instance) for instance in db_instances]