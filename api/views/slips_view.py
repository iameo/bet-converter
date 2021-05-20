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
from ..betsource import BetSources, link_bet9ja, link_sportybet, link_1xbet, link_msport, link_22bet
from ..worker import Bet9ja, SportyBet, X1Bet, MSport, Bet22

import re


from typing import List
from fastapi import APIRouter, Path
import json

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


slip_view = APIRouter()


@slip_view.post("/slips/")
async def create_slip(
    _code: schema.BookingSlipBase
):
    _slip = await crud.get_slip(booking_code=_code.booking_code)
    if _slip:
        raise HTTPException(status_code=400, detail="booking code exists!")
    return await crud.add_slip(_code)


@slip_view.get("/slips/{booking_code}", response_model=schema.BookingSlipOut, summary="get bet slip by booking code")
async def get_slip_by_code(booking_code: str):
    """
    Get booking slip by booking code:

    -**booking code**: your generated booking code e.g Y5GSHW

    return:

    betting slips with the requested booking code otherwise a 404 error
    """
    slip = await crud.get_slip(booking_code=booking_code)
    if slip is None:
        raise HTTPException(status_code=404, detail="booking slip not found!")
    return slip

@slip_view.get("/slips/detail/{booking_code}", response_model=schema.BookingSlipOut, summary="get bet slip by details (booking code, source and destination)")
async def get_slip_by_detail(booking_code: str, source: str, destination: str):
    """
    Get booking slip by details(booking_code, source and destination)

    -**booking code**: booking slip code e.g Y5GSHW
    -**source**: site where the booking code is generated from
    -**destination**: site where the booking code is generated to
    """
    slip = await crud.get_slip_detail(booking_code=booking_code, source=source, destination=destination)
    if slip is None:
        raise HTTPException(status_code=404, detail="booking slip not found!")
    return slip


@slip_view.get("/slips/convert/", summary="convert bet slip")
async def get_converted_slip(booking_code: str, source: BetSources, destination: BetSources):
    """
    Convert bet slip from source to your destination site:

    - **booking code**: your generated booking code e.g Y5GSHW
    - **source**: the site booking code was (originally) generated
    - **destination**: the site you would like to convert the booking slip to
    - **NB**: Depending on both source and destination sites & number of games in bet slip, conversion could span from 40s to minutes
    """

    if len(booking_code) >= 4:
        slip = await crud.get_slip_detail(source, destination, booking_code)

        if slip:
            return slip
        
        matches_extract = []
        slip_code = ''

        if source == BetSources.bet9ja:
            selections = Bet9ja(source=source, booking_code=booking_code, site=link_bet9ja).slip_extractor()

            if selections is not None:
                if destination == BetSources.bet9ja:
                    __bet9ja = Bet9ja(source=source, site=link_bet9ja)
                    slip_code = __bet9ja.injector("bet9ja", selections)

                if destination == BetSources.sportybet:
                    pass

                if destination == BetSources.x1bet:
                    __x1bet = X1Bet(source=source, site=link_1xbet)
                    slip_code = __x1bet.injector('bet9ja', selections)

                if destination == BetSources.msport:
                    __msport = MSport(source=source, site=link_msport)
                    slip_code = __msport.injector('bet9ja', selections)
                
                if destination == BetSources.bet22:
                    __bet22 = Bet22(source=source, site=link_22bet)
                    slip_code = __bet22.injector('bet9ja', selections)

                if destination == BetSources.betway:
                    pass
                
                payload = {"source": source, "destination": destination, "booking_code": str(booking_code).upper(), "new_booking_code": str(slip_code).upper()}
                db_slip = await crud.add_slip(**payload)

                return schema.ResponseModel([payload, db_slip], status='SUCCESS', code='200')

            else:
                return schema.ResponseModel(None, status='FAILED', code='500')


        elif source == BetSources.sportybet:
            selections = SportyBet(source=source, booking_code=booking_code, site=link_sportybet).slip_extractor()
            
            if selections is not None:
                if destination == BetSources.bet9ja:
                    _bet9ja = Bet9ja(source=source, site=link_bet9ja)
                    slip_code = _bet9ja.injector('sportybet', selections)
                
                if destination == BetSources.x1bet:
                    __x1bet = X1Bet(source=source, site=link_1xbet)
                    slip_code = __x1bet.injector('sportybet', selections)

                if destination == BetSources.msport:
                    __msport = MSport(source=source, site=link_msport)
                    slip_code = __msport.injector('sportybet', selections)
                
                if destination == BetSources.bet22:
                    __bet22 = Bet22(source=source, site=link_22bet)
                    slip_code = __bet22.injector('sportybet', selections)
                
                if destination == BetSources.sportybet:
                    pass
                
                if destination == BetSources.betway:
                    pass

                payload = {"source": source, "destination": destination, "booking_code": str(booking_code).upper(), "new_booking_code": str(slip_code).upper()}
                db_slip = await crud.add_slip(**payload)

                return schema.ResponseModel([payload, db_slip], status='SUCCESS', code='200')

            else:
                return schema.ResponseModel(None, status='FAILED', code='500')

        elif source == BetSources.x1bet:
            selections = X1Bet(source=source, booking_code=booking_code, site=link_1xbet).slip_extractor()

            if selections is not None:
                if destination == BetSources.x1bet:
                    __x1bet = X1Bet(source=source, site=link_1xbet)
                    slip_code = __x1bet.injector('1xbet', selections)
            
                if destination == BetSources.bet9ja:
                    __bet9ja = Bet9ja(source=source, site=link_bet9ja)
                    slip_code = __bet9ja.injector('1xbet', selections)
                
                if destination == BetSources.msport:
                    __msport = MSport(source=source, site=link_msport)
                    slip_code = __msport.injector('1xbet', selections)
                
                if destination == BetSources.bet22:
                    __bet22 = Bet22(source=source, site=link_22bet)
                    slip_code = __bet22.injector('1xbet', selections)
                
                if destination == BetSources.sportybet:
                    pass
                
                if destination == BetSources.betway:
                    pass

                
                payload = {"source": source, "destination": destination, "booking_code": str(booking_code).upper(), "new_booking_code": str(slip_code).upper()}
                db_slip = await crud.add_slip(**payload)

                return schema.ResponseModel([payload, db_slip], status='SUCCESS', code='200')

            else:
                return schema.ResponseModel(None, status='FAILED', code='500')

        elif source == BetSources.betway:
            # selections = BetWay(source=source, booking_code=booking_code, site=link_1xbet).slip_extractor()
            selections = 'faux'

            if selections is not None:
                if destination == BetSources.x1bet:
                    __x1bet = X1Bet(source=source, site=link_1xbet)
                    slip_code = __x1bet.injector('betway', selections)
            
                if destination == BetSources.bet9ja:
                    __bet9ja = Bet9ja(source=source, site=link_bet9ja)
                    slip_code = __bet9ja.injector('betway', selections)
                
                if destination == BetSources.msport:
                    __msport = MSport(source=source, site=link_msport)
                    slip_code = __msport.injector('betway', selections)
                
                if destination == BetSources.bet22:
                    __bet22 = Bet22(source=source, site=link_22bet)
                    slip_code = __bet22.injector('betway', selections)
                
                if destination == BetSources.sportybet:
                    pass

                
                payload = {"source": source, "destination": destination, "booking_code": str(booking_code).upper(), "new_booking_code": str(slip_code).upper()}
                db_slip = await crud.add_slip(**payload)

                return schema.ResponseModel([payload, db_slip], status='SUCCESS', code='200')

            else:
                return schema.ResponseModel(None, status='FAILED', code='500')

        elif source == BetSources.bet22:
            selections = Bet22(source=source, booking_code=booking_code, site=link_22bet).slip_extractor()

            if selections is not None:
                if destination == BetSources.x1bet:
                    __x1bet = X1Bet(source=source, site=link_1xbet)
                    slip_code = __x1bet.injector(source, selections)
            
                if destination == BetSources.bet9ja:
                    __bet9ja = Bet9ja(source=source, site=link_bet9ja)
                    slip_code = __bet9ja.injector(source, selections)
                
                if destination == BetSources.msport:
                    __msport = MSport(source=source, site=link_msport)
                    slip_code = __msport.injector(source, selections)
                
                if destination == BetSources.betway:
                    pass

                if destination == BetSources.sportybet:
                    pass

                if destination == BetSources.bet22:
                    __bet22 = Bet22(source=source, site=link_22bet)
                    slip_code = __bet22.injector(source, selections)
            
                
                payload = {"source": source, "destination": destination, "booking_code": str(booking_code).upper(), "new_booking_code": str(slip_code).upper()}
                db_slip = await crud.add_slip(**payload)

                return schema.ResponseModel([payload, db_slip], status='SUCCESS', code='200')

            else:
                return schema.ResponseModel(None, status='FAILED', code='500')

        else:
            return schema.ErrorResponseModel("INVALID OPTION!", "CHECK YOUR SELECTED OPTIONS AND TRY AGAIN", 400)

    else:
        raise HTTPException(status_code=400, detail=f"booking code can not be less than 4 characters!")


@slip_view.get("/slips/", response_model=List[schema.BookingSlipOut])
async def get_slips(skip: int = 0, limit: int = 10):
    slips = await crud.get_slips(skip=skip, limit=limit)
    if slips is None:
        raise HTTPException(status_code=404, detail="No slip at this time!")
    return slips