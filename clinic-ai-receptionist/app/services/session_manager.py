"""
Session Manager — Conversation memory + lead tracking
=====================================================

Each WhatsApp user gets a session dict that tracks:
- Conversation messages
- Collected lead info
- Unknown count (for escalation)
"""

sessions = {}


def get_session(user_id: str):
    if user_id not in sessions:
        sessions[user_id] = {
            "messages": [],
            "handoff": False,
            "lead": {
                "name": None,
                "phone": None,
                "intent": None,
                "goal": None,
                "interest": None,
                "timeline": None,
                "availability": None,
                "budget": None,
                "qualification": "new",
                "lead_status": "new",
                "conversation_summary": "",
                "unknown_count": 0,
                "serious_buyer": False,
            },
        }
    return sessions[user_id]


def update_session(user_id: str, key: str, value):
    session = get_session(user_id)
    session[key] = value


def update_lead(user_id: str, field: str, value):
    session = get_session(user_id)
    if "lead" in session:
        session["lead"][field] = value


def get_lead(user_id: str):
    session = get_session(user_id)
    return session.get("lead", {})


def add_message(user_id: str, role: str, content: str):
    session = get_session(user_id)
    if "messages" in session:
        session["messages"].append({
            "role": role,
            "content": content,
        })


def get_conversation_history(user_id: str):
    session = get_session(user_id)
    return session.get("messages", [])


def clear_session(user_id: str):
    if user_id in sessions:
        del sessions[user_id]


def get_all_sessions():
    return sessions


def is_handed_off(user_id: str) -> bool:
    session = get_session(user_id)
    return session.get("handoff", False)


def set_handoff(user_id: str, value: bool):
    session = get_session(user_id)
    session["handoff"] = value
