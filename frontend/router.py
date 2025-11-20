from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List

app = FastAPI()

candidates_data = {
    "john_doe": {
        "name": "John Doe",
        "applied_job_role": "Project Manager",
        "skillsets": ["Leadership", "Agile", "Communication", "Risk Management", "Budgeting"]
    },
    "jane_smith": {
        "name": "Jane Smith",
        "applied_job_role": "Customer Support Executive",
        "skillsets": ["Communication", "Problem Solving", "CRM Software", "Empathy", "Multitasking"]
    },
    "alice_johnson": {
        "name": "Alice Johnson",
        "applied_job_role": "Software Engineer",
        "skillsets": ["Python", "JavaScript", "React", "FastAPI", "SQL", "Git"]
    },
    "bob_williams": {
        "name": "Bob Williams",
        "applied_job_role": "Project Manager",
        "skillsets": ["Project Planning", "Team Management", "Scrum", "JIRA", "Stakeholder Management"]
    },
    "carol_brown": {
        "name": "Carol Brown",
        "applied_job_role": "Data Analyst",
        "skillsets": ["Python", "SQL", "Excel", "Tableau", "Statistics", "Data Visualization"]
    },
    "david_miller": {
        "name": "David Miller",
        "applied_job_role": "Software Engineer",
        "skillsets": ["Java", "Spring Boot", "Microservices", "Docker", "Kubernetes", "AWS"]
    }
}

@app.get("/candidates")
def get_all_candidates():
    """Get all candidates"""
    return candidates_data


@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    """Get a specific candidate by ID"""
    if candidate_id not in candidates_data:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidates_data[candidate_id]


@app.get("/search/by-role")
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


@app.get("/search/by-skill")
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


@app.get("/search/by-skills")
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


@app.get("/search/by-role-and-skill")
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