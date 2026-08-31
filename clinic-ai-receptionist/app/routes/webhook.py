"""
WhatsApp Webhook — Receives Meta Cloud API webhooks.

Flow:
  Meta Webhook POST → parse message → conversation service → send reply

Meta verification (GET) is handled separately.
"""

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.conversation_service import process_message
from app.services.whatsapp_service import send_whatsapp_message
from app.services.session_manager import get_session, get_lead
from app.services.lead_service import save_conversation_to_lead

router = APIRouter()

VERIFY_TOKEN = "key2_fitness_123"


@router.get(
    "/webhook",
    summary="Verify WhatsApp webhook",
    description="Meta calls this GET endpoint to verify the webhook URL.",
)
async def verify_webhook(
    hub_mode: str,
    hub_verify_token: str,
    hub_challenge: str,
):
    if (
        hub_mode == "subscribe"
        and hub_verify_token == VERIFY_TOKEN
    ):
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse(
        "Verification failed",
        status_code=403,
    )


@router.post(
    "/webhook",
    summary="Receive WhatsApp message",
    description="Meta sends incoming WhatsApp messages to this endpoint.",
)
async def receive_message(request: Request):
    body = await request.json()

    print("=" * 80)
    print("Incoming WhatsApp Webhook")
    print(body)
    print("=" * 80)

    try:
        entry = body["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        # Ignore delivery/read/status updates
        if "messages" not in value:
            return {"status": "ignored"}

        message = value["messages"][0]

        # Ignore non-text messages
        if message["type"] != "text":
            return {"status": "unsupported"}

        phone = message["from"]
        user_message = message["text"]["body"]

        # Process through conversation service
        ai_reply = process_message(
            user_id=phone,
            message=user_message,
        )

        # Persist lead + conversation to database
        db: Session = SessionLocal()
        try:
            session = get_session(phone)
            lead_data = get_lead(phone)
            messages = session.get("messages", [])

            save_conversation_to_lead(
                db=db,
                whatsapp_id=phone,
                messages=messages,
                lead_info=lead_data,
            )
        finally:
            db.close()

        # Send reply via WhatsApp
        send_whatsapp_message(
            phone=phone,
            message=ai_reply,
        )

        return {"status": "success"}

    except Exception as e:
        print("Webhook Error:", str(e))
        return {
            "status": "error",
            "message": str(e),
        }
