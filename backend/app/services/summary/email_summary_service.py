from services.clients.openai_client import *
from config.keys import *
from models.email_summary import *
import json
from schemas.email_schema import email_schema
from utils.helpers import string_to_json

async def email_summary(email:str) -> GPT_Email_Summary_Response:

    query  = f"""
            Provide a summary of the email and also extract the job and company from the email. 
             
             The email/job description content is provided here: {email}. 
             
             Make sure to ensure if the email/job description is referencing a job application or a job offer or  a job rejection
                or a job unrelated topic outside jobs.

                If the email/job description is related to a job application, make sure to extract the company name, job position, and status of the email/job description, do not make as UNRELATED.
             UNRELATED means that the email/job description does not reference a job description, job application, job offer, or job rejection.
             Return a JSON schema with the following keys: 

             {{
             
                "company": **insert company name here**,
                "job_position": **insert job position here**, # if not specified, return "N/A"
                "summary": **insert summary here**
                "status": **insert Enum One of: InReview, Interviewing, Offer, Rejected, Unrelated**

            }}
            """
    messages = [
        {
            "role": "system", 
            "content": "You are an assistant. summarizing an email and prepare a prompt for prepxilty to scrape the web for more information", 
        },
        {
            "role": "user", 
            "content":query
        }
        
    ]
   
    chat_client = GPTChatCompletionClient(base_url=ENDPOINT_OPENAI_GPT4, 
                                          api=OPENAI_GPT4_KEY,
                                          api_version=CHAT_VERSION,
                                          deployment_name=CHAT_DEPLOYMENT_NAME)
    response_format = {
            "type": "json_schema",
        "json_schema": {"name": "email_schema", "schema": GPT_Email_Summary_Response.model_json_schema()}
    }
    
    chat_response = await chat_client.call_async(
                            messages=messages, 
                            response_format=response_format, 
                            temperature=0.0,
                            max_tokens=1000,
                    )
    msgs = chat_client.parse_response(chat_response)
    try: 
        # msg  =  string_to_json(msgs[-1])
        response = json.loads(msgs[-1])
        logger.info("EMAIL SUMMARY RESPONSE", response)
    except Exception as e:
        logger.error("ERROR RESPONSE", e)
        raise SyntaxError("Response validation failed")
    
    try :
        response_format = GPT_Email_Summary_Response(**response)
    except Exception as e:
        logger.error("ERROR RESPONSE", e)
        raise SyntaxError("Response validation failed")
    
    return response_format
