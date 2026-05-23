from app.database.database import SessionLocal
from app.models.enquiry import Enquiry
from app.models.event import Event

from app.services.sop_matcher import match_sop
from app.logger.logger import logger


def process_enquiry(enquiry_id: int):

    db = SessionLocal()

    logger.info(
        "task_processing_started",
        extra={
            "enquiry_id": enquiry_id
        }
    )

    try:

        enquiry = (
            db.query(Enquiry)
            .filter(Enquiry.id == enquiry_id)
            .first()
        )

        if not enquiry:
            return

        result = match_sop(enquiry.message)

        if result:

            enquiry.matched_sop = result["matched_sop"]
            enquiry.suggested_response = result["response"]
            enquiry.status = "open"

            event = Event(
                enquiry_id=enquiry.id,
                event_type="SOP_MATCHED",
                details=result["matched_sop"]
            )

            db.add(event)

            logger.info(
                "sop_matched",
                extra={
                    "enquiry_id": enquiry.id,
                    "matched_sop": result["matched_sop"]
                }
            )

        else:

            enquiry.status = "escalated"

            event = Event(
                enquiry_id=enquiry.id,
                event_type="AUTO_ESCALATED",
                details="No SOP matched"
            )

            db.add(event)

            logger.warning(
                "auto_escalation_triggered",
                extra={
                    "enquiry_id": enquiry.id,
                    "reason": "No SOP matched"
                }
            )

        db.commit()

    finally:
        db.close()