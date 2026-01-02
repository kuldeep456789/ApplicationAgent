"""
FastAPI Backend - Main Application
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from loguru import logger
import sys

from backend.config import settings
from backend.models.database import init_db, get_db, Job, Application, UserProfile
from backend.modules.scraper import JobScraperService
from backend.modules.llm_engine import LLMEngine, JobMatcher
from backend.modules.form_filler import ApplicationAutomator
from pydantic import BaseModel, Field
from datetime import datetime

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level=settings.log_level
)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Job Application Assistant API")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Job Application Assistant API")

# Create FastAPI app
app = FastAPI(
    title="Job Application Assistant API",
    description="AI-powered job search and application automation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class JobSearchRequest(BaseModel):
    keywords: str = Field(..., description="Job search keywords")
    location: str = Field(default="", description="Job location")
    platforms: Optional[List[str]] = Field(default=None, description="Platforms to search")
    max_results_per_platform: int = Field(default=50, description="Max results per platform")

class JobAnalysisRequest(BaseModel):
    job_id: str = Field(..., description="Job ID to analyze")

class CoverLetterRequest(BaseModel):
    job_id: str = Field(..., description="Job ID")
    tone: str = Field(default="professional", description="Cover letter tone")

class ApplicationRequest(BaseModel):
    job_id: str = Field(..., description="Job ID to apply to")
    auto_submit: bool = Field(default=False, description="Auto-submit application")

class UserProfileCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    skills: List[str]
    experience_years: Optional[int] = None
    education: Optional[dict] = None
    resume_path: Optional[str] = None
    preferences: Optional[dict] = None

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Job Application Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/jobs/search")
async def search_jobs(
    request: JobSearchRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Searching jobs: {request.keywords} in {request.location}")
        
        scraper_service = JobScraperService()
        jobs = await scraper_service.search_all_platforms(
            keywords=request.keywords,
            location=request.location,
            platforms=request.platforms,
            max_results_per_platform=request.max_results_per_platform
        )
        
        background_tasks.add_task(save_jobs_to_db, jobs, db)
        
        return {
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jobs")
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(Job)
        if source:
            query = query.where(Job.source == source)
        query = query.offset(skip).limit(limit).order_by(Job.scraped_at.desc())
        result = await db.execute(query)
        jobs = result.scalars().all()
        return {
            "success": True,
            "count": len(jobs),
            "jobs": [job.__dict__ for job in jobs]
        }
    except Exception as e:
        logger.error(f"Error getting jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/jobs/analyze")
async def analyze_job(
    request: JobAnalysisRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Job).where(Job.job_id == request.job_id)
        )
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        result = await db.execute(select(UserProfile).limit(1))
        user_profile = result.scalar_one_or_none()
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        llm = LLMEngine()
        analysis = await llm.analyze_job(
            job=job.__dict__,
            user_profile=user_profile.__dict__
        )
        job.match_score = analysis.get('match_score', 0.0)
        await db.commit()
        return {
            "success": True,
            "job_id": request.job_id,
            "analysis": analysis
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cover-letter/generate")
async def generate_cover_letter_endpoint(
    request: CoverLetterRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Job).where(Job.job_id == request.job_id)
        )
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        result = await db.execute(select(UserProfile).limit(1))
        user_profile = result.scalar_one_or_none()
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        llm = LLMEngine()
        cover_letter = await llm.generate_cover_letter(
            job=job.__dict__,
            user_profile=user_profile.__dict__,
            tone=request.tone
        )
        return {
            "success": True,
            "job_id": request.job_id,
            "cover_letter": cover_letter
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating cover letter: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/applications/submit")
async def submit_application(
    request: ApplicationRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Job).where(Job.job_id == request.job_id)
        )
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        result = await db.execute(select(UserProfile).limit(1))
        user_profile = result.scalar_one_or_none()
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        llm = LLMEngine()
        cover_letter = await llm.generate_cover_letter(
            job=job.__dict__,
            user_profile=user_profile.__dict__
        )
        application = Application(
            job_id=request.job_id,
            status="pending",
            cover_letter=cover_letter,
            resume_version=user_profile.resume_path
        )
        db.add(application)
        job.is_applied = True
        await db.commit()
        return {
            "success": True,
            "job_id": request.job_id,
            "message": "Application submitted successfully",
            "application_id": application.id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications")
async def get_applications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(Application)
        if status:
            query = query.where(Application.status == status)
        query = query.offset(skip).limit(limit).order_by(Application.applied_at.desc())
        result = await db.execute(query)
        applications = result.scalars().all()
        return {
            "success": True,
            "count": len(applications),
            "applications": [app.__dict__ for app in applications]
        }
    except Exception as e:
        logger.error(f"Error getting applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/profile")
async def create_profile(
    profile: UserProfileCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(UserProfile).where(UserProfile.email == profile.email)
        )
        existing_profile = result.scalar_one_or_none()
        if existing_profile:
            for key, value in profile.model_dump().items():
                setattr(existing_profile, key, value)
            existing_profile.updated_at = datetime.utcnow()
            await db.commit()
            return {
                "success": True,
                "message": "Profile updated",
                "profile_id": existing_profile.id
            }
        else:
            new_profile = UserProfile(**profile.model_dump())
            db.add(new_profile)
            await db.commit()
            return {
                "success": True,
                "message": "Profile created",
                "profile_id": new_profile.id
            }
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profile")
async def get_profile(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(UserProfile).limit(1))
        profile = result.scalar_one_or_none()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {
            "success": True,
            "profile": profile.__dict__
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def save_jobs_to_db(jobs: List[dict], db: AsyncSession):
    try:
        for job_data in jobs:
            result = await db.execute(
                select(Job).where(Job.job_id == job_data.get('job_id'))
            )
            existing_job = result.scalar_one_or_none()
            if not existing_job:
                job = Job(**job_data)
                db.add(job)
        await db.commit()
        logger.info(f"Saved {len(jobs)} jobs to database")
    except Exception as e:
        logger.error(f"Error saving jobs to database: {e}")
        await db.rollback()

if __name__ == "__main__":
    import uvicorn
    import os
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"Starting uvicorn from root: {project_root}")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        app_dir=project_root
    )
