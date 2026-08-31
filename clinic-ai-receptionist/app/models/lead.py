from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # Contact info
    name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    whatsapp_id = Column(String(50), nullable=True)

    # Intent & qualification
    intent = Column(String(50), nullable=True)  # membership, personal_training, visit, pricing
    interest = Column(String(50), nullable=True)  # membership, pt, both, visit
    goal = Column(String(100), nullable=True)  # weight_loss, muscle_gain, general_fitness
    timeline = Column(String(50), nullable=True)  # immediately, this_week, this_month, just_exploring
    availability = Column(String(50), nullable=True)  # morning, afternoon, evening
    budget = Column(String(50), nullable=True)

    # Lead status
    lead_status = Column(String(50), default="new")  # new, interested, qualified, hot, follow_up, converted, lost
    qualification = Column(String(50), default="new")  # new, marketing_qualified, sales_qualified
    serious_buyer = Column(Boolean, default=False)

    # Source tracking
    source = Column(String(50), default="whatsapp")  # whatsapp, meta_ads, referral, walk_in
    campaign = Column(String(100), nullable=True)

    # Conversation
    conversation_summary = Column(Text, nullable=True)
    last_message = Column(Text, nullable=True)
    message_count = Column(Integer, default=0)

    # Internal notes (owner/team use only, never shown to customer)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_contacted_at = Column(DateTime, nullable=True)
    follow_up_at = Column(DateTime, nullable=True)
