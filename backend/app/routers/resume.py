import os
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import ResumeResponse, MatchResult, JobDescription, ResumeInfo
from app.services.pdf_parser import extract_text_from_pdf
from app.services.ai_service import extract_resume_info, match_resume_to_job
from app.services.cache_service import get_cached, set_cached
from app.config import UPLOAD_DIR, MAX_FILE_SIZE

router = APIRouter(prefix="/api", tags=["resume"])

_resume_store: dict = {}


@router.on_event("startup")
async def startup():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "仅支持PDF格式文件")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "文件大小超过10MB限制")

    resume_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{resume_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(content)

    raw_text = await asyncio.to_thread(extract_text_from_pdf, file_path)
    if not raw_text.strip():
        raise HTTPException(400, "无法从PDF中提取文本内容")

    cached = get_cached("info", raw_text)
    if cached:
        info = cached
    else:
        info = await asyncio.to_thread(extract_resume_info, raw_text)
        set_cached("info", raw_text, info)

    result = ResumeResponse(
        resume_id=resume_id,
        raw_text=raw_text,
        info=ResumeInfo(**info),
    )
    _resume_store[resume_id] = {"info": info, "text": raw_text}
    set_cached("resume", resume_id, {"info": info, "text": raw_text})
    return result


@router.post("/match/{resume_id}", response_model=MatchResult)
async def match_resume(resume_id: str, job: JobDescription):
    stored = _resume_store.get(resume_id)
    if not stored:
        # 尝试从缓存恢复
        cached_data = get_cached("resume", resume_id)
        if cached_data:
            stored = cached_data
        else:
            raise HTTPException(404, "简历不存在，请先上传")

    cache_key = f"{resume_id}:{job.description}"
    cached = get_cached("match", cache_key)
    if cached:
        return MatchResult(**cached)

    result = await asyncio.to_thread(match_resume_to_job, stored["info"], stored["text"], job.description)
    set_cached("match", cache_key, result)
    return MatchResult(**result)


@router.get("/resumes")
async def list_resumes():
    return [{"resume_id": rid, "info": data["info"]} for rid, data in _resume_store.items()]
