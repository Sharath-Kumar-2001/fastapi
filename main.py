from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
app = FastAPI()
router = APIRouter()

@app.get("/health")
async def health():
  return {"status": "ok"}

job_boards = {
  "acme": {
        "jobs":{
          "title-1": "Customer Support Executive", 
          "title-2": "Project Manager"
          }, 
        "Job Description": {
          "title1": "summa", 
          "title2": "summa"
          }
      },
    "bcg": {
        "jobs":{
          "title-1": "Customer Support Executive", 
          "title-2": "Project Manager"
          }, 
        "Job Description": {
          "title1": "summa", 
          "title2": "summa"
          }
      },
    "atlas": {
        "jobs":{
          "title-1": "Customer Support Executive", 
          "title-2": "Project Manager"
          }, 
        "Job Description": {
          "title1": "summa", 
          "title2": "summa"
          }
      }
}

@router.get("/list_jobs/{company_name}/", tags=["job_portal"])
async def list_jobs(company_name: str):
  try:
    return job_boards[company_name]
  except Exception as e:
    raise HTTPException(status_code=404, detail=f"The company name {company_name} is not found")
  
@router.get("/search_job_title/{company_name}", tags=["search_jobs"])
async def search_jobs(company_name: str, query: str):
  try:
    pass
  except Exception as e:
    raise HTTPException(status_code=404, detail=f"The requested job is not found")

@router.get("/list_company", tags=["search_jobs"])
async def list_jobs():
  try:
    return {"company_names": list(job_boards.keys())}
  except Exception as e:
    raise HTTPException(status_code=404, detail=f"The requested job is not found") 

app.include_router(router, prefix="/job-boards")
app.mount("/public", StaticFiles(directory="public"), name="staic")