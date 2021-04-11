import os

import requests
from selenium.webdriver.support import ui

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from typing import List

import string

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

import re

import time
from abc import ABC, abstractmethod

stopwords = stopwords.words('english')

chrome_path = 'driver\\chromedriver.exe'


class MatchExtractor(ABC):
    def __init__(self, source: str = None, site: str = None, booking_code: str = None) -> None:
        self.source = source
        self.site = site
        self.booking_code = booking_code

    def connect(self, wait_time=1):
        options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--no-sandbox')

        # comment out in local production - fix to this is already on local, I shall push soon
        options.binary_location = os.getenv("GOOGLE_CHROME_PATH")


        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, executable_path=chrome_path)
        driver.get(self.site)
        driver.implicitly_wait(wait_time)
        return driver

    @abstractmethod
    def games_extractor(self, team) -> List[str]:
        pass

    @abstractmethod
    def slip_extractor(self) -> List[str]:
        pass

    def injector(self) -> str:
        pass

    def clean_string(self, sentence) -> str:
        sentence = ''.join([word for word in sentence if word not in string.punctuation])
        sentence = sentence.lower()
        text = ' '.join([word for word in sentence.split() if word not in stopwords])
        return text

    def check_similarity(self, relations):
        cleaned = list(map(self.clean_string, relations))
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()

        csim = cosine_similarity(vectors[0].reshape(1, -1), vectors[1].reshape(1, -1))

        return csim

    def bet_cleanser(self, bet):
        if 'btts yes' in bet:
            return 'btts yes'




class Bet9ja(MatchExtractor):
    def games_extractor(self, team):
        driver = self.connect()
        # driver = webdriver.Chrome(chrome_options=options, executable_path=os.getenv("CHROMEDRIVER_PATH_LOCAL", "/app/.chromedriver/bin/chromedriver"))
        # driver.get("https://web.bet9ja.com/Sport/Default.aspx")
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
            league = match_team.split("\n")[0]
            match = re.findall(r"\(.*?\)", match_team)
            # print(match)
            if not match and "simulated" not in league.lower() and "-zoom" not in league.lower() \
                and "cyber live" not in league.lower() and "first goal" not in league.lower() and "match stats" not in league.lower() and "team to score " not in league.lower():
                matches.append({"source": page_title, "league": str(league), "team": match_team.split("\n")[1], "datetime": str(match_time)})
        return matches
        

    def slip_extractor(self):
        driver = self.connect()

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
            match = driver.find_elements_by_xpath('//*[@id="h_w_PC_cCoupon_divCouponIns"]/div[1]')
        except Exception as e:
            print(">>>>>", str(e))
        
        # self.matches = []
        # for meh in match:
        #     print(">", meh.text)
        # print("//:", match)
        match = match.split("\n") 
        # print(match)
        access = [1,2,5,6]
        map_access = map(match.__getitem__, access)
        accessed_data = list(map_access)
        print(match)
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


class NairaBet(MatchExtractor):
    pass


class SportyBet(MatchExtractor):
    # def __init__(self, country):
    #     super().__init__(country)
    #     pass

    def games_extractor(self, team):
        pass

    def slip_extractor(self):
        driver = self.connect()
        
        # try: #select country
        #     elem = driver.find_element_by_xpath('//*[@id="j_betslip"]/div[2]/div[1]/div/div[1]/div[1]/span[1]')
        # except NoSuchElementException:
        #     print(">>>")
        try:
            elem = driver.find_element_by_xpath('//*[@id="j_betslip"]/div[2]/div[1]/div/div[2]/span/input')
        except NoSuchElementException as e:
            print(">>>>>>>", str(e))

        elem.send_keys(self.booking_code)
        load = driver.find_element_by_xpath('//*[@id="j_betslip"]/div[2]/div[1]/div/button').click()
        table = driver.find_element_by_class_name("m-list")
        rows = table.find_elements(By.CLASS_NAME, "m-lay-mid")
        selection = []
        for row in rows[::2]: #duplicated in twos so get all even index([0,1,2,3] -> [1,3])
            line = row.text.split('\n')
            line[1] = line[1].split("|")[1].lstrip().replace(' v ',' - ')  #hacky
            access = [0,1,2]
            map_access = map(line.__getitem__, access)
            selection.append(list(map_access))
        return selection
            #{"bet": "Home", "team": "team A - team B", "bet mode": "1X2"}
        #     selection = {"bet": line[0], "team": line[1].split("|")[1].lstrip().replace(' v ',' - '), "bet mode": line[2]}
        # return selection



class X1Bet(MatchExtractor):
    def games_extractor(self, team):
        pass

    def slip_extractor(self):
        pass

    def injector(self, match_detail, match, bet: str = None, bet_selection: str = None):
        driver = self.connect()

        notification = driver.find_element_by_xpath('//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
        if notification:
            notification.click()
        try:
            elem = driver.find_element_by_xpath('//*[@id="hottest_games"]/div/div[1]/div/div/div/div/div[2]/div/div[1]/input')
        except NoSuchElementException as e:
            print(str(e))
        
        elem.send_keys(match_detail)

        try:
            elem = driver.find_element_by_xpath('//*[@id="hottest_games"]/div/div[1]/div/div/div/div/div[2]/div/div[1]/button').click()
        except NoSuchElementException as e:
            print(str(e))

        try:
            table = driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[3]/div/section')
        except NoSuchElementException as e:
            print(str(e))

        rows = table.find_elements(By.CLASS_NAME, "search-popup-events__item")
        # for row in rows:
        #     if 'LIVE' not in row.text:
        #         p_match = row.text.split("\n")
        p_match = [_match.split("\n") for _match in rows if "LIVE" not in row.text]
        # p_match = self.clean_string(p_match[0])
        for game in p_match:
            relations = [game, match]
            
            csim = self.check_similarity(relations)
            if csim >= .85:
                select = driver.find_element_by_partial_link_text(game[2].title()).click()
                
                windows = driver.window_handles
                driver.switch_to.window(windows[1])

                if bet_selection == 'btts yes':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[2]/div/div[2]/div[1]/span[1]').click()
                    driver.switch_to_window(windows[0])
                    driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[1]/i').click()
                elif bet_selection =='btts no':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[2]/div/div[2]/div[2]/span[1]').click()
                elif bet_selection == "home win":
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[1]/div/div[2]/div[1]/span[2]').click()
                elif bet_selection == 'draw':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[1]/div/div[2]/div[2]/span[2]').click()
                elif bet_selection == 'away win':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[1]/div/div[2]/div[3]/span[2]').click()
                elif bet_selection == 'dc 1x':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[2]/div[1]/div/div[2]/div[1]/span[2]').click()
                elif bet_selection == 'dc 12':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[2]/div[1]/div/div[2]/div[2]/span[2]').click()
                elif bet_selection == 'dc 2x':
                    driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[2]/div[1]/div/div[2]/div[3]/span[2]').click()
                

  
class MSport(MatchExtractor):
    def games_extractor(self, team):
        driver = self.connect(wait_time=3)
        page_title = driver.title
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/a[2]').click() or driver.find_element_by_class_name('m-pop-close-btn').click()
        # if notification is not None:
        #     notification.click()
        try:
            driver.find_element_by_class_name('m-az-btn').click()
        except NoSuchElementException as e:
            print(str(e))
        

        try:
            driver.find_element_by_xpath('/html/body/div[1]/header/div[4]/div[2]/div[2]/div[1]/a').click()
        except Exception as e:
            print(str(e))

        # time.sleep(1)

        try:
            elem = driver.find_element_by_xpath('/html/body/div/div[1]/form/div/input')
        except Exception as e:
            print(str(e))

        elem.send_keys(team)
        time.sleep(2)

        try:
            driver.find_element_by_xpath('/html/body/div/div[1]/div[2]').click()
        except NoSuchElementException:
            pass

        try:
            tb = driver.find_element_by_class_name('m-search-main')
        except Exception:
            pass

        try:
            sections = tb.find_elements_by_class_name("m-result-section")
        except Exception:
            pass
        
        matches = []
        for section in sections:
            if section.text.split('\n')[0].lower() == "not start":
        #         print(section.text.split("\n")[1:-1])
                games = section.find_elements_by_class_name("m-resultItem")
                for game in games:
                    if "simulated" not in game.text.lower() and "esports" not in game.text.lower() and "cyber live" not in game.text.lower() and "electronic league" not in game.text.lower():
                        _game = game.text.split("\n")
                        matches.append({
                            "source": page_title,
                            "datetime": _game[0],
                            "league": _game[1],
                            "team": ' '.join([a_ for a_ in _game[2:5]]).replace('vs','-')}
                            )    
        return matches

    def slip_extractor(self):
        pass


        

        
        

