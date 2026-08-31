from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.lead_service import (
    create_lead,
    get_all_leads,
    get_lead_by_id,
    update_lead_info,
    get_lead_stats,
)

router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class LeadCreate(BaseModel):
    whatsapp_id: str = Field(..., description="WhatsApp ID of the lead")
    name: Optional[str] = Field(None, description="Lead name")
    phone: Optional[str] = Field(None, description="Phone number")
    intent: Optional[str] = Field(None, description="membership, personal_training, visit, pricing")
    goal: Optional[str] = Field(None, description="weight_loss, muscle_gain, general_fitness")
    interest: Optional[str] = Field(None, description="membership, pt, both")
    timeline: Optional[str] = Field(None, description="immediately, this_week, this_month, just_exploring")
    source: str = Field("whatsapp", description="whatsapp, meta_ads, referral, walk_in")


class LeadStatusUpdate(BaseModel):
    lead_status: str = Field(..., description="new, interested, qualified, hot, follow_up, converted, lost")
    qualification: Optional[str] = Field(None, description="new, marketing_qualified, sales_qualified")


class LeadNotesUpdate(BaseModel):
    notes: str = Field(..., description="Internal notes for this lead")


class LeadSummary(BaseModel):
    id: int
    name: Optional[str]
    phone: Optional[str]
    whatsapp_id: Optional[str]
    intent: Optional[str]
    goal: Optional[str]
    interest: Optional[str]
    timeline: Optional[str]
    lead_status: Optional[str]
    qualification: Optional[str]
    serious_buyer: bool
    source: Optional[str]
    message_count: int
    created_at: Optional[str]
    updated_at: Optional[str]


def _serialize_lead(lead) -> dict:
    return {
        "id": lead.id,
        "name": lead.name,
        "phone": lead.phone,
        "whatsapp_id": lead.whatsapp_id,
        "intent": lead.intent,
        "goal": lead.goal,
        "interest": lead.interest,
        "timeline": lead.timeline,
        "availability": lead.availability,
        "budget": lead.budget,
        "lead_status": lead.lead_status,
        "qualification": lead.qualification,
        "serious_buyer": lead.serious_buyer,
        "source": lead.source,
        "campaign": lead.campaign,
        "conversation_summary": lead.conversation_summary,
        "last_message": lead.last_message,
        "message_count": lead.message_count,
        "notes": lead.notes,
        "created_at": str(lead.created_at) if lead.created_at else None,
        "updated_at": str(lead.updated_at) if lead.updated_at else None,
        "last_contacted_at": str(lead.last_contacted_at) if lead.last_contacted_at else None,
        "follow_up_at": str(lead.follow_up_at) if lead.follow_up_at else None,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", summary="List all leads")
def list_leads(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    leads = get_all_leads(db, status=status)
    return {
        "leads": [_serialize_lead(lead) for lead in leads],
        "total": len(leads),
    }


@router.get("/stats", summary="Lead counts by status")
def lead_stats(db: Session = Depends(get_db)):
    return get_lead_stats(db)


@router.post("/", status_code=201, summary="Create a new lead")
def create_new_lead(body: LeadCreate, db: Session = Depends(get_db)):
    lead = create_lead(
        db=db,
        whatsapp_id=body.whatsapp_id,
        name=body.name,
        phone=body.phone,
        intent=body.intent,
        goal=body.goal,
        interest=body.interest,
        source=body.source,
    )
    return _serialize_lead(lead)


@router.get("/{lead_id}", summary="Get a single lead")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return _serialize_lead(lead)


@router.get("/{lead_id}/conversation", summary="Get conversation summary stored on a lead")
def get_lead_conversation(lead_id: int, db: Session = Depends(get_db)):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {
        "lead_id": lead.id,
        "name": lead.name,
        "conversation_summary": lead.conversation_summary,
        "last_message": lead.last_message,
        "message_count": lead.message_count,
    }


@router.put("/{lead_id}/status", summary="Update lead status")
def update_lead_status(lead_id: int, body: LeadStatusUpdate, db: Session = Depends(get_db)):
    data = {"lead_status": body.lead_status}
    if body.qualification:
        data["qualification"] = body.qualification
    lead = update_lead_info(db, lead_id, **data)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Status updated", "lead_id": lead.id, "lead_status": lead.lead_status}


@router.put("/{lead_id}/notes", summary="Update internal notes on a lead")
def update_lead_notes(lead_id: int, body: LeadNotesUpdate, db: Session = Depends(get_db)):
    lead = update_lead_info(db, lead_id, notes=body.notes)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Notes updated", "lead_id": lead.id, "notes": lead.notes}


@router.put("/{lead_id}", summary="Update any lead fields")
def update_lead(lead_id: int, body: LeadCreate, db: Session = Depends(get_db)):
    data = body.dict(exclude_unset=True)
    lead = update_lead_info(db, lead_id, **data)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead updated", "lead_id": lead.id}
