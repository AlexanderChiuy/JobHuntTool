from services.job import job_url_service
from fastapi import APIRouter, HTTPException, Depends, Request
from config.keys import PERPLEXITY_API_KEY
from models.email_summary import GPT_Email_Summary_Response, Status
from services.summary import email_summary_service
from services.job import job_status_service
from config.logger import logger
from services.email import email_service
from auth.verification import verify_google_token

# set up logger 
router = APIRouter() 

@router.get("/email-summary")
async def get_summary_email(req: Request, auth_data: dict = Depends(verify_google_token)):
    body = await req.json()
    email = body.get("email")
    return await email_summary_service.email_summary(email)


@router.post("/company-job-info-crew-ai")
async def get_company_job_info(req: Request, auth_data: dict = Depends(verify_google_token)):
    logger.info("INFO CREW AI CALLED")
    body = await req.json()
    email_id = body.get("email_id")
    authorization = req.headers.get("authorization")
    # Step 1: Get email content
    email_response = await email_service.get_email(authorization, email_id)
    user_id = email_response['payload']['headers'][0]['value']
    summary_json: GPT_Email_Summary_Response = await email_service.get_email_summary(email_response)

    # Get resume summary
    
    # Step 2: Process job application based on status using match-case
    match(summary_json.status): 
        case Status.IN_REVIEW | Status.INTERVIEWING:
            await job_status_service.handle_in_review_or_interview(summary_json,user_id, authorization)
            return {"message": "Job info successfully updated"}

        case Status.OFFER | Status.REJECTED:
            msg = await job_status_service.handle_offer_or_rejection(summary_json, user_id, authorization)
            return {"message": msg}
        case _:
            raise HTTPException(status_code=500, detail="Response validation failed")
        
@router.post("/company-job-url-crew-ai")
async def get_company_job_url(req: Request, auth_data: dict = Depends(verify_google_token)):
    logger.info("INFO CREW AI CALLED")
    body = await req.json()
    job_post_url = body.get("job_post_url")
    user_id = auth_data.get("email")
    scraped_response = job_url_service.get_job_link_info(job_post_url)
    # Use job posting content as the "email"
    summary_json: GPT_Email_Summary_Response = await email_summary_service.email_summary(scraped_response)

    # Assume the user is in the Interviewing phase
    await job_status_service.handle_in_review_or_interview(summary_json, user_id, req.headers.get("authorization"))
    return {"message": "Job info successfully updated"}
