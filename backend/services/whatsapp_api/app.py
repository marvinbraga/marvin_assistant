import json
import logging

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from security import signature_required
from utils.handlers import WhatsAppMessageHandler

app = FastAPI()


async def handle_message(body: dict):
    """
    Handle incoming webhook events from the WhatsApp API.
    Similar to the original Flask function, but adapted for FastAPI.
    """
    # Check if it's a WhatsApp status update
    if body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("statuses"):
        logging.info("Received a WhatsApp status update.")
        return JSONResponse(content={"status": "ok"})

    try:
        if WhatsAppMessageHandler(body).process_message():
            return JSONResponse(content={"status": "ok"})
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not a WhatsApp API event",
            )
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON provided",
        )


async def verify(request: Request):
    """
    Required webhook verification for WhatsApp.
    Adapted for FastAPI.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == "YOUR_VERIFY_TOKEN":  # Replace with your token
            logging.info("WEBHOOK_VERIFIED")
            return challenge
        else:
            logging.info("VERIFICATION_FAILED")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Verification failed",
            )
    else:
        logging.info("MISSING_PARAMETER")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing parameters",
        )


@app.post("/webhook")
async def webhook_post(request: Request, is_valid: bool = Depends(signature_required)):
    body = await request.json()
    return await handle_message(body)


@app.get("/webhook")
async def webhook_get(request: Request):
    return await verify(request)
