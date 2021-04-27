from typing import List, Optional
from pydantic import BaseModel, Field

from datetime import datetime


# class MatchDetailBase(BaseModel):
#     source: str



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
    booking_code: str
    source: str
    destination: str
    new_bookingcode: str


class ConvertedSlipBase(BaseModel):
    destination: Optional[str] = None







class ConvertedSlip(ConvertedSlipBase):
    id: int
    booking_slip_id: int

    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class BookingSlipCreate(BookingSlipBase):
    pass


class ConvertedSlipCreate(BookingSlipCreate, ConvertedSlipBase):
    pass

class BookingSlip(BookingSlipBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name =True
        schema_extra = {
            "example": {
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
                "created_at": datetime.now(),
                "destination": "x1bet",
                "source": "bet9ja",
                "new_bookingcode": "ABYPY",
            }
        }





##################### RESPONSE #####################################

def SuccessResponseModel(data, message, code=200):
    return {
        "data": [data],
        "message": message,
        "code": code
    }


def ErrorResponseModel(error, message, code):
    return {
        "error": error,
        "message": message,
        "code": code
    }