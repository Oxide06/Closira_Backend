from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database.database import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    status = Column(String, default="processing")

    matched_sop = Column(String, nullable=True)
    suggested_response = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )