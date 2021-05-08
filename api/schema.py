from typing import List, Optional
from pydantic import BaseModel, Field

from datetime import datetime



class MatchDetailBase(BaseModel):
    source: Optional[str] = None


class MatchDetail(MatchDetailBase):
    league: str
    team: str
    datetime: str




############################BOOKING SLIP######################################

class BookingSlipBase(BaseModel):
    booking_code: str
    source: str
    destination: str
    new_bookingcode: Optional[str] = None


class BookingSlipCreate(BookingSlipBase):
    pass


class BookingSlip(BookingSlipBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id":3,
                "source": "bet9ja",
                "booking_code": "3XVU9BA",
                "destination": "x1bet",
                "new_bookingcode": "CJXPY",
                "created_at": "2021-04-27T04:44:11",
            }
        }




class BookingSlipOut(BookingSlipBase):
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "booking_code": "3D9FXWQ",
                "created_at": "2021-05-06T23:37:10",
                "destination": "x1bet",
                "source": "bet9ja",
                "new_bookingcode": "ABYPY",
            }
        }


# class SlipMixin(BaseModel):
#     id: int


# class BookingSlipCreated(SlipMixin, BookingSlipBase):
#     source: str
#     booking_code: str
#     destination: str
#     new_bookingcode: str


##################### RESPONSE #####################################

def SuccessResponseModel(data=[resp, id], message='SUCCESS', code=200):
    return {
        "data": data,
        "message": message,
        "code": code
    }


def ErrorResponseModel(error, message, code):
    return {
        "error": error,
        "message": message,
        "code": code
    }