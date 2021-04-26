from typing import List, Optional
from pydantic import BaseModel, Field

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
    booking_code: Optional[str] = None
    destination: Optional[str] = None
    new_code: Optional[str] = None




class BookingSlipCreate(BookingSlipBase):
    pass


class BookingSlip(BookingSlipBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name =True
        schema_extra = {
            "example": {
                "source": "bet9ja",
                "booking_code": "3XVU9BA",
                "destination": "1xbet",
                "new_code": "ZY7D2",
            }
        }
        
class BookingSlipOut(BookingSlipBase):
    created_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "source": "bet9ja",
                "booking_code": "3XVU9BA",
                "destination": "1xbet",
                "new_code": "ZY7D2",
                "created_at": datetime.now()
            }
        }


def SuccessResponseModel(data, message):
    return {
        "data": [data],
        "message": message,
        "code": 200
    }


def ErrorResponseModel(error, message, code):
    return {
        "error": error,
        "message": message,
        "code": code
    }