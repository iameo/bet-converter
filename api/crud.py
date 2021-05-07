# from sqlalchemy.orm import Session, session

from api import models, schema

from api.db import bookingslips, database



###########################BOOKING SLIP#####################################

async def add_slip(source='', destination='', booking_code='', new_bookingcode=''):
    query = bookingslips.insert().values(source=source, destination=destination, booking_code=booking_code, new_bookingcode=new_bookingcode)
    return await database.execute(query=query)

async def get_slip(booking_code):
    query = bookingslips.select(bookingslips.c.booking_code==booking_code)
    return await database.fetch_one(query=query)

async def get_slip_detail(source, destination, booking_code):
    query = bookingslips.select().where(bookingslips.c.source==source).where(bookingslips.c.destination==destination).where(bookingslips.c.booking_code==booking_code)
    return await database.fetch_one(query=query)

async def get_slips():
    query = bookingslips.select()
    return await database.fetch_all(query=query)

async def delete_slip(id: int):
    query = bookingslips.delete().where(bookingslips.c.id==id)
    return await database.execute(query=query)

async def update_slip(id: int, payload: schema.BookingSlipCreate): #I can't think of a possible usecase for now
    query = (
        bookingslips
        .update()
        .where(bookingslips.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)



###########################BOOKING SLIP#####################################

# async def get_slips(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.BookingSlip).offset(skip).limit(limit).all()

# async def get_slip(booking_code: str):
#     query = models.BookingSlip.filter(models.BookingSlip.booking_code == booking_code).first()
#     return await database.execute(query=query)
# async def get_slip_detail(db: Session, booking_code: str, source: str, destination: str):
#     return db.query(models.BookingSlip).filter(models.BookingSlip.booking_code == booking_code)\
#         .filter(models.BookingSlip.source == source).filter(models.BookingSlip.destination == destination).first()

# async def create_slip(db: Session, source='', destination='', booking_code='', new_bookingcode=''):
#     db_slip = models.BookingSlip(source=source, destination=destination, booking_code=booking_code, new_bookingcode=new_bookingcode)
#     db.add(db_slip)
#     db.commit()
#     db.refresh(db_slip)
#     return db_slip
  
# async def create_slip_convert(db: Session, _convert: schema.ConvertedSlipCreate, bookingslip_id: int):
#     db_convert = models.ConvertedSlip(**_convert.dict(), booking_slip_id=bookingslip_id)
#     db.add(db_convert)
#     db.commit()
#     db.refresh(db_convert)
#     return db_convert

