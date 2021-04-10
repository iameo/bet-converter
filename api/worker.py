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

stopwords = stopwords.words('english')

chrome_path = 'driver\\chromedriver.exe'


class MatchExtractor(object):
    def __init__(self, source: str = None, site: str = None, booking_code: str = None) -> None:
        self.source = source
        self.site = site
        self.booking_code = booking_code

    def connect(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, executable_path=chrome_path)
        driver.get(self.site)
        driver.implicitly_wait(1)
        return driver


    def extractor(self) -> List[str]:
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
    def extractor(self):
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


# class SportyBet(MatchExtractor):
#     def __init__(self, country):
#         super().__init__(country: str = None)
#         pass


class NairaBet(MatchExtractor):
    pass


class SportyBet(MatchExtractor):
    def extractor(self):
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
                

        

        
        
        

