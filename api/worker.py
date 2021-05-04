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
from . import models
from .helpers import log_error
from .bet_selections import (
    x1bet_to_msport, x1bet_to_bet22, x1bet_to_bet9ja, bet9ja_to_1xbet,\
    msport_to_bet9ja, bet9ja_to_msport, bet22_to_bet9ja, bet22_to_1xbet
    )

import pyperclip

import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


stopwords = stopwords.words('english')


class MatchExtractor(ABC):
    def __init__(self, source: str = None, site: str = None, booking_code: str = None) -> None:
        self.source = source
        self.site = site
        self.booking_code = booking_code

    def connect(self, wait_time=1):
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--window-size=1500,1000")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--no-sandbox')
        options.add_argument('--remote-debugging-port=9222')

        options.binary_location = os.getenv("GOOGLE_CHROME_BIN")

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(chrome_options=options, executable_path=os.getenv('CHROMEDRIVER_PATH'))
        try:
            driver.get(self.site)
            driver.implicitly_wait(wait_time)
        except Exception as e:
            driver.quit()
        return driver


    @abstractmethod
    def games_extractor(self, driver) -> List[dict]:
        pass


    @abstractmethod
    def slip_extractor(self) -> List[str]:
        pass


    def injector(self, source, selections) -> str:
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

    @staticmethod
    def chunk_it(seq, num): #courtesy of stackover
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out

    @staticmethod
    def match_cleanser(match):
        _match = re.sub(' & \w+', '', match) #Chelsea - Brighton & Hove ==> Chelsea - Brighton
        return _match





class Bet9ja(MatchExtractor):
    def games_extractor(self, driver):

        wait = WebDriverWait(driver, 10)

        submit = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="h_w_PC_oddsSearch_btnCerca"]'))).click()

        rows =  wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dgStyle'))).find_elements(By.TAG_NAME, "tr")[1:]

        if not rows:
            driver.back()
            driver.refresh()

        matches = []

        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")[0:]
            match_team = str(col[0].text)
            match_time = str(col[1].text)
            league = match_team.split("\n")[0]
            match = re.findall(r"\(.*?\)", match_team)

            if not match:
                matches.append({"source": "bet9ja", "league": str(league), "team": match_team.split("\n")[1], "datetime": str(match_time)})
        return matches
        

    def slip_extractor(self):
        driver = self.connect()

        selections = None

        wait = WebDriverWait(driver, 10)

        elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'TextBox')))
        elem.send_keys(self.booking_code)

        load = driver.find_element_by_class_name('lnk.Load').click()
 
        stat = wait.until(EC.presence_of_element_located((By.ID, 'h_w_PC_cCoupon_mexPrenotazione')))

        if 'not found' in stat.text:
            selections = None

        elif 'proceed' in stat.text: #booking code found but with expired games
            
            driver.find_element_by_id('h_w_PC_cCoupon_lnkOkPrenotatore').click()
            
            time.sleep(1)
            driver.execute_script("$('.CEvento').css({'display':'block', 'position':'static'})")
            
            rows = driver.find_elements_by_class_name("CItem")

            selections = [row.text.split("\n")[1:-1] for row in rows] #['Premier League', 'Team A - Team B', '1 1X2']

        else: #booking code found and intact
            driver.execute_script("$('.CEvento').css({'display':'block', 'position':'static'})")
                
            rows = driver.find_elements_by_class_name("CItem")

            selections = [row.text.split("\n")[1:-1] for row in rows]
            
        driver.quit()

        return selections
        


    def injector(self, source, selections):
        # matches_extract = _source.slip_extractor()

        league = ''
        bet = ''
        _bet_type = ''

        rows = None
        n_rows = ''

        driver = self.connect()
        wait = WebDriverWait(driver, 10)

        for __match in selections:
            try:
                match = __match[1]
                match = MatchExtractor.match_cleanser(match)
                elem = driver.find_element_by_class_name("TxtCerca")
                elem.click()
                elem.send_keys(" ") #faux to allow input in next loop otherwise buggy
                elem.clear()
                elem.send_keys(match)

                games = self.games_extractor(driver)
                    
                if not games: #no record found, skip to next game
                    continue

                league = __match[0]


                n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

                p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

                csim_check = []

                for game in p_match:
                    if len(game) >= 4:
                        relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                        if "simulated" not in relations[0] and "-zoom" not in relations[0] \
                                and "cyber live" not in relations[0] and "first goal" not in relations[0] and "match stats" not in relations[0] and "team to score " not in relations[0]:
                            csim = self.check_similarity(relations)
                        else:
                            csim = 0
                        csim_check.append([csim, game.split('~ ')[1]])
                    else:
                        continue
                
                max_index = max(range(len(csim_check)), key=csim_check.__getitem__)
                _team = max(csim_check)[1].split(' - ')
                
                rows = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dgStyle'))).find_elements(By.TAG_NAME, "a")[2:] #['descr', 'date','....']
                n_rows = len(wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dgStyle'))).find_elements(By.TAG_NAME, "a")[2:])

                if not rows or n_rows < 1:
                    driver.back()
                    driver.refresh()

                select_game = rows[max_index] #get the link of the max csim score
                if select_game:
                    if 'Srl' in select_game.text.title() or 'srl' in select_game.text.lower().split(' ')[-1]: #"Barcelona Srl"; simulated game; break
                        #move to next match since selected game is simulated
                        driver.back()
                        driver.refresh()
                        continue
                else:
                    continue #move to next match since no match
                
                ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
                driver.switch_to.window(driver.window_handles[1])


                bet_types = driver.find_elements_by_class_name("SEOddsTQ")
                bet_selections = driver.find_elements_by_class_name("SECQ")
                
                # Southampton 1X2
                if source == '1xbet':
                    _bet_type, bet = x1bet_to_bet9ja(__match[2].lower(), _team[0], _team[1], league.lower())
                elif source == 'msport':
                    pass
                elif source == '22bet':
                    _bet_type, bet = bet22_to_bet9ja(__match[2].lower(), _team[0], _team[1], league.lower())
                else:
                    if str(_bet_type).lower() == str(__match[1].split(' - ')[0]).lower():
                        _bet_type = 1
                    elif str(_bet_type).lower() == str(__match[1].split(' - ')[1]).lower():
                        _bet_type = 2
                    else:
                        _bet_type = _bet_type


                for bet_selection in bet_selections:
                    if bet_selection.text.lower() == bet.lower():
                        for bet_type in bet_types:
                            # print("YY: ", bet_type.text, _bet_type, bet_selection.text, bet )
                            if str(bet_type.text).lower() == str(_bet_type).lower():
                                fo = bet_type.find_element_by_xpath('following-sibling::*')
                                fo.click()
                                break
                            continue
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.back()
                driver.refresh()

            except NoSuchElementException as e:
                log_error(str(e))

            except ElementNotInteractableException as e:
                log_error(str(e))

            except Exception as e:
                log_error(str(e))
            
        time.sleep(2)
        place_the_bet = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'dx'))).click()
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
            log_error(str(e))

        except ElementNotInteractableException as e:
            log_error(str(e))

        except Exception as e:
            log_error(str(e))

        elem.send_keys(self.booking_code)
        load = driver.find_element_by_xpath('//*[@id="j_betslip"]/div[2]/div[1]/div/button').click()
        table = driver.find_element_by_class_name("m-list")
        rows = table.find_elements(By.CLASS_NAME, "m-lay-mid")

        selection = []
        for row in rows[::2]: #duplicated in twos so get all even index([0,1,2,3] -> [1,3])
            line = row.text.split("\n")
            line[1] = line[1].split("|")[1].lstrip().replace(' v ',' - ')
            access = [0,1,2] #['Home', 'Team A - Team B', '1x2']
            map_access = map(line.__getitem__, access)
            selection.append(list(map_access))
        return selection



class X1Bet(MatchExtractor):
    def games_extractor(self, driver):

        driver.find_element_by_class_name('sport-search__btn').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div').click()

        time.sleep(2)
        rows = driver.find_elements(By.CLASS_NAME, "search-popup-events__item")
        
        if not rows:
            driver.refresh()

        p_match = [_match.text.split("\n") for _match in rows if _match != '']
        p_match = [_match for _match in p_match if _match != ['']]

        matches = []
        for col in p_match:
            if len(col) >= 4:
                matches.append({"source": "1XBET", "league": str(col[1]), "team": str(col[2]), "datetime": ' '.join([a_ for a_ in col[0].split('.')[1:]]).replace(' ','/')})
            else:
                continue
        return matches


    def slip_extractor(self):

        driver = self.connect()

        wait = WebDriverWait(driver, 10)
        
        notification = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a'))).click()

        try:
            driver.find_element_by_class_name('c-dropdown__trigger').click()
            coupon = driver.find_element_by_class_name('coupon__input')
            coupon.send_keys(self.booking_code)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="sports_right"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div[3]/div/div/div/div[2]/div/div/div[3]/div/button').click()
            time.sleep(2)
            selections = driver.find_element_by_class_name('coupon__bets').text
        
        except NoSuchElementException as e:
            log_error(str(e))

        except ElementNotInteractableException as e:
            log_error(str(e))

        except Exception as e:
            log_error(str(e))

        if selections is None:
            return selections

        _selections = re.split("\n", selections)
        _selections = [_selections[x:x+4] for x in range(0, len(_selections), 5)] #first 5 elements per selection
        # _selections[0] = re.split('\d+', selections[0])

        games = []
        for game in _selections:
            game[0] = re.split('\d+', game[0])[1]
            game[1] =  game[1] + ' - ' + game[2]
            game[2] =  game[3]
            games.append(game[:-1]) #exclude last index - redundant
        driver.quit()
        return games


    def injector(self, source, selections):

        league = ''
        bet = '' #e.g Double Chance
        _bet_type = '' #1X or 12 or 2X
        slip_code = ''

        driver = self.connect()

        notification = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a'))).click()
 
        for __match in selections:
            driver.refresh()
            match = __match[1]
            league = __match[0]

            match = MatchExtractor.match_cleanser(match)
            time.sleep(1)

            try:
                elem = driver.find_element_by_class_name('sport-search__input')
            except NoSuchElementException as e:
                log_error(str(e))

            except ElementNotInteractableException as e:
                log_error(str(e))

            except Exception as e:
                log_error(str(e)) 

            # elem.click()
            elem.send_keys(" ") #faux to allow input in next loop otherwise buggy
            elem.clear()
            elem.send_keys(match + ' ' + league)

            games = self.games_extractor(driver)
            if not games:
                continue



            bet = __match[2].split(" ")[-1]
            _bet_type= ' '.join([a for a in __match[2].split(" ")[:-1]])

            n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

            p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

         
            if 'euro' in league.lower():
                league = 'UEFA European Championship'
            else:
                league = league
 

            csim_check = []
            for game in p_match:
                relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                if "simulated" not in relations[0] and "-zoom" not in relations[0] \
                            and "alternative" not in relations[0] and "first goal" not in relations[0] and "match stats" not in relations[0] \
                                and "team to score " not in relations[0] and "lottery" not in relations[0] and "dream" not in relations[0]:
                    csim = self.check_similarity(relations)
                else:
                    csim = 0
                csim_check.append([csim, game.split('~ ')[1]])
            
            max_index = max(range(len(csim_check)), key=csim_check.__getitem__)


            time.sleep(1)
            rows = driver.find_element(By.CLASS_NAME, "search-popup-events").find_elements(By.TAG_NAME, "a")
            n_rows = len(driver.find_element(By.CLASS_NAME, "search-popup-events").find_elements(By.TAG_NAME, "a"))

            select_game = rows[max_index] #get the link of the max csim score
            
            if not select_game or n_rows < 1:
                continue
            
            link_text = select_game.text.lower()
            if 'alternative' in link_text or 'draft' in link_text or 'esport' in link_text: #"Barcelona Srl"; simulated game; skip
                driver.refresh()
                continue

            ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
            driver.switch_to.window(driver.window_handles[1])


            bet_types = driver.find_elements_by_class_name("bet_type")
            bet_selections = driver.find_elements_by_class_name("bet-title")


            if str(_bet_type) == '1': #Home team
                _bet_type = max(csim_check)[1].split(' - ')[0] # Team A - Team B (split and get Team A)
            if str(_bet_type) == '2': #Away team; Draw is Draw still on 1Xbet so no need to alter that
                _bet_type = max(csim_check)[1].split(' - ')[1]
            else:
                _bet_type = _bet_type

            time.sleep(1)
            for bet_selection in bet_selections:
                if bet_selection.text.lower() == bet.lower():
                    for bet_type in bet_types:
                        # print("YY: ", bet_type.text, _bet_type, bet_selection.text, bet )
                        if str(bet_type.text).lower() == str(_bet_type).lower():
                            fo = bet_type.find_element_by_xpath('following-sibling::*')
                            fo.click()
                            break
                        continue
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()


        element = driver.find_element_by_class_name('right-banners-block')

        actions = ActionChains(driver)
        actions.move_to_element(element).perform() #move below save button for interactivity

        time.sleep(1)
        trigs = driver.find_elements_by_class_name('c-dropdown__trigger')
        trigs[-1].click()

        
        driver.find_element_by_class_name('grid__cell.grid__cell--span-6.grid__cell--span-bsr-4.grid__cell--order-bsr-1').click() #tap on save button to generate code
        
        time.sleep(1)

        trigger_dropdowns = driver.find_elements_by_class_name('coupon-btn-group__item.save-coupon__input-wrap')[-1] #use the last one
        trigger_dropdowns.click()
        
        coupon = trigger_dropdowns.find_element_by_class_name("coupon__input")
        coupon.click()
        a = ActionChains(driver)
        # perform the ctrl+c pressing action
        a.key_down(Keys.CONTROL).click(coupon).send_keys('C').key_up(Keys.CONTROL).perform()

        # slip_code = pyperclip.paste() #paste copied object in environment
        time.sleep(1)
        slip_code = coupon.get_attribute("value")

        driver.quit()

        return slip_code

  
class MSport(MatchExtractor):
    def games_extractor(self, driver):

        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/a[2]').click() or driver.find_element_by_class_name('m-pop-close-btn').click()

        try:
            driver.find_element_by_class_name('m-az-btn').click()
            driver.find_element_by_xpath('/html/body/div[1]/header/div[4]/div[2]/div[2]/div[1]/a').click()

        except NoSuchElementException as e:
            log_error(str(e))

        except ElementNotInteractableException as e:
            log_error(str(e))

        except Exception as e:
            log_error(str(e))
        # time.sleep(1)


        # try:
        #     driver.find_element_by_xpath('/html/body/div/div[1]/div[2]').click()
        # except NoSuchElementException:
        #     pass

        show_more = driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[7]')
        if show_more:
            show_more.click()
        else:
            pass

        # try:
        #     tb = driver.find_element_by_class_name('m-search-main')
        # except Exception:
        #     pass
        time.sleep(3)


        sections = driver.find_elements_by_class_name("m-result-section")

        matches = []
        for section in sections:
            if section.text.split("\n")[0].lower() == "not start":
                games = section.find_elements_by_class_name("m-resultItem")
                for game in games:
                    if "simulated" not in game.text.lower() and "esports" not in game.text.lower() and "cyber live" not in game.text.lower() and "electronic league" not in game.text.lower():
                        _game = game.text.split("\n")
                        matches.append({
                            "source": 'msport',
                            "datetime": _game[0],
                            "league": _game[1],
                            "team": ' '.join([a_ for a_ in _game[2:5]]).replace('vs','-')}
                            )    
        return matches


    def slip_extractor(self):

        driver = self.connect()

        notification = driver.find_element_by_class_name('m-pop-close-btn')
        if notification:
            notification.click()
        else:
            pass

        try:
            driver.find_element_by_class_name('m-betslip-ball').click()
            coupon = driver.find_element_by_class_name('v-input--inner')
            coupon.send_keys(self.booking_code)
            time.sleep(1)
            coupon.send_keys(Keys.ENTER)
            selections = ''
        
        except NoSuchElementException as e:
            log_error(str(e))

        except ElementNotInteractableException as e:
            log_error(str(e))

        except Exception as e:
            log_error(str(e))

        #process selections
        #return selection

    def injector(self, source, selections):

        league = ''
        bet = ''
        _bet_type = ''
        slip_code = ''

        driver = self.connect()

        for __match in selections:
            match = __match[1]

            match = MatchExtractor.match_cleanser(match)
            time.sleep(1)

            elem = driver.find_element_by_xpath('/html/body/div/div[1]/form/div/input')
            elem.click()
            elem.send_keys(" ") #faux to allow input in next loop otherwise buggy
            elem.clear()
            elem.send_keys(match)

            games = self.games_extractor(driver)
           
            if not games:
                continue

            league = __match[0]

            bet = __match[2].split(" ")[-1]
            _bet_type= ' '.join([a for a in __match[2].split(" ")[:-1]])

            n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

            p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]


            csim_check = []

            for game in p_match:
                if len(game) >= 4:
                    relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                    if "simulated" not in relations[0] and "cyber live" not in relations[0]:
                        csim = self.check_similarity(relations)
                    else:
                        csim = 0
                    csim_check.append([csim, game.split('~ ')[1]])
                else:
                    continue

            max_index = max(range(len(csim_check)), key=csim_check.__getitem__)
            
            time.sleep(2)

            show_more = driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[7]')
            if show_more:
                show_more.click()
            else:
                pass

            time.sleep(3)
            sections = driver.find_elements_by_class_name("m-result-section")
            print("SEC: ", sections)
            rows = ''
            for section in sections:
                # if section.text.split("\n")[0].lower() == "not start":
                rows = section.find_elements_by_class_name("m-resultItem")
                # if rows:
                #     break
            # rows = driver.find_elements(By.CLASS_NAME, "m-resultItem")

            select_game = rows[max_index] #get the link of the max csim score

            if select_game:
                if 'Alternative' in select_game.text.title():
                    driver.refresh()
                    continue
            else:
                continue

            ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
            driver.switch_to.window(driver.window_handles[1])


            bet_types = driver.find_elements_by_class_name("")
            bet_selections = driver.find_elements_by_class_name("")

            #place bet
            for bet_selection in bet_selections:
                if bet_selection.text.lower() == bet.lower():
                    for bet_type in bet_types:
                        # print("YY: ", bet_type.text, _bet_type, bet_selection.text, bet )
                        if str(bet_type.text).lower() == str(_bet_type).lower():
                            fo = bet_type.find_element_by_xpath('following-sibling::*')
                            fo.click()
                            break
                        continue
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        #place bet and return slipcode
        return slip_code



class Bet22(MatchExtractor):
    def games_extractor(self, driver):

        try:
            rows = driver.find_elements_by_class_name('search-results-list__item')
        
        except NoSuchElementException as e:
            log_error(str(e))

        except ElementNotInteractableException as e:
            log_error(str(e))

        except Exception as e:
            log_error(str(e))
        
        if not rows:
            driver.refresh()

        matches = []

        for row in rows:
            list_view = row.text.split("\n")
            if len(list_view) == 3:
                league_match = list_view[2].rsplit(".", 1)
                league = league_match[0]
                match_team = league_match[1]
                match_time = list_view[1]

                matches.append({"source": "22bet", "league": str(league), "team": match_team.lstrip().replace('-', ' - '), "datetime": str(match_time)})
            continue
        
        return matches

    def slip_extractor(self):
        driver = self.connect()

        try:
            coupon = driver.find_element_by_class_name('cc-controls__input_text.keyboardInput')

            coupon.clear()
            coupon.send_keys(self.booking_code)

            load = driver.find_element_by_class_name('cc-controls__btn-main_upload').click()

        except NoSuchElementException as e:
            log_error(str(e))

        except ElementNotInteractableException as e:
            log_error(str(e))
        
        except Exception as e:
            log_error(str(e))

        selections = driver.find_element_by_id('all_bets')
        _selections = re.split("\n", selections.text)
        _selections = [_selections[x:x+3] for x in range(0, len(_selections), 4)] #first 3 elements per selection

        games = []      
        for game in _selections:
            game[0] = re.split('\d+', game[0])[1]
            game[1] =  game[1]
            game[2] =  game[2]
            games.append(game)

        driver.quit()
        return games

    def injector(self, source, selections):
        league = ''
        bet = ''
        _bet_type = ''
        slip_code = ''

        driver = self.connect()
        
        wait = WebDriverWait(driver, 10)
        
        for __match in selections:
            try:
                match = __match[1]

                match = MatchExtractor.match_cleanser(match)
                time.sleep(1)

                elem = driver.find_element_by_class_name('input.searchInput.keyboardInput')
                elem.click()
                elem.send_keys(" ") #faux to allow input in next loop otherwise buggy
                elem.clear()
                elem.send_keys(match)
                elem.send_keys(Keys.ENTER)

                games = self.games_extractor(driver)
                    
                if not games: 
                    continue

                league = __match[0]

                bet = __match[2].split(" ")[-1]
                _bet_type= ' '.join([a for a in __match[2].split(" ")[:-1]])


                n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

                p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

                csim_check = []

                for game in p_match:
                    if len(game) >= 4:
                        relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                        if "simulated" not in relations[0] and "pes" not in relations[0] \
                                and "cyber" not in relations[0] and "fifa" not in relations[0] and "4x4" not in relations[0] and "team to score " not in relations[0]:
                            csim = self.check_similarity(relations)
                        else:
                            csim = 0
                        csim_check.append([csim, game.split('~ ')[1]])
                    else:
                        continue

                max_index = max(range(len(csim_check)), key=csim_check.__getitem__)
                _team = max(csim_check)[1].split(' - ')
                
                rows = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results-list'))).find_elements(By.TAG_NAME, "a")

                if not rows:
                    continue
                
                select_game = rows[max_index] #get the link of the max csim score
                if select_game:
                    if '4x4' in select_game.text.title() or 'simulated' in select_game.text.lower(): #"Barcelona Srl"; simulated game; break
                        #move to next match since selected game is simulated
                        driver.back()
                        driver.refresh()
                        continue
                else:
                    continue #move to next match since no match
                
                ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
                # driver.switch_to.window(driver.window_handles[1])

# ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform(
                bet_types = driver.find_elements_by_class_name("bet_type")
                bet_selections = driver.find_elements_by_class_name("bet_group")

                
                if str(_bet_type).lower() == "1" and str(bet) == '1X2':
                    _bet_type = _team[0]
                elif str(_bet_type).lower() == "2" and str(bet) == '1X2':
                    _bet_type = _team[1]
                else:
                    _bet_type = _bet_type


                #place bet
                for bet_selection in bet_selections:
                    if bet_selection.text.lower() == bet.lower():
                        for bet_type in bet_types:
                            # print("YY: ", bet_type.text, _bet_type, bet_selection.text, bet )
                            if str(bet_type.text).lower() == str(_bet_type).lower():
                                fo = bet_type.find_element_by_xpath('following-sibling::*')
                                fo.click()
                                break
                            continue
                # driver.close()
                # driver.switch_to.window(driver.window_handles[0])
                driver.back()
                driver.refresh()

            except NoSuchElementException as e:
                log_error(str(e))

            except ElementNotInteractableException as e:
                log_error(str(e))

            except Exception as e:
                log_error(str(e))
            
        time.sleep(2)
        save_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc-controls__btn-main_get'))).click()
        time.sleep(2)
        slip = driver.find_element_by_class_name('cc-controls__input_text.keyboardInput')
        slip_code = slip.get_attribute('value')

        driver.quit()

        return slip_code



        
        

