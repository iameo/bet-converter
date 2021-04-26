from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func

from datetime import datetime
# from sqlalchemy import pickleType

from .database import Base



class BookingSlip(Base):
    __tablename__ = "bookingslips"
      
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    booking_code = Column(String, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    converted_slips = relationship("ConvertedSlip", back_populates="booking_slip")

    def __repr__(self):
        # return f'from {self.source}({self.booking_code}) -> {self.destination}({self.new_booking_code})'
        return f'from {self.source}({self.booking_code})'


class ConvertedSlip(Base):
    __tablename__ = "convertedslips"
    
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True)
    new_booking_code = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking_slip_id = Column(Integer, ForeignKey("bookingslips.id"))

    booking_slip = relationship("BookingSlip", back_populates="converted_slips")

