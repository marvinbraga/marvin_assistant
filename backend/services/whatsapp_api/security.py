import hashlib
import hmac
import logging
import os

from dotenv import load_dotenv, find_dotenv
from fastapi import Request, HTTPException

load_dotenv(find_dotenv())

APP_SECRET = os.environ["APP_SECRET"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]


def validate_signature(payload: str, signature: str):
    """
    Validate the incoming payload's signature against our expected signature.
    """
    # Use the App Secret to hash the payload
    expected_signature = hmac.new(
        bytes(APP_SECRET, "latin-1"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Check if the signature matches
    return hmac.compare_digest(expected_signature, signature) or signature == VERIFY_TOKEN


async def signature_required(request: Request):
    """
    Dependency to ensure that the incoming requests to our webhook are valid and signed with
    the correct signature.
    """
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")[7:] or request.query_params.get("hub.verify_token", "")

    if not validate_signature(body.decode("utf-8"), signature):
        logging.info("Signature verification failed!")
        raise HTTPException(status_code=403, detail="Invalid signature")
    return True
