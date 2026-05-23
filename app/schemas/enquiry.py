from pydantic import BaseModel, Field
from typing import Optional


class EnquiryCreate(BaseModel):
    customer_name: str = Field(
        ...,
        example="John Doe"
    )

    channel: str = Field(
        ...,
        example="whatsapp"
    )

    message: str = Field(
        ...,
        example="What are your pricing plans?"
    )


class FollowUpRequest(BaseModel):
    delay_minutes: int = Field(
        ...,
        gt=0,
        example=30
    )

    message_template: str | None = Field(
        None,
        example="Checking if you still need assistance."
    )

class EscalateRequest(BaseModel):
    reason: str = Field(
        ...,
        example="Customer requested human support"
    )