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

from . import crud, models, schema
from .database import engine, SessionLocal
from .betsource import BetSources
from .worker import Bet9ja

import re


from typing import List
from pydantic import BaseModel



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BET CONVERTER")



GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = 'driver\\chromedriver.exe' or '/app/.chromedriver/bin/chromedriver'


#db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





############################ROUTES##########################################

@app.get("/")
def index():
    return RedirectResponse("/docs")

@app.get("/sources/")
def supported_sources():
    return [{"supported sources": BetSources.list()}]


@app.post("/slips/", response_model=schema.BookingSlip)
def create_slip(
    _code: schema.BookingSlipCreate, db: Session = Depends(get_db)
):
    _slip = crud.get_slip(db, code=_code.code)
    if _slip:
        raise HTTPException(status_code=400, detail="booking code exists!")
    return crud.create_slip(db=db, _code=_code)


@app.get("/slips/{booking_code}", response_model=schema.BookingSlipOut)
def get_slip_by_code(booking_code: str, db: Session = Depends(get_db)):
    slip = crud.get_slip(db, code=booking_code)
    if slip is None:
        raise HTTPException(status_code=404, detail="booking slip not found!")
    return slip


@app.get("/slips/convert/{booking_code}") #incomplete!!!!
async def get_converted_slip(source: BetSources, destination: BetSources, booking_code: str, db: Session = Depends(get_db)):
    # check slip is valid against source, goto source, extract, "store", go to dest, input, book, return booking code
    if source == BetSources.bet9ja:
        matches = Bet9ja(source=source, booking_code=booking_code)
        matches_extract = matches.extractor()
        return {"source": matches.source, "booking code": matches.booking_code, "matches": matches_extract}
        # for match in matches:
        #     fetch_team(match)



@app.get("/slips/", response_model=List[schema.BookingSlipOut])
def get_slips(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    slips = crud.get_slips(db, skip=skip, limit=limit)
    print(slips)
    if slips is None:
        raise HTTPException(status_code=404, detail="No slip at this time!")
    return slips


@app.get("/matches/{team}", response_model=List[schema.MatchDetail])
def fetch_team(team: str):
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--no-sandbox')

    # comment out in local production - fix to this is already on local, I shall push soon
    options.binary_location = GOOGLE_CHROME_PATH

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    global driver
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROMEDRIVER_PATH)
    driver.get("https://web.bet9ja.com/Sport/Default.aspx")
    driver.implicitly_wait(1)
    try:
        elem = driver.find_element_by_xpath('//*[@id="h_w_PC_oddsSearch_txtSearch"]')
    except Exception as e:
        print(">>>>>>", str(e))
    # else:
    #     elem = driver.find_element_by_xpath('//*[@id="s_w_PC_oddsSearch_txtSearch"]')
    elem.send_keys(team)

    try:
        submit = driver.find_element_by_xpath('//*[@id="h_w_PC_oddsSearch_btnCerca"]').click()
    except Exception as e:
        print(">>>>>>", str(e))  #terrible I know! debugging 
    # else:
    #     submit = driver.find_element_by_xpath('//*[@id="s_w_PC_oddsSearch_btnCerca"]').click()

    # try:
    #     tb = driver.find_element_by_xpath('//*[@id="h_w_PC_PC_gridSottoEventi"]') 
    # except Exception as e:
    #     print(">>>>>>", str(e))
    # # else:
        # tb = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]')

    page_title = driver.title


    try:
        rows = driver.find_element_by_xpath('//*[@id="h_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:]
    except NoSuchElementException:
        rows = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:] #**barffs**

    matches = []

    for row in rows:
        col = row.find_elements(By.TAG_NAME, "td")[0:]
        match_team = str(col[0].text)
        match_time = str(col[1].text)
        match = re.findall(r"\(.*?\)", match_team)
        if not match and "simulated" not in match_team.lower() and "-zoom" not in match_team.lower() \
            and "cyber live" not in match_team.lower() and "first goal" not in match_team.lower() and "match stats" not in match_team.lower() and "team to score " not in match_team.lower():
            matches.append({"source": page_title, "team": match_team, "time": match_time})
            # return {"Team": match_team, "Time": match_time}
        
    return matches



@app.post("/matches/")
def create_match_selection(team: str = None):
    get_team = fetch_team(team)
    print(">>>>>>>>>>", get_team)
    elem = driver.find_element_by_xpath('//*[@id="h_w_PC_PC_gridSottoEventi"]/tbody/tr[4]/td[1]/a').click()
    return {"elem":get_team}
# //*[@id="s_w_PC_PC_gridSottoEventi"]/tbody/tr[4]/td[1]/a