from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from models import JobBoard, JobPost

engine = create_engine(str(settings.DATABASE_URL), echo=True)
def get_db_session():
    return sessionmaker(bind=engine)()
app = FastAPI()

@app.get("/health")
async def health_check():
    try:
        with get_db_session() as connection:
            connection.execute(text("SELECT 1")) 
            return "Database Connection successful!"
    except Exception as e:
        return "Database connection has error"
    
@app.get("/api/jobboards")
async def api_job_boards():
    with get_db_session() as session:
        jobBoards = session.query(JobBoard).all()
        return jobBoards
    
@app.get("/api/jobPost")
async def api_job_posts():
    with get_db_session() as session:
        jobPost = session.query(JobPost).all()
        return jobPost
    
@app.get("/api/job-boards/{job_id}/job-posts")
async def get_jobs(job_id: int):
    with get_db_session() as session:
        getJobs = session.query(JobPost).filter(JobPost.job_board_id == job_id).all()
        return getJobs
    
@app.get("/api/job-boards/{slug}")
async def api_company_job_board(slug):
  with get_db_session() as session:
     jobPosts = session.query(JobPost) \
        .join(JobPost.job_board) \
        .filter(JobBoard.slug.__eq__(slug)) \
        .all()
     return jobPosts