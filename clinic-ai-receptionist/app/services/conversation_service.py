"""
Conversation Service — Core conversation logic.

Orchestrates:
  incoming message → context building → LLM call → response

This layer is transport-agnostic. It does NOT know about
WhatsApp, webhooks, or HTTP. It just processes messages.
"""

from app.config.key2_business import (
    BUSINESS_NAME,
    AI_CONFIG,
    get_business_summary,
)
from app.services.llm_provider import get_llm_provider
from app.services.session_manager import (
    get_session,
    get_lead,
    update_lead,
    add_message,
    get_conversation_history,
)

# ---------------------------------------------------------------------------
# System prompt — built once at import from verified business config
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = f"""
You are a friendly, professional AI receptionist for {BUSINESS_NAME}.

Your job is to help potential members with:
- Membership plans and pricing
- Personal training options
- Gym timings and facilities
- Scheduling a visit
- Answering fitness-related questions about the gym

You are NOT a generic chatbot. You work FOR {BUSINESS_NAME}.

==================================================
BUSINESS INFORMATION
==================================================

{get_business_summary()}

==================================================
IMPORTANT RULES
==================================================

1. NEVER invent prices, plans, trainers, timings, or facilities.
2. ALL business information MUST come from the data provided above.
3. If you don't have specific information, say:
   "I don't have that exact detail right now, but I can have
   someone from our team reach out to you with the complete
   information."
4. NEVER make up trainer names, class schedules, or special offers.
5. NEVER promise discounts, deals, or offers that aren't listed.
6. NEVER fabricate facility names or equipment.

==================================================
CONVERSATION STYLE
==================================================

1. Be warm, friendly, and enthusiastic about fitness.
2. Use simple, clear language. Avoid jargon.
3. Keep responses concise — this is WhatsApp, not an essay.
4. Use emojis sparingly but naturally.
5. Be conversational — like a real person, not a robot.
6. Remember what the user already told you. Don't ask again.
7. If user says "I already told you", apologize and use
   the context from the conversation.

==================================================
LEAD CAPTURE
==================================================

When someone shows genuine interest, naturally ask for:
1. Their name
2. Phone number (if not already known)
3. What they're looking for (membership/PT/both)
4. Their fitness goal
5. When they want to start

DO NOT force this information. If they're just browsing,
answer their questions and let them go.

==================================================
WHAT NOT TO DO
==================================================

1. Don't claim to be human. You're an AI assistant.
2. Don't promise anything you can't verify.
3. Don't share other customers' information.
4. Don't discuss competitor gyms.
5. Don't give medical or diet advice.
6. Don't repeat the same question if already answered.
7. Don't write long paragraphs — keep it WhatsApp-friendly.
"""


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def process_message(
    user_id: str,
    message: str,
) -> str:
    """
    Process a single incoming message and return the AI reply.

    Transport-agnostic — works for WhatsApp, web, API, etc.
    """
    session = get_session(user_id)
    lead = get_lead(user_id)
    history = get_conversation_history(user_id)

    # Build user prompt with context
    history_text = ""
    for msg in history[-20:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    lead_context = ""
    if lead.get("name"):
        lead_context += f"Customer name: {lead['name']}\n"
    if lead.get("phone"):
        lead_context += f"Phone: {lead['phone']}\n"
    if lead.get("intent"):
        lead_context += f"Intent: {lead['intent']}\n"
    if lead.get("goal"):
        lead_context += f"Goal: {lead['goal']}\n"

    user_prompt = f"""
Conversation History:
{history_text if history_text else "(No prior messages)"}

Lead Information:
{lead_context if lead_context else "No lead info collected yet."}

Current User Message:
{message}
"""

    # Call LLM
    provider = get_llm_provider()
    reply = provider.generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    # Track messages
    add_message(user_id, "user", message)
    add_message(user_id, "assistant", reply)

    # Extract lead info from message
    _extract_lead_info(user_id, message)

    return reply


# ---------------------------------------------------------------------------
# Lead extraction — lightweight heuristics
# ---------------------------------------------------------------------------

import re


def _extract_lead_info(user_id: str, message: str):
    """Extract lead information from user message using heuristics."""
    msg_lower = message.lower().strip()
    lead = get_lead(user_id)

    # Name detection
    name_patterns = [
        r"my name is (\w+)",
        r"i'm (\w+)",
        r"i am (\w+)",
        r"call me (\w+)",
        r"this is (\w+)",
        r"name[:\s]+(\w+)",
    ]
    stop_words = {
        "looking", "interested", "checking", "asking",
        "want", "need", "trying", "here", "just",
        "the", "a", "an", "and", "or", "but",
    }
    for pattern in name_patterns:
        match = re.search(pattern, msg_lower)
        if match and not lead.get("name"):
            name = match.group(1).title()
            if len(name) > 1 and name.lower() not in stop_words:
                update_lead(user_id, "name", name)

    # Phone detection — Indian phone numbers
    phone_match = re.search(
        r"(?:\+?91[\s-]?)?([6-9]\d{9})", message
    )
    if phone_match and not lead.get("phone"):
        update_lead(user_id, "phone", phone_match.group(1))

    # Intent detection
    intent_keywords = {
        "membership": ["membership", "join", "member", "plan", "subscribe"],
        "personal_training": ["personal training", "pt", "trainer", "training", "coach"],
        "visit": ["visit", "come", "tour", "see"],
        "pricing": ["price", "cost", "how much", "rate", "fee", "charge"],
        "timing": ["timing", "time", "hour", "open", "close", "when"],
    }
    for intent, keywords in intent_keywords.items():
        if any(kw in msg_lower for kw in keywords):
            if not lead.get("intent"):
                update_lead(user_id, "intent", intent)
            break

    # Goal detection
    goal_keywords = {
        "weight_loss": ["weight loss", "lose weight", "fat", "slim", "lean"],
        "muscle_gain": ["muscle", "bulk", "gain", "strength", "build"],
        "general_fitness": ["fitness", "health", "fit", "active", "exercise"],
    }
    for goal, keywords in goal_keywords.items():
        if any(kw in msg_lower for kw in keywords):
            if not lead.get("goal"):
                update_lead(user_id, "goal", goal)
            break

    # Serious buyer signal
    serious_keywords = [
        "join", "sign up", "register", "book", "enroll",
        "start", "today", "now", "where", "location", "address",
    ]
    if any(kw in msg_lower for kw in serious_keywords):
        update_lead(user_id, "serious_buyer", True)
        if lead.get("lead_status") == "new":
            update_lead(user_id, "lead_status", "interested")
