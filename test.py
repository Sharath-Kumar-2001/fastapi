from fastapi import FastAPI, APIRouter, Request, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List
app = FastAPI()
router = APIRouter()
candidate = APIRouter()
templates = Jinja2Templates(directory="public")
app.mount("/public", StaticFiles(directory="frontend/dist"), name="public")

@router.get("/html")
async def get_image():
    return FileResponse("public/index.html")

data = {
    "acme": {
        "jobs": {"Customer Support Executive": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.","Project Manager"
        : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
    },
    "bcg": {
        "jobs": {"Customer Support Executive": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.","Project Manager"
        : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
    },
    "atlas": {
        "jobs": {"Customer Support Executive": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.","Project Manager"
        : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
    }
}

@router.get("/jobs/{company}", response_class=HTMLResponse)
async def get_jobs(request: Request, company: str | None = None):
    """
    /jobs              -> all companies
    /jobs?company=acme -> only acme
    """

    company_key = company.lower()
    if company_key not in data:
        raise HTTPException(status_code=404, detail="Company not found")

    company_data = data[company_key]

    # Find job by its TITLE value (case-insensitive match)
    jobs = company_data["jobs"]
    print(company_data)
    matched_job_key = None
    # for key, title in jobs.items():
    #     if title.lower() == job_title.lower():
    #         matched_job_key = key
    #         break

    # if not matched_job_key:
    #     raise HTTPException(status_code=404, detail="Job title not found")

    # OPTIONAL: map "title-1" -> "title1" to get description
    # num = "".join(ch for ch in matched_job_key if ch.isdigit())  # '1' or '2'
    # desc_key = f"title{num}"
    # job_description = company_data["Job Description"].get(desc_key, "No description available")
    return data[company]
    # return templates.TemplateResponse(
    #     "jobs.html",
    #     {
    #         "request": request,
    #         "company_name": company_key,
    #         # "job_title": job_title,
    #         # "job_description": job_description,
    #     },
    # )

# @router.get("/data/{company}")
# async def data_value(company:str):
#     answer = {}
#     for key, value in data[company]["jobs"].items():
#         answer["title"] = key
#         answer["jobDescription"] = value
#     return answer

@router.get("/data/{company}")
async def data_value(company: str):
    if company not in data:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return [
        {"title": key, "jobDescription": value}
        for key, value in data[company]["jobs"].items()
    ]

@router.get("/data/{company}/{title}")
async def job_role(company:str, title:str):
    if company.lower() not in data:
         return HTTPException(status_code=404, detail="The company is not available")
    for job_title, job_desc in data[company]["jobs"].items():
        if title.lower() == job_title.lower():
            return {
                "job title": job_title,
                "job Description": job_desc
            }
        else:
            return HTTPException(status_code=404, detail="The job title is not available")

candidates_data = {
    "PM001": {
        "name": "John Doe",
        "applied_job_role": "Project Manager",
        "skillsets": ["Leadership", "Agile", "Communication", "Risk Management", "Budgeting"]
    },
    "CSE001": {
        "name": "Jane Smith",
        "applied_job_role": "Customer Support Executive",
        "skillsets": ["Communication", "Problem Solving", "CRM Software", "Empathy", "Multitasking"]
    },
    "SE001": {
        "name": "Alice Johnson",
        "applied_job_role": "Software Engineer",
        "skillsets": ["Python", "JavaScript", "React", "FastAPI", "SQL", "Git"]
    },
    "PM002": {
        "name": "Bob Williams",
        "applied_job_role": "Project Manager",
        "skillsets": ["Project Planning", "Team Management", "Scrum", "JIRA", "Stakeholder Management"]
    },
    "DA001": {
        "name": "Carol Brown",
        "applied_job_role": "Data Analyst",
        "skillsets": ["Python", "SQL", "Excel", "Tableau", "Statistics", "Data Visualization"]
    },
    "SE002": {
        "name": "David Miller",
        "applied_job_role": "Software Engineer",
        "skillsets": ["Java", "Spring Boot", "Microservices", "Docker", "Kubernetes", "AWS"]
    }
}


@candidate.get("/candidates")
def get_all_candidates():
    """Get all candidates"""
    return candidates_data


@candidate.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    """Get a specific candidate by ID"""
    if candidate_id not in candidates_data:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidates_data[candidate_id]


@candidate.get("/search/by-role")
def search_by_role(role: str):
    """Search candidates by job role (case-insensitive)"""
    role_lower = role.lower()
    
    matching_candidates = {
        candidate_id: candidate_info
        for candidate_id, candidate_info in candidates_data.items()
        if candidate_info["applied_job_role"].lower() == role_lower
    }
    
    if not matching_candidates:
        raise HTTPException(status_code=404, detail=f"No candidates found for role: {role}")
    
    return {"role": role, "count": len(matching_candidates), "candidates": matching_candidates}


@candidate.get("/search/by-skill")
def search_by_skill(skill: str):
    """Search candidates by a specific skill (case-insensitive)"""
    skill_lower = skill.lower()
    
    matching_candidates = {
        candidate_id: candidate_info
        for candidate_id, candidate_info in candidates_data.items()
        if any(s.lower() == skill_lower for s in candidate_info["skillsets"])
    }
    
    if not matching_candidates:
        raise HTTPException(status_code=404, detail=f"No candidates found with skill: {skill}")
    
    return {"skill": skill, "count": len(matching_candidates), "candidates": matching_candidates}


@candidate.get("/search/by-skills")
def search_by_multiple_skills(skills: List[str] = Query(...)):
    """Search candidates who have ALL specified skills (case-insensitive)"""
    skills_lower = [skill.lower() for skill in skills]
    
    matching_candidates = {}
    for candidate_id, candidate_info in candidates_data.items():
        candidate_skills_lower = [s.lower() for s in candidate_info["skillsets"]]
        # Check if candidate has all required skills
        if all(skill in candidate_skills_lower for skill in skills_lower):
            matching_candidates[candidate_id] = candidate_info
    
    if not matching_candidates:
        raise HTTPException(status_code=404, detail=f"No candidates found with all skills: {', '.join(skills)}")
    
    return {"skills": skills, "count": len(matching_candidates), "candidates": matching_candidates}


@candidate.get("/search/by-role-and-skill")
def search_by_role_and_skill(role: str, skill: str):
    """Search candidates by both job role and skill (case-insensitive)"""
    role_lower = role.lower()
    skill_lower = skill.lower()
    
    matching_candidates = {
        candidate_id: candidate_info
        for candidate_id, candidate_info in candidates_data.items()
        if candidate_info["applied_job_role"].lower() == role_lower
        and any(s.lower() == skill_lower for s in candidate_info["skillsets"])
    }
    
    if not matching_candidates:
        raise HTTPException(
            status_code=404, 
            detail=f"No candidates found for role '{role}' with skill '{skill}'"
        )
    
    return {
        "role": role,
        "skill": skill,
        "count": len(matching_candidates),
        "candidates": matching_candidates
    }

app.include_router(router=candidate, prefix="/candidates")

app.include_router(router=router, prefix="/api")



