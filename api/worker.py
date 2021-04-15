import os

import requests
from selenium.webdriver.support import ui

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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

from .betsource import link_bet9ja, link_1xbet

stopwords = stopwords.words('english')

chrome_path = 'driver\\chromedriver.exe'


class MatchExtractor(ABC):
    def __init__(self, source: str = None, site: str = None, booking_code: str = None) -> None:
        self.source = source
        self.site = site
        self.booking_code = booking_code

    def connect(self, wait_time=1):
        options = webdriver.ChromeOptions()

        # options.add_argument("--headless")
        # options.add_argument('--disable-gpu')
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument('--no-sandbox')

        # comment out in local production - fix to this is already on local, I shall push soon
        # options.binary_location = os.getenv("GOOGLE_CHROME_PATH")


        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_path)
        driver.maximize_window()
        driver.get(self.site)
        driver.implicitly_wait(wait_time)
        return driver


    @abstractmethod
    def games_extractor(self, team, driver) -> List[str]:
        pass


    @abstractmethod
    def slip_extractor(self) -> List[str]:
        pass


    def injector(self, source, seletions) -> str:
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

    # def bet_cleanser(self, bet):
    #     if 'btts yes' in bet:
    #         return 'btts yes'

    @staticmethod
    def chunk_it(seq, num): #courtesy of stackover
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out





class Bet9ja(MatchExtractor):
    def games_extractor(self, team):
        driver = self.connect()

        # try:
        elem = driver.find_element_by_class_name("TxtCerca")
        elem.clear()
        # except Exception as e:
        #     print(str(e))
        # else:
        #     elem = driver.find_element_by_xpath('//*[@id="s_w_PC_oddsSearch_txtSearch"]')
        print("TEAM: ", team)
        print("===========???????????PPPPP::::::::::::::")
        elem.send_keys(team)

        try:
            submit = driver.find_element_by_xpath('//*[@id="h_w_PC_oddsSearch_btnCerca"]').click()
        except Exception as e:
            print(str(e))  #terrible I know! debugging 
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

        # try:
        stat = driver.find_element_by_id('h_w_PC_cCoupon_mexPrenotazione')
        # except NoSuchElementException:
        #     # stat = driver.find_element_by_xpath('//*[@id="s_w_PC_PC_gridSottoEventi"]').find_elements(By.TAG_NAME, "tr")[1:] #**barffs**
        #     pass

        if 'not found' in stat.text:
            return {"status": "booking code has expired or invalid!"}

        elif 'proceed' in stat.text: #booking code found but with expired games
            
            driver.find_element_by_id('h_w_PC_cCoupon_lnkOkPrenotatore').click()
            
            time.sleep(2)
            driver.execute_script("$('.CEvento').css({'display':'block', 'position':'static'})")
            try:
                rows = driver.find_elements_by_class_name("CItem")
                n_rows = len(driver.find_elements_by_class_name("CItem"))
            except Exception as e:
                print(">>>>>", str(e))

            print(rows)
            print(n_rows)
            selections = [MatchExtractor.chunk_it(_row.text.split("\n"), n_rows) for _row in rows] #exclude game tag and odd
            _selections = [selection for selection in selections] #exclude game tag and odd

            return selections
        
        else: #booking code found and intact
            driver.execute_script("$('.CEvento').css({'display':'block', 'position':'static'})")
            try:
                rows = driver.find_elements_by_class_name("CItem")
                n_rows = len(driver.find_elements_by_class_name("CItem"))
            except Exception as e:
                print(">>>>>", str(e))
        
            selections = [MatchExtractor.chunk_it(_row.text.split("\n"), n_rows) for _row in rows] #exclude game tag and odd
            _selections = [selection for selection in selections]
            # for __game in selections:
            #     self.injector(__game[0], __game[1].split(" ")[1], __game[1].split(" ")[0])
            print(selections)
            return selections


        #redundant code above; create a function and replace!

    def injector(self, source, selections):
        # matches_extract = _source.slip_extractor()

        league = ''
        bet = ''
        _bet_type = ''
        driver = self.connect()

        for __match in selections:
            if source == 'bet9ja':
                games = self.games_extractor(__match[1][1])

                league = __match[1][0]
                match = __match[1][1]
                bet = __match[2][0].split(" ")[1]
                _bet_type=__match[2][0].split(" ")[0]
                
                if isinstance(games, dict):
                    n_games = [games['league'] + ' ~ ' + games['team']]
                else:
                    n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

            elif source == 'sportybet':
                games = self.games_extractor(__match[1])

                league = ''
                match = __match[1]
                bet = __match[2]
                _bet_type=__match[0]

                n_games = [game['league'] + ' ~ ' + game['team'] for game in games]
            
            else:
                pass

            p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

            csim_check = []
            for game in p_match:
                if len(game) >= 4:
                    relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                    csim = self.check_similarity(relations)
                    csim_check.append([csim, game.split('~ ')[1]])
                else:
                    continue

            print("SMCHL", csim_check)
            select = driver.find_element_by_partial_link_text(max(csim_check)[1].title())

            ActionChains(driver).move_to_element(select).key_down(Keys.CONTROL).click(select).key_up(Keys.COMMAND).perform()
            driver.switch_to.window(driver.window_handles[1])


            bet_types = driver.find_elements_by_class_name("SEOddsTQ")
            bet_selections = driver.find_elements_by_class_name("SECQ")

            #place bet
            for bet_type, bet_selection in zip(bet_types, bet_selections):

                #match bet and bet type: Home - Home and 1x2 - 1x2
                if str(bet_type.text).lower() == str(_bet_type).lower() and (bet_selection.text.lower() == bet.lower()):
                    fo = bet_type.find_element_by_xpath('following-sibling::*')
                    fo.click()
                    break
                    
                else:
                    continue
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # driver.refresh()
            # driver.get(link_bet9ja)
            # # driver.back()
        driver.refresh()
        place_the_bet = driver.find_element_by_class_name('dx').click()
        time.sleep(2)
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        slip_code = str(driver.find_element_by_class_name("number").text).split(':')[1]
        driver.quit()

        return slip_code



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
            print(row.text)
            line = row.text.split('\n')
            line[1] = line[1].split("|")[1].lstrip().replace(' v ',' - ')  #hacky
            access = [0,1,2] #['Home', 'Team A - Team B', '1x2']
            map_access = map(line.__getitem__, access)
            selection.append(list(map_access))
            print("======================================================================")
            print(selection)
        return selection



class X1Bet(MatchExtractor):
    def games_extractor(self, team):
        pass

    def slip_extractor(self):
        pass

    def injector(self, league: str = None, match: str = None, bet: str = None, _bet_type: str = None):
        if 'euro' in league.lower():
            league = 'UEFA European Championship'
        else:
            league = league
        #print("#########", league, match, bet, _bet_type)
        driver = self.connect()

        notification = driver.find_element_by_xpath('//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
        if notification:
            notification.click()
        try:
            elem = driver.find_element_by_xpath('//*[@id="hottest_games"]/div/div[1]/div/div/div/div/div[2]/div/div[1]/input')
        except NoSuchElementException as e:
            print(str(e))
        
        elem.send_keys(match)
        time.sleep(2)

        try:
            elem = driver.find_element_by_xpath('//*[@id="hottest_games"]/div/div[1]/div/div/div/div/div[2]/div/div[1]/button').click()
        except NoSuchElementException as e:
            print(str(e))

        # try:
        #     table = driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[3]/div/section')
        # except NoSuchElementException as e:
        #     print(str(e))
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div').click()
        # time.sleep(2)
        # if live:
        #     live.click()
        #     time.sleep(2)
        
        rows = driver.find_elements(By.CLASS_NAME, "search-popup-events__item")

        # print([sx.text for sx in rows])
        p_match = [_match.text.split("\n") for _match in rows if _match != '' if "LIVE" not in _match.text if 'Alternat' not in _match.text]
        p_match = [_match for _match in p_match if _match != ['']]
        #printPMEA: ", p_match)

        csim_check = []
        for game in p_match:
            if len(game) >= 4:
                print(game)
                relations = [self.clean_string(game[1] + ' ' + game[2]), self.clean_string(league + ' ' + match)]
                #print("REL: ", relations)
                csim = self.check_similarity(relations)
                csim_check.append([csim, game[2]])
                print(game, csim)
            else:
                continue
            
        
        select = driver.find_element_by_partial_link_text(max(csim_check)[1].title()).click()
        windows = driver.window_handles
        #print("SWITCHING TO WINDOW 1")
        driver.switch_to.window(windows[1])
        #print("SWITCHED")
        # else:
        #         print("++++++++++++NO GAME++++++++++++")
        #         return {"status": "Couldn't find the appropriate game to bet on"}

        bet_types = driver.find_elements_by_class_name("bet_type")

        #print("+++++++++++++++++++ABOUT TO PLACE BET")
        #print("_________", _bet_type)
        #place bet
        for bet_type in bet_types:
            if bet_type.text != "" and bet_type.text != " ":
                #print("===================")
                if "Both Teams To Score - No" == _bet_type.title() or "NG" == _bet_type.strip().upper():
                    print(bet_type.text)
                    print("BET SEEN")
                    bet_type.click()
                    time.sleep(1)
                    driver.switch_to.window(windows[0])
                    driver.refresh()
                
                else:
                    #print("3e23e23e32e32BET NOT FOUND")
                    continue
            else:
                continue

  
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

    def injector(self):
        pass


        

        
        

