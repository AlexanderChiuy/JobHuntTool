from fastapi import APIRouter, HTTPException
from openai import OpenAI
from services.perplexity_client import PerplexityClient 
from services.openai_client import GPTChatCompletionClient, GPTCompletionClient, InMemoryResponseManager
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
import os
import json
from typing import Dict, List
import re 

router = APIRouter()
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")
OPENAI_GPT4_KEY = os.getenv("AZURE_OPENAI_KEY_GPT_4")
ENDPOINT_OPENAI_GPT4 = os.getenv("GPT4_ENDPOINT")

CHAT_VERSION = "2024-08-01-preview"  # Update if needed
CHAT_DEPLOYMENT_NAME = "gpt-4o"  # Replace with your deployed model name

"""
perplexity_client = PerplexityClient(
    api_key=PERPLEXITY_API_KEY,
    api_url=PERPLEXITY_API_URL,
    model="sonar"
)
"""
print(PERPLEXITY_API_URL)
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

class Email_Summary_Request(BaseModel):
    content: str

@router.post("/email-summary")
async def get_summary_email(packet: Email_Summary_Request):
    messages = [
            {
                "role": "system", 
                "content": "You are an assistant. summarizing an email and prepare a prompt for prepxilty to scrape the web for more information", 
            },
            {
                "role": "user", 
                "content": f"The email content is provided here: {packet.content}"
            }
        ]
    response_manager = InMemoryResponseManager()
    for i in messages:
        response_manager.add_response(role=i["role"], content = i["content"])
    chat_client = GPTChatCompletionClient(response_manager=response_manager, 
                                          base_url=ENDPOINT_OPENAI_GPT4, 
                                          api=OPENAI_GPT4_KEY,
                                          api_version=CHAT_VERSION,
                                          deployment_name=CHAT_DEPLOYMENT_NAME)
    chat_response = chat_client.call(messages=messages)
    msgs = chat_client.parse_response(chat_response)
    for i in msgs:
        chat_client.add_memory(role = "assistant", content = i)
    return {"data": chat_client.get_history()[-1]}

class ColumnResult(BaseModel):
    status: str
    content: str
    source: List[str]

class JobInformation(BaseModel):
    company: str
    results: Dict[str, ColumnResult]

@router.get("/company-job-info")
async def get_company_job_info(company: str, job_position: str):
    # Build the query for the Perplexity API
    query = f"""
        Task:
            - Provide a comprehensive summary about {company} and the job position {job_position}. Gather the following information:
            1. **Job Description:**
                - Search LinkedIn, the Company Career Site, Indeed, and Glassdoor for the job posting details.
            2. **Salary/Pay Range:**
                - Search http://levels.fyi/ for details on the salary range for {job_position} at {company}.
            3. **Interview Process:**
                - Gather insights from interview process reviews.
                - Identify whether the technical interviews are more focused on algorithms or data structures.
                - Explicity specify the range of total number of rounds, breaking them down into behavioral and technical rounds.
                - Include the typical overall duration of the interview process.
            4. **Interview Experience:**
                - Find an example of an interview experience for {job_position} at {company}.
            5. **Recommended Preparation:**
                - Search Reddit and Leetcode for recommended Leetcode problems for {company}.

            Output Requirements:
            - Output a JSON object in the following format, and do not include any additional text or markdown:

            {{
                "company": "{company}",
                "results": {{
                    "job_description": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Concise summary of the job posting>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "pay_range": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Details on the salary range>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "interview_process": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Details on the interview process, including round counts (behavioral and technical) and overall duration>",
                    "source": ["<url1>", "<url2>", ...]
                    }},
                    "example_interview_experience": {{
                    "status": "<Validated|Needs Work|Incorrect>",
                    "content": "<Example of an interview experience>",
                    "source": ["<url1>", "<url2>", ...]
                    }}
                }}
            }}
    """

    

    messages = [
        {
            "role": "system",
            "content": (
                "Give a consice but informative answer"
            ),
        },
        {   
            "role": "user",
            "content": (
                query
            ),
        },
    ]       
    response_format = {
		    "type": "json_schema",
        "json_schema": {"schema": JobInformation.model_json_schema()}
    }
    prelixty_client = PerplexityClient(api_key=PERPLEXITY_API_KEY, 
                                       api_url="https://api.perplexity.ai/chat/completions", 
                                       model="sonar")
    response = await prelixty_client.get_response(messages=messages, response_format=response_format)
    print(type(response))
    print(("Raw response from API: %r", response))
    cleaned = re.sub(r"^```json\s*", "", response)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        response = json.loads(cleaned)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    try:
        response_format = JobInformation(**response)
    except Exception as e:
        print("ERROR RESPONSE", e)
        raise HTTPException(status_code=500, detail="Response validation failed")

    return {"data": response_format}
