SOPS = {
    "pricing": {
        "keywords": ["price", "pricing", "cost", "quote", "package"],
        "response": "Thank you for your interest. Our team will share pricing details shortly."
    },
    "booking": {
        "keywords": ["book", "appointment", "schedule", "meeting"],
        "response": "Thank you for your booking enquiry. We will contact you soon."
    },
    "complaint": {
        "keywords": ["complaint", "issue", "problem", "refund"],
        "response": "We're sorry for the inconvenience. A support representative will review your case."
    },
    "after_hours": {
        "keywords": ["closed", "tomorrow", "office hours"],
        "response": "We received your enquiry outside business hours and will respond soon."
    }
}


def match_sop(message: str):
    message = message.lower()

    for sop_name, sop_data in SOPS.items():

        for keyword in sop_data["keywords"]:

            if keyword in message:
                return {
                    "matched_sop": sop_name,
                    "response": sop_data["response"]
                }

    return None