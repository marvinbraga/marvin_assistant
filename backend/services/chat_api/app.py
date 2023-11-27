import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

load_dotenv(find_dotenv())
redis_host = os.environ["REDIS_HOST"]
llm_host = os.environ["LLM_HOST"]
llm_port = os.environ["LLM_PORT"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/alive")
async def front_conversation():
    return {"status": 200, "message": "Chat conversation is ok."}
