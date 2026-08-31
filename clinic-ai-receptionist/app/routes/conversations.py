"""
Conversation API — Clean endpoints for sending/receiving messages.

These are transport-agnostic. The webhook route uses these
internally. They can also be called directly for testing.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.conversation_service import process_message
from app.services.session_manager import (
    get_session,
    get_lead,
    get_conversation_history,
    clear_session,
    is_handed_off,
    set_handoff,
    sessions as _sessions,
)
from app.services.lead_service import save_conversation_to_lead

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class SendMessageRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="Unique user identifier (e.g. phone number or WhatsApp ID)",
        examples=["919876543210"],
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The user's message text",
        examples=["What are your membership plans?"],
    )


class SendMessageResponse(BaseModel):
    reply: str = Field(
        ...,
        description="AI-generated reply text",
    )
    user_id: str


class ConversationHistoryResponse(BaseModel):
    user_id: str
    messages: list
    total: int


class LeadInfoResponse(BaseModel):
    user_id: str
    lead: dict


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/send",
    response_model=SendMessageResponse,
    summary="Send a message and get an AI reply",
    description=(
        "Processes an incoming user message through the conversation "
        "service and returns the AI-generated reply. Also updates "
        "session memory and lead information automatically."
    ),
)
def send_message(request: SendMessageRequest):
    try:
        reply = process_message(
            user_id=request.user_id,
            message=request.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}",
        )

    return SendMessageResponse(
        reply=reply,
        user_id=request.user_id,
    )


@router.get(
    "/{user_id}/history",
    response_model=ConversationHistoryResponse,
    summary="Get conversation history for a user",
)
def get_history(user_id: str):
    messages = get_conversation_history(user_id)
    return ConversationHistoryResponse(
        user_id=user_id,
        messages=messages,
        total=len(messages),
    )


@router.get(
    "/{user_id}/lead",
    response_model=LeadInfoResponse,
    summary="Get lead information collected from a user",
)
def get_lead_info(user_id: str):
    lead = get_lead(user_id)
    return LeadInfoResponse(
        user_id=user_id,
        lead=lead,
    )


@router.delete(
    "/{user_id}",
    summary="Clear a user's conversation session",
)
def delete_session(user_id: str):
    clear_session(user_id)
    return {"message": f"Session cleared for {user_id}"}


# ---------------------------------------------------------------------------
# Handoff — mark conversation for human takeover
# ---------------------------------------------------------------------------

@router.post(
    "/{user_id}/handoff",
    summary="Hand off conversation to a human agent",
    description=(
        "Marks this conversation as handed off. Subsequent messages "
        "from this user should be routed to a human agent instead "
        "of the AI. The session and lead data are preserved."
    ),
)
def handoff_conversation(user_id: str):
    session = get_session(user_id)
    set_handoff(user_id, True)
    return {
        "message": f"Conversation handed off for {user_id}",
        "user_id": user_id,
        "handoff": True,
        "messages_in_session": len(session.get("messages", [])),
    }


@router.post(
    "/{user_id}/reset",
    summary="Reset a user's conversation session",
    description=(
        "Clears the in-memory session for this user. "
        "Lead data in the database is NOT deleted — only the "
        "live conversation context is wiped. A new session will "
        "start on the next incoming message."
    ),
)
def reset_conversation(user_id: str):
    was_active = user_id in _sessions
    clear_session(user_id)
    return {
        "message": f"Session reset for {user_id}",
        "user_id": user_id,
        "had_session": was_active,
    }
