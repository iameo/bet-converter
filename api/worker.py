import requests
from selenium.webdriver.support import ui

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from typing import List

chrome_path = 'driver\\chromedriver.exe'


class MatchExtractor(object):
    def __init__(self, source: str = None, booking_code: str = None) -> None:
        self.source = source
        self.booking_code = booking_code

    def extractor(self) -> List[str]:
        pass

    def injector(self) -> str:
        pass


class Bet9ja(MatchExtractor):
    def extractor(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, executable_path=chrome_path)
        driver.get("https://web.bet9ja.com/Sport/Default.aspx")
        driver.implicitly_wait(1)

        # elem = driver.find_element_by_xpath('//*[@id="toast-b2892900-126b-454e-9e82-65f4ee3622fc"]/div/div/div/div[2]/div/p[2]/a').click()
        try:
            elem = driver.find_element_by_xpath('//*[@id="h_w_PC_cCoupon_txtPrenotatore"]')
        except Exception as e:
            print(">>>>>>", str(e))
        # else:
        #     elem = driver.find_element_by_xpath('//*[@id="s_w_PC_oddsSearch_txtSearch"]')
        elem.send_keys(self.booking_code)

        try:
            load = driver.find_element_by_xpath('//*[@id="h_w_PC_cCoupon_lnkLoadPrenotazione"]').click()
        except Exception as e:
            print(">>>>>>", str(e)) 

        try:
            stat = driver.find_element_by_xpath('//*[@id="h_w_PC_cCoupon_mexPrenotazione"]/font/b')
        except NoSuchElementException:
            rows = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:] #**barffs**

        if 'not found' in stat.text:
            return {"status": "booking code has expired or invalid!"}
        

        try:
            match = driver.find_element_by_xpath('//*[@id="h_w_PC_cCoupon_divCouponIns"]/div[1]').text
        except Exception as e:
            print(">>>>>", str(e))
        
        # self.matches = []

        match = match.split("\n") 
        access = [1,2,5,6]
        map_access = map(match.__getitem__, access)
        accessed_data = list(map_access)
        return accessed_data

        # for match_game in str(match).split('\n'):

        #     if '-' in item or ' ' in item: #teamA - teamB or/and '1 1X2'(I shall improve on this)
        #         matches.append(match_game)
        # return self.matches



    # def injector(self, matches):
    #     self.matches = matches
    #     for match in self.matches:
            #search
            #select match and odd





class Betway(MatchExtractor):
    pass


# class SportyBet(MatchExtractor):
#     def __init__(self, country):
#         super().__init__(country: str = None)
#         pass


class NairaBet(MatchExtractor):
    pass