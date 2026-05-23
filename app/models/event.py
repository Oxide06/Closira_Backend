from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from app.database.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    enquiry_id = Column(
        Integer,
        ForeignKey("enquiries.id")
    )

    event_type = Column(String, nullable=False)
    details = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )