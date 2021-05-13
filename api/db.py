import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, sql)
import sqlalchemy
from databases import Database
from datetime import datetime

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

DATABASE_URI = os.getenv('SQLAlCHEMY_DATABASE_URL')

metadata = sqlalchemy.MetaData()


bookingslips = Table(
    'bookingslips',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('source', String(100), index=True),
    Column('booking_code', String(50)),
    Column('destination', String(100)),
    Column('new_booking_code', String(50)),
    Column('created_at', DateTime(timezone=True), server_default=sql.func.now())
)

engine = sqlalchemy.create_engine(
    DATABASE_URI, connect_args={"check_same_thread": False}
)

database = Database(DATABASE_URI)