from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, Float, Boolean, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.config import settings
class Base(DeclarativeBase):
    pass
class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    company: Mapped[str] = mapped_column(String(255))
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    salary_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    job_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(100))  
    url: Mapped[str] = mapped_column(Text)
    posted_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(50))  
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cover_letter: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resume_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    response_received: Mapped[bool] = mapped_column(Boolean, default=False)
    response_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
class UserProfile(Base):
    __tablename__ = "user_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    skills: Mapped[list] = mapped_column(JSON)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    education: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    resume_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
