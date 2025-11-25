from fastapi import FastAPI, APIRouter, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from file_storage import upload_file, UPLOAD_DIR
from models import JobBoard, JobPost
from typing import Annotated
import os

engine = create_engine(str(settings.DATABASE_URL), echo=True)
def get_db_session():
    return sessionmaker(bind=engine)()

tags_metadata = [
    {
        "name" : "POST API's",
        "description": "Learning how the post api is creation."
    },
    {
        "name": "Calculator",
        "description": "Addition & Multiplication only done now"
    }
]

app = FastAPI(docs_url="/sharath", openapi_tags=tags_metadata)
router = APIRouter()

app.mount("/assets", StaticFiles(directory="frontend-router-concept/build/client/assets"))

if not settings.PRODUCTION:
    app.mount("/uploads", StaticFiles(directory="uploads"))

@router.get("/health")
async def health_check():
    try:
        with get_db_session() as connection:
            connection.execute(text("SELECT 1")) 
            return "Database Connection successful!"
    except Exception as e:
        return "Database connection has error"
    
@router.get("/job-boards")
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

class JobBoardForm(BaseModel):
    slug: str = Field(..., min_length=3, max_digits=20)
    logo: UploadFile = File(...)


@router.post('/job-boards',tags=["POST API's"])
async def api_create_new_job_board(
    slug: Annotated[str, Form(min_length=3, max_length=20)],
    logo: Annotated[UploadFile, File()]
):
    logo_contents = await logo.read()
    file_store = upload_file(
        bucket_name="company-logos",
        path=logo.filename,
        contents=logo_contents,
        content_type=logo.content_type
    )
    return {"slug": slug, "fileurl": file_store}

@router.post('/Addition',tags=['Calculator'])
async def calculator(x: Annotated[int, Form()], y: Annotated[int, Form()]):
    return {"Addition": x+y}

class Multiply(BaseModel):
    x:int = Field(..., min_length=1, max_digits=3)
    y: int = Field(..., min_length=1, max_digits=3)
    logo: UploadFile = File(...)

@router.post('/multiply',tags=['Calculator'])
async def Multiply(mul: Multiply):
    return {"Multiply": mul.x+mul.y, "filename": mul.logo.filename}

app.include_router(router=router, prefix="/api")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend-router-concept", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
