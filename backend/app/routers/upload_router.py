# upload_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from services.interview.insert_resume import insert_resume
from services.interview.resume_parser import extract_resume_text
from utils.text_cleaner import clean_resume_text
from auth.verification import verify_google_token

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
    auth_data: dict = Depends(verify_google_token)
):
    userId = auth_data.get("email")
    allowed_extensions = {"pdf", "doc", "docx"}
    filename = resume.filename
    extension = filename.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, DOC, or DOCX file."
        )

    content = await resume.read()
    resume_text = extract_resume_text(content, extension)
    cleaned_resume_text = clean_resume_text(resume_text)
    await insert_resume(filename, cleaned_resume_text, userId)
