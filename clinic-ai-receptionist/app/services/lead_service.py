"""
Lead Service — CRUD operations for leads
"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.lead import Lead


def create_lead(
    db: Session,
    whatsapp_id: str,
    name: str = None,
    phone: str = None,
    intent: str = None,
    goal: str = None,
    interest: str = None,
    source: str = "whatsapp",
):
    """Create a new lead."""
    lead = Lead(
        whatsapp_id=whatsapp_id,
        name=name,
        phone=phone,
        intent=intent,
        goal=goal,
        interest=interest,
        source=source,
        lead_status="new",
        qualification="new",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def get_lead_by_whatsapp(db: Session, whatsapp_id: str):
    """Get the most recent lead for a WhatsApp user."""
    return db.query(Lead).filter(
        Lead.whatsapp_id == whatsapp_id
    ).order_by(Lead.created_at.desc()).first()


def get_lead_by_id(db: Session, lead_id: int):
    """Get a lead by ID."""
    return db.query(Lead).filter(Lead.id == lead_id).first()


def update_lead_info(
    db: Session,
    lead_id: int,
    **kwargs,
):
    """Update lead information."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None

    for key, value in kwargs.items():
        if hasattr(lead, key) and value is not None:
            setattr(lead, key, value)

    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    return lead


def get_all_leads(
    db: Session,
    status: str = None,
    limit: int = 100,
):
    """Get all leads, optionally filtered by status."""
    query = db.query(Lead)

    if status:
        query = query.filter(Lead.lead_status == status)

    return query.order_by(Lead.created_at.desc()).limit(limit).all()


def get_lead_stats(db: Session):
    """Get lead statistics for the dashboard."""
    total = db.query(Lead).count()
    new = db.query(Lead).filter(Lead.lead_status == "new").count()
    interested = db.query(Lead).filter(Lead.lead_status == "interested").count()
    qualified = db.query(Lead).filter(Lead.lead_status == "qualified").count()
    hot = db.query(Lead).filter(Lead.lead_status == "hot").count()
    follow_up = db.query(Lead).filter(Lead.lead_status == "follow_up").count()
    converted = db.query(Lead).filter(Lead.lead_status == "converted").count()
    lost = db.query(Lead).filter(Lead.lead_status == "lost").count()

    return {
        "total": total,
        "new": new,
        "interested": interested,
        "qualified": qualified,
        "hot": hot,
        "follow_up": follow_up,
        "converted": converted,
        "lost": lost,
    }


def save_conversation_to_lead(
    db: Session,
    whatsapp_id: str,
    messages: list,
    lead_info: dict,
):
    """Save conversation summary to the lead."""
    lead = get_lead_by_whatsapp(db, whatsapp_id)

    if not lead:
        lead = create_lead(
            db=db,
            whatsapp_id=whatsapp_id,
            name=lead_info.get("name"),
            phone=lead_info.get("phone"),
            intent=lead_info.get("intent"),
            goal=lead_info.get("goal"),
            interest=lead_info.get("interest"),
        )

    # Update with latest info
    if lead_info.get("name"):
        lead.name = lead_info["name"]
    if lead_info.get("phone"):
        lead.phone = lead_info["phone"]
    if lead_info.get("intent"):
        lead.intent = lead_info["intent"]
    if lead_info.get("goal"):
        lead.goal = lead_info["goal"]
    if lead_info.get("interest"):
        lead.interest = lead_info["interest"]
    if lead_info.get("lead_status"):
        lead.lead_status = lead_info["lead_status"]
    if lead_info.get("serious_buyer"):
        lead.serious_buyer = True
        if lead.lead_status == "new":
            lead.lead_status = "interested"

    # Build conversation summary
    summary_lines = []
    for msg in messages[-10:]:  # Last 10 messages
        role = "User" if msg["role"] == "user" else "AI"
        summary_lines.append(f"{role}: {msg['content'][:100]}")

    lead.conversation_summary = "\n".join(summary_lines)
    lead.last_message = messages[-1]["content"] if messages else ""
    lead.message_count = len(messages)
    lead.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(lead)
    return lead
