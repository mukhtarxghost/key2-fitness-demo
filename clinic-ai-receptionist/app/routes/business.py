"""
Business API — Read-only access to Key 2 Fitness configuration.

No authentication for now. This exists so the frontend/owner
can pull business info programmatically, and so the AI can
be rebuilt or audited against the source of truth.
"""

from fastapi import APIRouter

from app.config.key2_business import (
    BUSINESS_NAME,
    BUSINESS_TYPE,
    CURRENCY,
    CURRENCY_SYMBOL,
    MEMBERSHIP_PLANS,
    PERSONAL_TRAINING,
    GYM_TIMINGS,
    FACILITIES,
    GROUP_CLASSES,
    LOCATION,
    CONTACT,
    CURRENT_OFFERS,
    TRIAL_INFO,
    QUALIFICATION_QUESTIONS,
)

router = APIRouter(
    prefix="/business",
    tags=["Business"],
)


@router.get("/", summary="Full business profile")
def get_business():
    return {
        "name": BUSINESS_NAME,
        "type": BUSINESS_TYPE,
        "currency": CURRENCY,
        "currency_symbol": CURRENCY_SYMBOL,
        "timings": GYM_TIMINGS,
        "facilities": FACILITIES,
        "group_classes": GROUP_CLASSES,
        "location": LOCATION,
        "contact": CONTACT,
        "current_offers": CURRENT_OFFERS,
        "trial": TRIAL_INFO,
        "qualification_questions": QUALIFICATION_QUESTIONS,
    }


@router.get("/memberships", summary="Membership plans")
def get_memberships():
    return {
        "currency": CURRENCY_SYMBOL,
        "plans": MEMBERSHIP_PLANS,
    }


@router.get("/personal-training", summary="Personal training packages and trainers")
def get_personal_training():
    return {
        "currency": CURRENCY_SYMBOL,
        "available": PERSONAL_TRAINING["available"],
        "packages": PERSONAL_TRAINING["packages"],
        "trainers": PERSONAL_TRAINING["trainers"],
        "total_trainers": PERSONAL_TRAINING["total_trainers"],
    }
