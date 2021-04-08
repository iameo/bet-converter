from sqlalchemy.orm import Session, session

from . import models, schema

# def get_team(db: Session, team_name: str):
#     return db.query(models.MatchDetail).filter(models.MatchDetail.team == team_name).all()






###########################BOOKING SLIP#####################################

def get_slips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookingSlip).offset(skip).limit(limit).all()

def get_slip(db: Session, code: str):
    return db.query(models.BookingSlip).filter(models.BookingSlip.code == code).first()

def create_slip(db: Session, _code: schema.BookingSlipCreate):
    db_slip = models.BookingSlip(source = _code.source, code = _code.code, match = _code.match)
    db.add(db_slip)
    db.commit()
    db.refresh(db_slip)
    return db_slip

  


# def get_postits(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.PostIT).offset(skip).limit(limit).all()

# def create_anon_postit(db: Session, postit: schema.PostITCreate, anon_id: int):
#     db_postit = models.PostIT(**postit.dict(), anon_id=anon_id)
#     db.add(db_postit)
#     db.commit()
#     db.refresh(db_postit)
#     return db_postit



    #get match by tag
    #get ma