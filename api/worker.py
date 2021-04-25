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

import pyperclip

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
    def games_extractor(self, driver, team) -> List[dict]:
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

    @staticmethod
    def match_cleanser(match):
        _match = re.sub(' & \w+', '', match) #Chelsea - Brighton & Hove ==> Chelsea - Brighton
        return _match






class Bet9ja(MatchExtractor):
    def games_extractor(self, driver):

        try:
            submit = driver.find_element_by_xpath('//*[@id="h_w_PC_oddsSearch_btnCerca"]').click()
        except Exception as e:
            print(str(e))  #terrible I know! debugging 

        page_title = driver.title

        time.sleep(2)

        rows = driver.find_element_by_class_name('dgStyle').find_elements(By.TAG_NAME, "tr")[1:]
        
        matches = []

        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")[0:]
            match_team = str(col[0].text)
            match_time = str(col[1].text)
            league = match_team.split("\n")[0]
            match = re.findall(r"\(.*?\)", match_team)

            if not match:
                matches.append({"source": page_title, "league": str(league), "team": match_team.split("\n")[1], "datetime": str(match_time)})
        return matches
        

    def slip_extractor(self):
        driver = self.connect()

        try:
            elem = driver.find_element_by_class_name('TextBox')
        except Exception as e:
            print(">>>>>>", str(e))

        elem.send_keys(self.booking_code)

        try:
            load = driver.find_element_by_class_name('lnk.Load').click()
        except Exception as e:
            print(">>>>>>", str(e)) 

        time.sleep(3)
        # try:
        stat = driver.find_element_by_id('h_w_PC_cCoupon_mexPrenotazione')
        # except NoSuchElementException:
        #     stat = driver.find_element_by_id('s_w_PC_cCoupon_mexPrenotazione')

        if 'not found' in stat.text:
            return {"status": "booking code has expired or invalid!"}

        elif 'proceed' in stat.text: #booking code found but with expired games
            
            driver.find_element_by_id('h_w_PC_cCoupon_lnkOkPrenotatore').click()
            
            time.sleep(1)
            driver.execute_script("$('.CEvento').css({'display':'block', 'position':'static'})")
            
            rows = driver.find_elements_by_class_name("CItem")
            n_rows = len(driver.find_elements_by_class_name("CItem"))

            # selections = [MatchExtractor.chunk_it(_row.text.split("\n"), n_rows) for _row in rows] #exclude game tag and odd
            # _selections = [selection for selection in selections] #exclude game tag and odd

            selections = [row.text.split("\n")[1:-1] for row in rows] #['Premier League', 'Team A - Team B', '1 1X2']
            # print("SELE: ", selections)

            return selections
        
        else: #booking code found and intact
            driver.execute_script("$('.CEvento').css({'display':'block', 'position':'static'})")
                
            rows = driver.find_elements_by_class_name("CItem")
            n_rows = len(driver.find_elements_by_class_name("CItem"))

        
            # selections = [MatchExtractor.chunk_it(_row.text.split("\n"), n_rows) for _row in rows] #exclude game tag and odd
            # _selections = [selection for selection in selections]
            selections = [row.text.split("\n")[1:-1] for row in rows]

            return selections
        #redundant code above; create a function and replace!



    def injector(self, source, selections):
        # matches_extract = _source.slip_extractor()

        league = ''
        bet = ''
        _bet_type = ''

        driver = self.connect()

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

                bet = __match[2].split(" ")[-1]
                _bet_type= ' '.join([a for a in __match[2].split(" ")[:-1]])


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
                # select = driver.find_element_by_partial_link_text(max(csim_check)[1].title())

                max_index = max(range(len(csim_check)), key=csim_check.__getitem__)
                
                time.sleep(2)
                # driver.find_element_by_class_name('dgStyle').find_elements(By.TAG_NAME, "tr")[1:]
                # try:
                rows = driver.find_element_by_class_name('dgStyle').find_elements(By.TAG_NAME, "a")[2:] #['descr', 'date','....']
                # except NoSuchElementException:
                #     rows = driver.find_element_by_id('h_w_PC_PC_gridSottoEventi').find_elements(By.TAG_NAME, "a")[2:] #['descr', 'date','....']



                select_game = rows[max_index] #get the link of the max csim score
                if select_game:
                    if 'Srl' in select_game.text.title(): #"Barcelona Srl"; simulated game; break
                        #move to next match since selected game is simulated
                        driver.back()
                        driver.refresh()
                else:
                    continue #move to next match since no match
                
                ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
                driver.switch_to.window(driver.window_handles[1])


                bet_types = driver.find_elements_by_class_name("SEOddsTQ")
                bet_selections = driver.find_elements_by_class_name("SECQ")
                
                if str(_bet_type).lower() == str(__match[1].split(' - ')[0]).lower():
                    _bet_type = 1
                elif str(_bet_type).lower() == str(__match[1].split(' - ')[1]).lower():
                    _bet_type = 2
                else:
                    _bet_type = _bet_type


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
                driver.back()
                driver.refresh()

            except Exception as e:
                print(str(e))
        # driver.refresh() #since it refrehes in end of loop above
        time.sleep(2)
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
            line = row.text.split("\n")
            line[1] = line[1].split("|")[1].lstrip().replace(' v ',' - ')
            access = [0,1,2] #['Home', 'Team A - Team B', '1x2']
            map_access = map(line.__getitem__, access)
            selection.append(list(map_access))
        return selection



class X1Bet(MatchExtractor):
    def games_extractor(self, team):

        driver = self.connect()

        # notification on 1xbet removed as at 16-04-2021
        # back on 5 hours 2later
        notification = driver.find_element_by_xpath('//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
        if notification:
            notification.click()
        try:
            elem = driver.find_element_by_xpath('//*[@id="hottest_games"]/div/div[1]/div/div/div/div/div[2]/div/div[1]/input')
        except NoSuchElementException as e:
            print(str(e))
            
        elem.clear()
        elem.send_keys(team)

        driver.find_element_by_class_name('sport-search__btn').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div').click()

        time.sleep(2)
        rows = driver.find_elements(By.CLASS_NAME, "search-popup-events__item")
        
        p_match = [_match.text.split("\n") for _match in rows if _match != '' if "LIVE" not in _match.text if 'Alternat' not in _match.text]
        p_match = [_match for _match in p_match if _match != ['']]

        matches = []
        for col in p_match:
            if len(col) >= 4:
                matches.append({"source": "1XBET", "league": str(col[1]), "team": str(col[2]), "datetime": ' '.join([a_ for a_ in col[0].split('.')[1:]]).replace(' ','/')})
            continue
        return matches, driver


    def slip_extractor(self):

        driver = self.connect()
        notification = driver.find_element_by_xpath('//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
        if notification:
            notification.click()
        else:
            pass
        try:
            driver.find_element_by_class_name('c-dropdown__trigger').click()
            coupon = driver.find_element_by_class_name('coupon__input')
            coupon.send_keys(self.booking_code)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="sports_right"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div[3]/div/div/div/div[2]/div/div/div[3]/div/button').click()
            time.sleep(2)
            selections = driver.find_element_by_class_name('coupon__bets').text
        except NoSuchElementException as e:
            print(str(e))
        
        _selections = re.split("\n", selections)
        _selections = [_selections[x:x+4] for x in range(0, len(_selections), 5)] #first 5 elements per selection
        # _selections[0] = re.split('\d+', selections[0])

        games = []
        for game in _selections:
            game[0] = re.split('\d+', game[0])[1]
            game[1] =  game[1] + ' - ' + game[2]
            game[2] =  game[3].split(' ', 1)[1].title() + ' ' + game[3].split(' ', 1)[0]
            games.append(game[:-1]) #exclude last index - redundant

        driver.quit()
        return games


    def injector(self, source, selections):

        league = ''
        bet = '' #e.g Double Chance
        _bet_type = '' #1X or 12 or 2X
        slip_code = ''

        # driver = self.connect()

        # notification = driver.find_element_by_xpath('//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
        # if notification:
        #     notification.click()
        # else:
        #     pass
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
        # driverx.find_element_by_class_name('c-dropdown__trigger').click()
        # coupon = driverx.find_element_by_class_name('coupon__input')
        # coupon.send_keys('faux') #faux code inorder to keep coupon field active otherwise bug from automated environment

        for __match in selections:
            match = __match[1]

            match = MatchExtractor.match_cleanser(match)
            time.sleep(1)
            games, driver = self.games_extractor(match)
           
            if not games:
                continue

            league = __match[0]

            bet = __match[2].split(" ")[-1]
            _bet_type= ' '.join([a for a in __match[2].split(" ")[:-1]])

            n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

            p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

         
            if 'euro' in league.lower():
                league = 'UEFA European Championship'
            else:
                league = league
 
            # p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

            csim_check = []
            for game in p_match:
                relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                if "simulated" not in relations[0] and "-zoom" not in relations[0] \
                            and "alternative" not in relations[0] and "first goal" not in relations[0] and "match stats" not in relations[0] and "team to score " not in relations[0]:
                    csim = self.check_similarity(relations)
                else:
                    csim = 0
                csim_check.append([csim, game.split('~ ')[1]])
            max_index = max(range(len(csim_check)), key=csim_check.__getitem__)

            # driver.find_element_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div').click()
            # driver.find_element_by_xpath('//*[@id="checkbox_1"]').click()
            

            time.sleep(1)
            rows = driver.find_element(By.CLASS_NAME, "search-popup-events").find_elements(By.TAG_NAME, "a")
            #  or driver.find_element_by_class_name('search-popup-events__item')
            # print(rows, max_index)
            select_game = rows[max_index] #get the link of the max csim score
            if select_game:

                ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
                driver.switch_to.window(driver.window_handles[1])               
                #  pass
            else:
                # return "Match not found"
                pass


            window_now = driver.window_handles[0]

            bet_types = driver.find_elements_by_class_name("bet_type")
            bet_selections = driver.find_elements_by_class_name("bet-title")


            if str(_bet_type) == '1': #Home team
                _bet_type = max(csim_check)[1].split(' - ')[0] # Team A - Team B (split and get Team A)
            if str(_bet_type) == '2': #Away team; Draw is Draw still on 1Xbet so no need to alter that
                _bet_type = max(csim_check)[1].split(' - ')[1]
            else:
                _bet_type = _bet_type


            for bet_type, bet_selection in zip(bet_types, bet_selections):
                if (bet_type.text == _bet_type.title() or bet_type.text == _bet_type.strip().upper()) and (str(bet_selection.text).lower() == str(bet).lower()) and bet_type.text != "" and bet_type.text != " ":
                    print("BET SEEN")
                    bet_type.click()
                    time.sleep(1)
                    break
                    
                else:
                    continue
            # driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            # driver.close()

        driver.refresh()

        element = driver.find_element_by_class_name('right-banners-block')

        actions = ActionChains(driver)
        actions.move_to_element(element).perform() #move below save button for interactivity

        driver.find_element_by_class_name('grid__cell.grid__cell--span-6.grid__cell--span-bsr-4.grid__cell--order-bsr-1').click() #tap on save button to generate code

        # coupon.send_keys(Keys.CONTROL, 'a') #mark all
        # coupon.send_keys(Keys.CONTROL, 'c') #copy
        slip_code = pyperclip.paste() #paste copied object in environment

        return slip_code

  
class MSport(MatchExtractor):
    def games_extractor(self, team):
        driver = self.connect(wait_time=3)
        page_title = driver.title
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/a[2]').click() or driver.find_element_by_class_name('m-pop-close-btn').click()

        try:
            driver.find_element_by_class_name('m-az-btn').click()
            driver.find_element_by_xpath('/html/body/div[1]/header/div[4]/div[2]/div[2]/div[1]/a').click()

        except NoSuchElementException as e:
            print(str(e))

        # time.sleep(1)

        try:
            elem = driver.find_element_by_xpath('/html/body/div/div[1]/form/div/input')
        except Exception as e:
            print(str(e))

        elem.send_keys(team)
        time.sleep(2)

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

        try:
            sections = driver.find_elements_by_class_name("m-result-section")
        except Exception:
            pass
        
        matches = []
        for section in sections:
            if section.text.split("\n")[0].lower() == "not start":
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
        return matches, driver

    def slip_extractor(self):
        pass

    def injector(self, source, selections):

        league = ''
        bet = ''
        _bet_type = ''

        # driver = self.connect()

        for __match in selections:
            match = __match[1]

            match = MatchExtractor.match_cleanser(match)

            games, driver = self.games_extractor(match)

            league = __match[0]

            bet = __match[2].split(" ")[1]
            _bet_type=__match[2].split(" ")[0]
                

            n_games = [game['league'] + ' ~ ' + game['team'] for game in games]

            p_match = [_match for _match in n_games if _match != [''] if _match != [' ~ ']]

            csim_check = []
            for game in p_match:
                print("GA<E: ", game, len(game))
                if len(game) >= 4:
                    relations = [self.clean_string(game), self.clean_string(league + ' ' + match)]
                    csim = self.check_similarity(relations)
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
            # print("GA: ", [g.text for g in rows])
            select_game = rows[max_index] #get the link of the max csim score
            if select_game:
                pass
            else:
                return "Match not found"

            ActionChains(driver).move_to_element(select_game).key_down(Keys.CONTROL).click(select_game).key_up(Keys.COMMAND).perform()
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

        driver.refresh()
        place_the_bet = driver.find_element_by_class_name('dx').click()
        time.sleep(2)
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        slip_code = str(driver.find_element_by_class_name("number").text).split(':')[1]
        driver.quit()

        return slip_code



        

        
        

