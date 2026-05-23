from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from app.database.dependencies import get_db
from app.models.enquiry import Enquiry
from app.models.event import Event
from app.schemas.enquiry import EnquiryCreate
from app.services.background_tasks import process_enquiry
from fastapi import HTTPException
from app.schemas.enquiry import EscalateRequest
from app.schemas.enquiry import FollowUpRequest
from app.logger.logger import logger

router = APIRouter(
    prefix="/enquiry",
    tags=["Enquiry"]
)


@router.post("/")
def create_enquiry(
    enquiry: EnquiryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    new_enquiry = Enquiry(
        customer_name=enquiry.customer_name,
        channel=enquiry.channel,
        message=enquiry.message,
        status="processing"
    )

    db.add(new_enquiry)
    db.commit()
    db.refresh(new_enquiry)
    logger.info(
    "enquiry_created",
    extra={
        "enquiry_id": new_enquiry.id,
        "customer_name": new_enquiry.customer_name,
        "channel": new_enquiry.channel
    }
    )

    event = Event(
        enquiry_id=new_enquiry.id,
        event_type="ENQUIRY_CREATED",
        details="New enquiry received"
    )

    db.add(event)
    db.commit()

    background_tasks.add_task(
        process_enquiry,
        new_enquiry.id
    )

    return {
        "enquiry_id": new_enquiry.id,
        "status": "processing"
    }

@router.get("/{id}")
def get_enquiry(
    id: int,
    db: Session = Depends(get_db)
):
    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found"
        )

    return enquiry

@router.post("/{id}/escalate")
def escalate_enquiry(
    id: int,
    request: EscalateRequest,
    db: Session = Depends(get_db)
):
    
    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found"
        )

    enquiry.status = "escalated"

    event = Event(
        enquiry_id=id,
        event_type="ESCALATED",
        details=request.reason
    )

    db.add(event)
    db.commit()
    db.refresh(enquiry)

    logger.info(
    "manual_escalation",
    extra={
        "enquiry_id": id,
        "reason": request.reason
    }
    )

    return {
        "enquiry_id": id,
        "status": "escalated",
        "reason": request.reason
    }

@router.get("/{id}/history")
def get_history(
    id: int,
    db: Session = Depends(get_db)
):

    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found"
        )

    events = (
        db.query(Event)
        .filter(Event.enquiry_id == id)
        .order_by(Event.created_at)
        .all()
    )

    timeline = []

    for event in events:
        timeline.append({
            "event_type": event.event_type,
            "details": event.details,
            "timestamp": event.created_at
        })

    return {
        "enquiry_id": enquiry.id,
        "customer_name": enquiry.customer_name,
        "channel": enquiry.channel,
        "message": enquiry.message,
        "status": enquiry.status,
        "matched_sop": enquiry.matched_sop,
        "suggested_response": enquiry.suggested_response,
        "timeline": timeline
    }

@router.post("/{id}/follow-up")
def schedule_follow_up(
    id: int,
    request: FollowUpRequest,
    db: Session = Depends(get_db)
):

    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found"
        )

    event = Event(
        enquiry_id=id,
        event_type="FOLLOWUP_SCHEDULED",
        details=f"Delay: {request.delay_minutes} minutes | Message: {request.message_template}"
    )

    db.add(event)
    db.commit()

    logger.info(
    "followup_scheduled",
    extra={
        "enquiry_id": id,
        "delay_minutes": request.delay_minutes
    }
    )

    return {
        "enquiry_id": id,
        "message": "Follow-up scheduled",
        "delay_minutes": request.delay_minutes,
        "template": request.message_template
    }

