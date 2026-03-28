from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()

PG_SCHEMA = os.getenv("PG_SCHEMA", "public")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}"
    f"/{os.getenv('PG_DATABASE')}"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"server_settings": {"search_path": PG_SCHEMA}},
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()
