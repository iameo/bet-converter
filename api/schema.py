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
    booking_code: str = None

    
    # destination: Optional[str] = None
    # new_booking_code: Optional[str] = None

class ConvertedSlipBase(BaseModel):
    destination: Optional[str] = None







class ConvertedSlip(ConvertedSlipBase):
    id: int
    booking_slip_id: int
    new_booking_code: Optional[str] = None

    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class BookingSlipCreate(BookingSlipBase):
    source: Optional[str] = None

class ConvertedSlipCreate(BookingSlipCreate, ConvertedSlipBase):
    pass

class BookingSlip(BookingSlipBase):
    id: int
    converted_slips: List[ConvertedSlip] = [{}]
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name =True
        schema_extra = {
            "example": {
                "source": "bet9ja",
                "booking_code": "3XVU9BA",

            }
        }



# class BookingSlip(BookingSlipBase):
#     id: int
#     converted_slips: List[ConvertedSlip]

#     class Config:
#         orm_mode = True



class BookingSlipOut(BookingSlipBase, ConvertedSlipBase):
    created_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "source": "bet9ja",
                "booking_code": "3XVU9BA",
                "converts": [
                    {"destination": "1xbet",
                    "new_booking_code": "ZY7D2",
                    "created_at": datetime.now(),
                    "id": 2,
                    "booking_slip_id": 1}
                ],
                "created_at": datetime.now()
            }
        }





##################### RESPONSE #####################################

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