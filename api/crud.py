from sqlalchemy.orm import Session, session

from . import models, schema

# def get_team(db: Session, team_name: str):
#     return db.query(models.MatchDetail).filter(models.MatchDetail.team == team_name).all()






###########################BOOKING SLIP#####################################

def get_slips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookingSlip).offset(skip).limit(limit).all()

def get_slip(db: Session, booking_code: str):
    return db.query(models.BookingSlip).filter(models.BookingSlip.booking_code == booking_code).first()

def create_slip(db: Session, _code: schema.BookingSlipCreate):
    db_slip = models.BookingSlip(source = _code.source, booking_code = _code.booking_code, converted_slips = _code.converted_slips)
    db.add(db_slip)
    db.commit()
    db.refresh(db_slip)
    return db_slip

  
def create_slip_convert(db: Session, _convert: schema.ConvertedSlipCreate, bookingslip_id: int):
    db_convert = models.ConvertedSlip(**_convert.dict(), booking_slip_id=bookingslip_id)
    db.add(db_convert)
    db.commit()
    db.refresh(db_convert)
    return db_convert

