from pydantic import BaseModel
from typing import Optional


class ResumeInfo(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    job_intention: Optional[str] = None
    expected_salary: Optional[str] = None
    work_years: Optional[str] = None
    education: Optional[str] = None
    project_experience: Optional[str] = None


class MatchResult(BaseModel):
    match_score: float
    skill_match_rate: float
    experience_relevance: float
    analysis: str


class ResumeResponse(BaseModel):
    resume_id: str
    raw_text: str
    info: ResumeInfo
    match_result: Optional[MatchResult] = None


class JobDescription(BaseModel):
    description: str
