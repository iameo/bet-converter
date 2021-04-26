from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func

from datetime import datetime
# from sqlalchemy import pickleType

from .database import Base

class MatchDetail(Base):
    __tablename__ = "matchdetails"

    id = Column(Integer, primary_key=True, index=True)
    team = Column(String, index=True)
    time = Column(String, index=True)

    def __repr__(self):
        return self.team
  

class BookingSlip(Base):
    __tablename__ = "bookingslips"
      
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    booking_code = Column(String, index=True)
    destination = Column(String, index=True)
    new_booking_code = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Bet Code: ' + self.code + '>'
