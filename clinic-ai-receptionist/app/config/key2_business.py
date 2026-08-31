"""
Key 2 Fitness — Business Configuration
=======================================

All verified information about Key 2 Fitness.

RULES:
- Only use information defined here.
- Anything marked UNKNOWN must never be fabricated by the AI.
- If a customer asks about UNKNOWN items, the AI should say
  "I don't have that specific information right now, but I can
  have someone from our team get back to you on that."
"""

# ==========================================================
# BUSINESS IDENTITY
# ==========================================================

BUSINESS_NAME = "Key 2 Fitness"
BUSINESS_TYPE = "Fitness Gym"
CURRENCY = "INR"
CURRENCY_SYMBOL = "₹"

# ==========================================================
# BUSINESS CONTEXT (known from conversations)
# ==========================================================

OPERATIONAL = {
    "monthly_enquiries": "70-80",
    "meta_ads_spend_monthly": "₹20,000",
    "marketing_person_spend_monthly": "₹20,000",
    "owner_interest": "diversification through automation",
}

# ==========================================================
# MEMBERSHIP PLANS (VERIFIED)
# ==========================================================

MEMBERSHIP_PLANS = [
    {
        "id": "monthly",
        "name": "Monthly Plan",
        "price": "₹2,999",
        "price_value": 2999,
        "duration": "1 month",
        "features": [
            "Full gym access",
            "All equipment & machines",
            "Locker room facilities",
        ],
        "status": "verified",
    },
    {
        "id": "quarterly",
        "name": "3-Month Plan",
        "price": "₹3,999",
        "price_value": 3999,
        "duration": "3 months",
        "features": [
            "Full gym access",
            "All equipment & machines",
            "Locker room facilities",
            "Best value for short commitment",
        ],
        "status": "verified",
    },
    {
        "id": "half_yearly",
        "name": "6-Month Plan",
        "price": "₹5,999",
        "price_value": 5999,
        "duration": "6 months",
        "features": [
            "Full gym access",
            "All equipment & machines",
            "Locker room facilities",
            "Great savings over monthly",
        ],
        "status": "verified",
    },
    {
        "id": "annual",
        "name": "12-Month Plan",
        "price": "₹7,999",
        "price_value": 7999,
        "duration": "12 months",
        "features": [
            "Full gym access",
            "All equipment & machines",
            "Locker room facilities",
            "Best value — lowest monthly cost",
        ],
        "status": "verified",
    },
]

# ==========================================================
# PERSONAL TRAINING (VERIFIED)
# ==========================================================

PERSONAL_TRAINING = {
    "available": True,
    "packages": [
        {
            "id": "pt_standard",
            "name": "Personal Training Package",
            "sessions": 20,
            "price": "₹9,999",
            "price_value": 9999,
            "session_duration": "UNKNOWN",
            "features": [
                "20 one-on-one PT sessions",
                "Personalized workout plan",
                "Guided by trained professionals",
            ],
            "status": "verified",
        },
    ],
    "trainers": [
        {
            "name": "UNKNOWN",
            "specialization": "UNKNOWN",
            "experience": "UNKNOWN",
            "available_slots": "UNKNOWN",
            "status": "needs_verification",
        },
        {
            "name": "UNKNOWN",
            "specialization": "UNKNOWN",
            "experience": "UNKNOWN",
            "available_slots": "UNKNOWN",
            "status": "needs_verification",
        },
        {
            "name": "UNKNOWN",
            "specialization": "UNKNOWN",
            "experience": "UNKNOWN",
            "available_slots": "UNKNOWN",
            "status": "needs_verification",
        },
    ],
    "total_trainers": 3,
}

# ==========================================================
# GYM TIMINGS (VERIFIED)
# ==========================================================

GYM_TIMINGS = {
    "weekdays": "6:00 AM - 10:00 PM (Monday to Saturday)",
    "weekends": "8:00 AM - 12:00 PM (Sunday)",
    "holidays": "UNKNOWN",
    "monday_to_saturday": "6:00 AM - 10:00 PM",
    "sunday": "8:00 AM - 12:00 PM",
}

# ==========================================================
# FACILITIES / EQUIPMENT
# ==========================================================

FACILITIES = [
    "UNKNOWN — owner to provide full list",
]

# ==========================================================
# GROUP CLASSES / SESSIONS
# ==========================================================

GROUP_CLASSES = [
    # UNKNOWN — owner to provide class schedule
]

# ==========================================================
# LOCATION
# ==========================================================

LOCATION = {
    "address": "UNKNOWN",
    "city": "UNKNOWN",
    "landmark": "UNKNOWN",
    "pincode": "UNKNOWN",
    "google_maps_link": "UNKNOWN",
}

# ==========================================================
# CONTACT INFORMATION
# ==========================================================

CONTACT = {
    "phone": "UNKNOWN",
    "whatsapp": "UNKNOWN",
    "email": "UNKNOWN",
    "instagram": "UNKNOWN",
    "facebook": "UNKNOWN",
}

# ==========================================================
# OFFERS / PROMOTIONS
# ==========================================================

CURRENT_OFFERS = []

# ==========================================================
# TRIAL / VISIT
# ==========================================================

TRIAL_INFO = {
    "free_trial_available": "UNKNOWN",
    "trial_duration": "UNKNOWN",
    "trial_conditions": "UNKNOWN",
    "walk_in_available": "UNKNOWN",
}

# ==========================================================
# LEAD QUALIFICATION QUESTIONS
# ==========================================================

QUALIFICATION_QUESTIONS = {
    "interest": "What brings you to Key 2 Fitness? Are you looking for gym membership or personal training?",
    "goal": "What's your primary fitness goal? Weight loss, muscle gain, general fitness, or something else?",
    "experience": "Have you been to a gym before or is this your first time?",
    "timeline": "When are you looking to start?",
    "availability": "What time of day usually works best for you?",
    "budget": "Do you have a budget in mind for your fitness journey?",
    "contact": "Can I get your name and phone number so our team can reach out with more details?",
}

# ==========================================================
# AI BEHAVIOR CONFIGURATION
# ==========================================================

AI_CONFIG = {
    "greeting": (
        f"Hey! Welcome to {BUSINESS_NAME} 💪\n\n"
        "I'm your virtual assistant. I can help you with:\n\n"
        "• Membership plans & pricing\n"
        "• Personal training options\n"
        "• Gym timings & facilities\n"
        "• Scheduling a visit\n\n"
        "What would you like to know?"
    ),
    "fallback": (
        "I don't have that specific information right now, "
        "but I can have someone from our team get back to you "
        "on that. Would you like me to arrange a callback?"
    ),
    "unknown_handler": (
        "That's a great question! I want to make sure I give "
        "you accurate information. Let me have our team reach "
        "out to you with the exact details. Can I get your "
        "name and number?"
    ),
    "closing": (
        "Thanks for your interest in Key 2 Fitness! 💪 "
        "Our team will reach out to you soon with all the "
        "details. Looking forward to helping you start your "
        "fitness journey!"
    ),
    "max_unknown_before_escalation": 2,
}


# ==========================================================
# HELPERS
# ==========================================================

def get_membership_summary():
    """Return membership plans formatted for AI context."""
    lines = [f"=== {BUSINESS_NAME} MEMBERSHIP PLANS ===\n"]
    for plan in MEMBERSHIP_PLANS:
        lines.append(
            f"• {plan['name']} ({plan['duration']}) — {plan['price']}"
        )
        for f in plan["features"]:
            lines.append(f"  - {f}")
        lines.append("")
    return "\n".join(lines)


def get_pt_summary():
    """Return PT information formatted for AI context."""
    lines = [f"=== {BUSINESS_NAME} PERSONAL TRAINING ===\n"]
    for pkg in PERSONAL_TRAINING["packages"]:
        lines.append(
            f"• {pkg['name']} — {pkg['sessions']} sessions — {pkg['price']}"
        )
        for f in pkg["features"]:
            lines.append(f"  - {f}")
        lines.append("")
    if PERSONAL_TRAINING["trainers"]:
        lines.append(f"Number of Trainers: {PERSONAL_TRAINING['total_trainers']}")
    return "\n".join(lines)


def get_timings_summary():
    """Return gym timings formatted for AI context."""
    return (
        f"=== {BUSINESS_NAME} TIMINGS ===\n"
        f"Monday to Saturday: {GYM_TIMINGS['monday_to_saturday']}\n"
        f"Sunday: {GYM_TIMINGS['sunday']}\n"
    )


def get_business_summary():
    """Return full business info formatted for AI context."""
    parts = [
        f"=== {BUSINESS_NAME} ===",
        f"Type: {BUSINESS_TYPE}",
        f"Currency: {CURRENCY_SYMBOL}\n",
        get_membership_summary(),
        get_pt_summary(),
        get_timings_summary(),
    ]

    if FACILITIES and not any("UNKNOWN" in f for f in FACILITIES):
        parts.append("=== FACILITIES ===")
        for fac in FACILITIES:
            parts.append(f"• {fac}")
        parts.append("")

    if GROUP_CLASSES:
        parts.append("=== GROUP CLASSES ===")
        for cls in GROUP_CLASSES:
            parts.append(f"• {cls['name']} — {cls['days']} — {cls['time']}")
        parts.append("")

    if CURRENT_OFFERS:
        parts.append("=== CURRENT OFFERS ===")
        for offer in CURRENT_OFFERS:
            parts.append(
                f"• {offer['title']}: {offer['description']} "
                f"(valid till {offer['valid_until']})"
            )
        parts.append("")

    return "\n".join(parts)
