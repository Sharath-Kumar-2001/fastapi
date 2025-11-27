from fastapi import FastAPI, APIRouter, File, Form, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from auth import authenticate_admin
from config import settings
from file_storage import encrypt_filename, upload_file, UPLOAD_DIR
from models import JobBoard, JobPost
from typing import Annotated, Optional
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

# if not settings.PRODUCTION:
app.mount("/uploads", StaticFiles(directory="uploads/company-logos"))

class JobBoardResponse(BaseModel):
    id: int
    slug: str
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True

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
    
@router.get("/job-posts/{slug}")
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

@router.get("/job-boards/{job_id}", response_model= JobBoardResponse)
async def getById(job_id: int):
    try:
        with get_db_session() as session:
            getJobId = session.get(JobBoard, job_id)
            return JobBoardResponse.from_orm(getJobId)
    except Exception as e:
        raise HTTPException(status_code=404, detail= "Job Not found")


@router.post("/job-boards/new", response_model=JobBoardResponse)
async def create_job_board_with_upload(
    slug: str = Form(...),
    logo: UploadFile = File(...)
):
    """
    Create a new job board with logo file upload.
    Accepts multipart/form-data with slug and logo file.
    Filename is encrypted before storage.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"]
    if logo.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Encrypt the filename
    encrypted_filename = encrypt_filename(logo.filename)
    # file_path = f"/{encrypted_filename}"
    
    # Read file contents
    try:
        contents = await logo.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")
    finally:
        await logo.close()
    
    # Upload file using your function
    try:
        logo_url = upload_file(
            bucket_name="company-logos",
            path=encrypted_filename,
            contents=contents,
            content_type=logo.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
    
    # Save to database
    with get_db_session() as session:
        # Check if slug already exists
        existing = session.query(JobBoard).filter(JobBoard.slug == slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists")
        
        # Create new job board
        new_job_board = JobBoard(
            slug=slug,
            logo_url=logo_url
        )
        session.add(new_job_board)
        session.flush()
        session.refresh(new_job_board)
        session.commit()
        return JobBoardResponse.from_orm(new_job_board)

@router.put("/job-boards/{job_board_id}/update")
async def update_job_board(job_board_id: int, new_logo_file: UploadFile = File(...)):
    try:
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"]
        if new_logo_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
            )
        
        # Encrypt the filename
        encrypted_filename = encrypt_filename(new_logo_file.filename)
        try:
            contents = await new_logo_file.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")
        finally:
            await new_logo_file.close()
        try:
            newLogoUrl = upload_file(
                bucket_name="company-logos",
                path=encrypted_filename,
                contents=contents,
                content_type=new_logo_file.content_type
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
        with get_db_session() as session:
            job_board = session.query(JobBoard).filter(JobBoard.id == job_board_id).first()
            if not job_board:
                raise HTTPException(status_code=404, detail="Job board not found")
            updateJobBoard = session.query(JobBoard). filter(JobBoard.id == job_board_id).update({JobBoard.logo_url: newLogoUrl})
            session.commit()
            if not updateJobBoard:
                raise HTTPException(status_code=500, detail="Error updating the logo url.")
            return "Job Board Updated successfully."
    except Exception as e:
        raise HTTPException(status_code=200, detail= f"No Job Board found  {e}")

@router.delete("/job-boards/{job_id}/delete")
async def delete_job_board(job_id: int):
    try:
        with get_db_session() as session:
            job_board = session.query(JobBoard).filter(JobBoard.id == job_id).first()
            if not job_board:
                raise HTTPException(status_code=404, detail="Job board not found")
            delete_job_board = session.delete(job_board)
            session.commit()
    except:
        raise HTTPException(status_code=500, detail="Database connection error.")
    
class AdminLoginForm(BaseModel):
   username : str
   password : str

@router.post("/admin-login")
async def admin_login(response: Response, admin_login_form: Annotated[AdminLoginForm, Form()]):
   auth_response = authenticate_admin(admin_login_form.username, admin_login_form.password)
   if auth_response is not None:
      secure = settings.PRODUCTION
      cookie_value = response.set_cookie(key="admin_session", value=auth_response, httponly=True, secure=secure, samesite="Lax")
      return {"message": "Come to the dark side, we have cookies"}
   else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.post

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
