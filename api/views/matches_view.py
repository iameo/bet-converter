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

# models.Base.metadata.create_all(bind=engine)


match_view = APIRouter()



@match_view.get("/matches/{team}", response_model=List[schema.MatchDetail])
def fetch_team(team: str, source: BetSources):
    if source == BetSources.bet9ja:
    # options = webdriver.ChromeOptions()

    # options.add_argument("--headless")
    # options.add_argument('--disable-gpu')
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument('--no-sandbox')

        games_by_team = Bet9ja(source="bet9ja", site=link_bet9ja).games_extractor(team)
        return games_by_team
    
    if source == BetSources.msport:
        games_by_team = MSport(source="msport", site=link_msport).games_extractor(team)
        return games_by_team
    # comment out in local production - fix to this is already on local, I shall push soon
    # options.binary_location = os.getenv("GOOGLE_CHROME_PATH")

    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # global driver
    # driver = webdriver.Chrome(chrome_options=options, executable_path=os.getenv("CHROMEDRIVER_PATH_LOCAL", "/app/.chromedriver/bin/chromedriver"))
    # driver.get("https://web.bet9ja.com/Sport/Default.aspx")
    # driver.implicitly_wait(1)
    # try:
    #     elem = driver.find_element_by_xpath('//*[@id="h_w_PC_oddsSearch_txtSearch"]')
    # except Exception as e:
    #     print(">>>>>>", str(e))
    # # else:
    # #     elem = driver.find_element_by_xpath('//*[@id="s_w_PC_oddsSearch_txtSearch"]')
    # elem.send_keys(team)

    # try:
    #     submit = driver.find_element_by_xpath('//*[@id="h_w_PC_oddsSearch_btnCerca"]').click()
    # except Exception as e:
    #     print(">>>>>>", str(e))  #terrible I know! debugging 
    # # else:
    # #     submit = driver.find_element_by_xpath('//*[@id="s_w_PC_oddsSearch_btnCerca"]').click()

    # # try:
    # #     tb = driver.find_element_by_xpath('//*[@id="h_w_PC_PC_gridSottoEventi"]') 
    # # except Exception as e:
    # #     print(">>>>>>", str(e))
    # # # else:
    #     # tb = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]')

    # page_title = driver.title


    # try:
    #     rows = driver.find_element_by_xpath('//*[@id="h_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:]
    # except NoSuchElementException:
    #     rows = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:] #**barffs**

    # matches = []

    # for row in rows:
    #     col = row.find_elements(By.TAG_NAME, "td")[0:]
    #     match_team = str(col[0].text)
    #     match_time = str(col[1].text)
    #     league = match_team.split("\n")[0]
    #     print(match_team)
    #     match = re.findall(r"\(.*?\)", match_team)
    #     print(match)
    #     if not match and "simulated" not in league.lower() and "-zoom" not in league.lower() \
    #         and "cyber live" not in league.lower() and "first goal" not in league.lower() and "match stats" not in league.lower() and "team to score " not in league.lower():
    #         matches.append({"source": page_title, "league": league, "team": match_team.split("\n")[1], "datetime": match_time})
    #         # return {"Team": match_team, "Time": match_time}
        
    # return matches



@match_view.post("/matches/")
def create_match_selection(team: str = None):
    get_team = fetch_team(team)
    print(">>>>>>>>>>", get_team)
    elem = driver.find_element_by_xpath('//*[@id="h_w_PC_PC_gridSottoEventi"]/tbody/tr[4]/td[1]/a').click()
    return {"elem":get_team}
# //*[@id="s_w_PC_PC_gridSottoEventi"]/tbody/tr[4]/td[1]/a