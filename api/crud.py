from sqlalchemy.orm import Session, session

from . import models, schema

# def get_team(db: Session, team_name: str):
#     return db.query(models.MatchDetail).filter(models.MatchDetail.team == team_name).all()






###########################BOOKING SLIP#####################################

def get_slips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookingSlip).offset(skip).limit(limit).all()

def get_slip(db: Session, booking_code: str):
    return db.query(models.BookingSlip).filter(models.BookingSlip.booking_code == booking_code).first()

def get_slip_detail(db: Session, booking_code: str, source: str, destination: str):
    return db.query(models.BookingSlip).filter(models.BookingSlip.booking_code == booking_code)\
        .filter(models.BookingSlip.source == source).filter(models.BookingSlip.destination == destination).first()

def create_slip(db: Session, source='', destination='', booking_code='', new_bookingcode=''):
    db_slip = models.BookingSlip(source=source, destination=destination, booking_code=booking_code, new_bookingcode=new_bookingcode)
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

