from typing import List, Optional
from pydantic import BaseModel

from datetime import datetime


# class MatchDetailBase(BaseModel):
#     source: str

# class AnonUserCreate(MatchDetailBase):
#     pass

# class MatchDetail(MatchDetailBase):
#     team: str
#     time: str


class MatchDetailBase(BaseModel):
    source: Optional[str] = None


class MatchDetail(MatchDetailBase):
    league: str
    team: str
    datetime: str




############################BOOKING SLIP######################################

class BookingSlipBase(BaseModel):
    source: Optional[str] = None
    code: Optional[str] = None
    match: Optional[List] = []


class BookingSlipCreate(BookingSlipBase):
    pass


class BookingSlip(BookingSlipBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BookingSlipOut(BookingSlipBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


