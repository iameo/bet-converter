import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse


import requests
from selenium.webdriver.support import ui

from selenium import webdriver
from sqlalchemy.orm import Session
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from .. import crud, models, schema
from ..database import engine, SessionLocal
from ..betsource import BetSources, link_bet9ja, link_sportybet, link_1xbet, link_msport
from ..worker import Bet9ja, SportyBet, X1Bet, MSport

import re


from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Path
import json

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

models.Base.metadata.create_all(bind=engine)


slip_view = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@slip_view.post("/slips/", response_model=schema.BookingSlip)
def create_slip(
    _code: schema.BookingSlipCreate, db: Session = Depends(get_db)
):
    _slip = crud.get_slip(db, code=_code.code)
    if _slip:
        raise HTTPException(status_code=400, detail="booking code exists!")
    return crud.create_slip(db=db, _code=_code)


@slip_view.get("/slips/{booking_code}", response_model=schema.BookingSlipOut)
def get_slip_by_code(booking_code: str, db: Session = Depends(get_db)):
    slip = crud.get_slip(db, code=booking_code)
    if slip is None:
        raise HTTPException(status_code=404, detail="booking slip not found!")
    return slip


@slip_view.get("/slips/convert/")
async def get_converted_slip(booking_code: str, source: BetSources, destination: BetSources, db: Session = Depends(get_db)):
    # check slip is valid against source, goto source, extract, "store", go to dest, input, book, return booking code

    matches_extract = []
    slip_code = ''

    if source == BetSources.bet9ja:
        selections = Bet9ja(source=source, booking_code=booking_code, site=link_bet9ja).slip_extractor()

        if selections is not None:
            if destination == BetSources.bet9ja:
                __bet9ja = Bet9ja(source=source, site=link_bet9ja)
                slip_code = __bet9ja.injector('bet9ja', selections)

            if destination == BetSources.sportybet:
                pass

            if destination == BetSources.x1bet:
                __x1bet = X1Bet(source=source, site=link_1xbet)
                slip_code = __x1bet.injector('bet9ja', selections)

            if destination == BetSources.msport:
                __msport = MSport(source=source, site=link_msport)
                slip_code = __msport.injector('bet9ja', selections)

            return {"source": source, "destination": destination, "booking code": slip_code}
        else:
            return {"status": "failed"}

    elif source == BetSources.sportybet:
        selections = SportyBet(source=source, booking_code=booking_code, site=link_sportybet).slip_extractor()
        
        if destination == BetSources.bet9ja:
            _bet9ja = Bet9ja(source=source, site=link_bet9ja)
            slip_code = _bet9ja.injector('sportybet', selections)

        return {"source": source, "destination": destination, "booking code": slip_code}
        # matches_extract = matches.slip_extractor()
        # return {"source": matches.source, "booking code": matches.booking_code, "matches": matches_extract}
    
    elif source == BetSources.x1bet:
        matches = X1Bet(source=source, booking_code=booking_code, site=link_1xbet)
        selections = matches.slip_extractor()

        if selections is not None:
            if destination == BetSources.x1bet:
                __x1bet = X1Bet(source=source, site=link_1xbet)
                slip_code = __x1bet.injector('1xbet', selections)
            
        
            if destination == BetSources.bet9ja:
                __bet9ja = Bet9ja(source=source, site=link_bet9ja)
                slip_code = __bet9ja.injector('1xbet', selections)

            return {"source": source, "initial":booking_code, "destination": destination, "new code": slip_code}
        # for match in matches:
        #     fetch_team(match)
        else:
            return {"status": "failed"}
    
    elif source == BetSources.betway:
        pass



@slip_view.get("/slips/all/", response_model=List[schema.BookingSlipOut])
async def get_slips(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    slips = crud.get_slips(db, skip=skip, limit=limit)
    if slips is None:
        raise HTTPException(status_code=404, detail="No slip at this time!")
    return slips
