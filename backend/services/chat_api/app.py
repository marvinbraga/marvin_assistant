import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware

from backend.services.chat_api.apis import LlmApi
from backend.services.chat_api.conversations import Conversation
from backend.services.chat_api.services import ConversationService

load_dotenv(find_dotenv())
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


@app.get("/api/chats/{user_id}/{conversation_id}")
async def get_conversation_endpoint(user_id: str, conversation_id: str):
    key_id = f"{user_id}-{conversation_id}"
    service = ConversationService(Conversation(session_id=key_id), LlmApi(llm_host, llm_port))
    return service.get_conversation()


@app.post("/api/chats/{user_id}/{conversation_id}")
async def post_conversation_endpoint(user_id, conversation_id: str, json_data: dict = Body(None)):
    key_id = f"{user_id}-{conversation_id}"
    service = ConversationService(Conversation(session_id=key_id), LlmApi(llm_host, llm_port))
    return service.post_conversation_message(json_data.get("message"))
