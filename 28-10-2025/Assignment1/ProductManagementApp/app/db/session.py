import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL not set in environment (.env)')

# Async engine using asyncpg driver
async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, future=True)

Base = declarative_base()

# Dependency for routes
async def get_session():
    async with async_session() as session:
        yield session
