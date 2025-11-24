from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from models import JobBoard, JobPost
import os

engine = create_engine(str(settings.DATABASE_URL), echo=True)
def get_db_session():
    return sessionmaker(bind=engine)()

app = FastAPI()
router = APIRouter()

app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))

@router.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")

@router.get("/health")
async def health_check():
    try:
        with get_db_session() as connection:
            connection.execute(text("SELECT 1")) 
            return "Database Connection successful!"
    except Exception as e:
        return "Database connection has error"
    
@router.get("/jobboards")
async def api_job_boards():
    with get_db_session() as session:
        jobBoards = session.query(JobBoard).all()
        return jobBoards
    
@router.get("/jobPost")
async def api_job_posts():
    with get_db_session() as session:
        jobPost = session.query(JobPost).all()
        return jobPost
    
@router.get("/job-boards/{job_id}/job-posts")
async def get_jobs(job_id: int):
    with get_db_session() as session:
        getJobs = session.query(JobPost).filter(JobPost.job_board_id == job_id).all()
        return getJobs
    
@router.get("/job-boards/{slug}")
async def api_company_job_board(slug):
  with get_db_session() as session:
     jobPosts = session.query(JobPost) \
        .join(JobPost.job_board) \
        .filter(JobBoard.slug.__eq__(slug)) \
        .all()
     return jobPosts
  
app.include_router(router=router, prefix="/api")