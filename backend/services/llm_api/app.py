import logging
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from backend.services.llm_api.services import LLMConnection

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/alive")
async def llm_conversation():
    return {"status": 200, "message": "LLM conversation is ok."}


@app.post("/api/gpt")
async def chat_with_llm(json_data: dict = Body(None)):
    service = LLMConnection(json_data)
    result = service.send().output
    return result
