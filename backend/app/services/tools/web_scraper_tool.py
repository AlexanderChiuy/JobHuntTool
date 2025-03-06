from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from crewai.tools.base_tool import BaseTool
from langchain.chains import create_extraction_chain
from typing import List
from config.keys import *
from services.clients.openai_client import *
from pydantic import BaseModel, Field
from typing import Type
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup

chat_client = GPTChatCompletionClient(base_url=ENDPOINT_OPENAI_GPT4, 
                                      api=OPENAI_GPT4_KEY,
                                      api_version=CHAT_VERSION,
                                      deployment_name=CHAT_DEPLOYMENT_NAME)

# List of tags to extract
tags_to_extract = ['span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

def extract(content: List[str]) -> str:
    messages = [
            {
                "role": "system", 
                "content": "You are an assistant. who is reading scraped data from a list of website urls and extracting information", 
            },
            {
                "role": "user", 
                "content": f"the data is: {content}"
            }
        ]
    response = chat_client.call(messages=messages)
    msgs = chat_client.parse_response(response)
    return msgs[-1]

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    urls: List[str] = Field(..., description="LIST OF URLS TO SCRAPE")

class WebScrapperTool(BaseTool):
    name: str = "Webscrapper Tool"
    description: str = "A tool to use gpt-4o to extract information from a list of urls"
    args_schema: Type[BaseModel] = MyToolInput
    
    def _run(self, urls: str) -> str:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        docs = []
        for url in urls:
            driver.get(url)
            content = driver.page_source
            print(content)
            docs.append(content)
        # Close the WebDriver
        driver.quit()
        website_contents = []
        for doc in docs:
            soup = BeautifulSoup(doc, 'html.parser')
            span_text_list = []
            for span in soup.find_all(tags_to_extract):
                span_text = span.get_text(strip=True)
                span_text_list.append(span_text)
            website_contents.append(span_text_list)

        extracted_content = extract(content=website_contents)
        return extracted_content