from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import requests
from selenium.webdriver.support import ui

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

from . import crud, models, schema
from .database import engine, SessionLocal

import re


from typing import List
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BET CONVERTER")


chrome_path = 'C:\\Users\\okwud\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe'


#db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




############################ROUTES##########################################

@app.get("/b/")
def index():
    return [{"Hello": "There"}]


@app.post("/slips/", response_model=schema.BookingSlip)
def create_slip(
    _code: schema.BookingSlipCreate, db: Session = Depends(get_db)
):
    _slip = crud.get_slip(db, code=_code.code)
    if _slip:
        raise HTTPException(status_code=400, detail="code exists!")
    return crud.create_slip(db=db, _code=_code)


@app.get("/slips/{booking_code}", response_model=schema.BookingSlipOut)
def get_slip_by_code(booking_code: str, db: Session = Depends(get_db)):
    slip = crud.get_slip(db, code=booking_code)
    if slip is None:
        raise HTTPException(status_code=404, detail="booking slip not found!")
    return slip


@app.get("/matches/{team}", response_model=List[schema.MatchDetail])
async def fetch_team(team: str):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=chrome_path)
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
    except ElementNotInteractableException:
        rows = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:] #**barffs**

    matches = []

    for row in rows:
        col = row.find_elements(By.TAG_NAME, "td")[0:]
        match_team = str(col[0].text)
        match_time = str(col[1].text)
        match = re.findall(r"\(.*?\)", match_team)
        if not match and "simulated" not in match_team.lower() and "-zoom" not in match_team.lower():
            matches.append({"source": page_title, "team": match_team, "time": match_time})
            # return {"Team": match_team, "Time": match_time}
        
    return matches
