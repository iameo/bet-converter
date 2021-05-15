import re


###### SOURCE: BET9JA#######

def bet9ja_to_1xbet(bet, home, away, league):
    bet_type = ''
    bet_selection = ''

    #to qualify
    if 'to qualify' in bet:
        bet_type = bet.rsplit(' - ')[1]
        bet_selection = bet.rsplit(' - ')[1]

    #total over x.x
    elif 'over' in bet and (('o/u' in bet) or ('o / u' in bet)):
        o_u = re.search('\d.\d', bet)
        bet_type = f'Total Over {float(o_u.group())}'
        bet_selection = 'Total'
    #total under x.x
    elif 'under' in bet and (('o/u' in bet) or ('o / u' in bet)):
        o_u = re.search('\d.\d', bet)
        bet_type = f'Total Under {float(o_u.group())}'
        bet_selection = 'Total'

    #handicap market
    # elif 'handicap' in bet:
    #     bet_selection = bet.split(' ', 1)[0]
    #     bet_type = bet.split(' ', 1)[1]
    
    #3way win
    # elif 'to win by (3way)' in bet:
    #     bet_type = bet.split('.')[0]
    #     bet_selection = bet.split('.')[1]
    
    #DOUBLE CHANCE SELECTIONS#

    #Double Chance Halftime
    elif 'ht double chance' in bet:
        if "12" in bet:
            bet_type = f'{home} Or {away}'
        elif "1x" in bet:
            bet_type = f'{home} Or X'
        elif "x2" in bet:
            bet_type = f'{away} Or X'
        else:
            bet_type = ''

        bet_selection = 'Double Chance HT'

    #Double Chance 2HT (Second Half)
    elif '2ht double chance' in bet:
        if "12" in bet:
            bet_type = f'{home} Or {away}'
        elif "1x" in bet:
            bet_type = f'{home} Or X'
        elif "x2" in bet:
            bet_type = f'{away} Or X'
        else:
            bet_type = ''

        bet_selection = 'Double Chance 2HT'

    #Double Chance - 60mins
    elif 'double chance' in bet:
        if "12" in bet:
            bet_type = f'{home} Or {away}'
        elif "1x" in bet:
            bet_type = f'{home} Or X'
        elif "x2" in bet:
            bet_type = f'{away} Or X'
        else:
            bet_type = ''

        bet_selection = 'Double Chance'


    #first goal
    elif 'next goal' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        elif 'neither' in bet:
            bet_type = 'No Goal'
        else:
            bet_type = ''
        bet_selection = 'First Goal'
    #last goal
    elif 'next goal 1' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        else:
            #'no one' in bet:
            bet_type = 'No Goal'
        bet_selection = 'Last Goal'

    #correct score
    elif 'correct score' in bet:
        bet_selection = 'Correct Score (17Way)'
        score = re.search('\d+-\d+', bet)
        bet_type = f'Correct Score {score.group()}'

    #both teams to score - 2 goals+ yes
    elif 'gg gg/ng 2+' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Each Team To Score 2 Or More - Yes'
    #both teams to score - 2 goals+ no
    elif 'ng gg/ng 2+' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Each Team To Score 2 Or More - No'

    #both teams to score - yes 
    elif 'gg gg/ng' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - Yes'
    #both teams to score - no
    elif 'ng gg/ng' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - No'
    #btts - team to score
    elif 'gg team to score' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - Yes'
    elif 'ng team to score' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - No'

    
    #--- Result and Both Teams to Score -- #
    elif '1x & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} X And Both Teams To Score - Yes'
    elif '2x & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{away} X And Both Teams To Score - Yes'
    elif '12 & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} {away} And Both Teams To Score - Yes'
    elif '1x & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} X And Both Teams To Score - No'
    elif '2x & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{away} X And Both Teams To Score - No'
    elif '12 & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} {away} And Both Teams To Score - No'
    elif '1 & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {home} And Both Teams To Score - Yes'
    elif '2 & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {away} And Both Teams To Score - Yes'
    elif 'x & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = 'X And Both Teams To Score - Yes'
    elif '1 & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {home} And Both Teams To Score - No'
    elif '2 & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {away} And Both Teams To Score - No'
    elif 'x & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = 'X And Both Teams To Score - No'
    
        #!--- end of result and btts ---#

    # -- Result and in minutes --#
    elif '1x2 -' in bet:
        get_time = re.match('\d+', bet.split(' - ')[-1])
        get_result = bet.split(' ')[0]
        if '1' == get_result:
            bet_type = f'{home} To Win In {get_time.group()} Minute'
        elif '2' == get_result:
            bet_type = f'{away} To Win In {get_time.group()} Minute'
        elif 'x' == get_result:
            bet_type = f'Draw In {get_time.group()} Minute'
        else:
            bet_type = ''

        bet_selection = 'Result In Minute'

    elif 'double chance -' in bet or 'dc -' in bet: #double chance
        get_time = re.match('\d+', bet.split(' - ')[-1])
        get_result = bet.split(' ')[0]
        if '1x' == get_result:
            bet_type = f'{home} X In {get_time.group()} Minute'
        elif 'x2' == get_result:
            bet_type = f'{away} X In {get_time.group()} Minute'
        elif '12' == get_result:
            bet_type = f'{home} {away} In {get_time.group()} Minute'
        else:
            bet_type = ''

        bet_selection = 'Win or Draw In Minute'


    #HT-FT 1x2
    elif 'ht/ft' in bet:
        bet_selection = "HT-FT"
        _bet_type = bet.split(' ', 1)[0]
        if '1/1' == _bet_type:
            bet_type = f'HT-FT W {home} W {home}'
        elif '1/x' == _bet_type:#ht-ft HT-FT W UDINESE CALCIO X
            bet_type = f'HT-FT W {home} X'
        elif '1/2' == _bet_type: 
            bet_type = f'HT-FT W {home} W {away}'
        elif 'x/1' == _bet_type: #ht-ft ht-ft XW UDINESE CALCIO
            bet_type = f'HT-FT XW {home}'
        elif 'x/x' == _bet_type:
            bet_type = f'HT-FT XX'
        elif 'x/2'== _bet_type:
            bet_type = f'HT-FT XW {away}'
        elif '2/1' == _bet_type: 
            bet_type = f'HT-FT W {away} W {home}'
        elif  '2/x' == _bet_type: 
            bet_type = f'HT-FT W {away} X'
        elif '2/2' == _bet_type: 
            bet_type = f'HT-FT W {away} W {away}'
        else:
            bet_type = ''
        
    # SCORES IN EACH HALF 1ST HALF > 2ND HALF
    elif 'highest scoring half' in bet:
        bet_selection = 'Scores In Each Half'
        if '1st' in bet:
            bet_type = '1st Half > 2nd Half'
        elif '2nd' in bet:
            bet_type = '1st Half < 2nd Half'
        elif 'equal' in bet:
            bet_type = '1st Half = 2nd Half'
        else:
            bet_type = ''

    #yellow card - team
    elif 'yellow card yellow card' in bet:
        if 'yellow card - yes' in bet:
            bet_type = 'yes yellow card'
        elif 'yellow card - no' in bet:
            bet_type = 'no yellow card'
        else:
            bet_type = ''
        bet_selection = 'Yellow Card'

    #red card - team
    elif 'red card' in bet:
        if 'yes red card' in bet:
            bet_type = 'red card - yes'
        elif 'no red card' in bet:
            bet_type = 'red card - no'
        else:
            bet_type = ''
        bet_selection = 'Red Card'


    #basketball specials######
    elif ('basketball' in league or 'nba' in league) and '1x2' in bet:
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if '1HH' in bet:
            bet_type = home
        elif '2HH' in bet:
            bet_type = away
        else:
            bet_type = ''

    
    elif ('basketball' in league or 'nba' in league) and ('1x2 rt' in bet or '1x2' in bet or '1x2 (5.5)' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if 1 == bet:
            bet_type = home
        elif 2 == bet:
            bet_type = away
        else:
            bet_type = 'X'

    elif ('basketball' in league or 'nba' in league) and ('1x2 in regular time' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    # --- end of basketball special markets ----

    # -- baseball market ---
    elif '1x2' in bet.split(" ")[-1] and ('baseball' in league or 'tennis' in league):
        bet_type = bet.split(" ", 1)[-1]
        bet_selection = '1 - 2'
        # ##print("PPPPPPPJ: ", bet_type,'c', home,'d', bet, 'e', bet_selection)
        if str(bet_type).lower() in str(home).lower():
            bet_type = '1HH'
        else:
            bet_type = '2HH'
    # -- end of baseball marker ---


    elif '1x2' in bet:
        bet_type = bet.split(" ")[0]
        bet_selection = '1x2'
        ##print("PPPPPPP: ", bet_type,'c', home,'d', away,'f', bet, 'e', bet_selection, league)
        if str(bet_type).lower() == '1':
            bet_type = f'{home}'
        elif str(bet_type).lower() == '2':
            bet_type = f'{away}'
        else:
            bet_type = "Draw"

 
    else:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        #print("PPPPPPPX: ", bet_type,'c', home,'d', bet, 'e', bet_selection, league)
        if str(bet_type).lower() in str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() in str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

    return bet_type, bet_selection

    
#almost same market structure as 1xbet
def bet9ja_to_22bet(bet):
    bet_type = ''
    bet_selection = ''

    #odd/even
    if 'odd/even' in bet:
        bet_selection = 'Even/odd'
        odd_even = bet.split(' ')[0]
        if odd_even is 'odd':
            bet_type = 'Total Even - No' 
        bet_type = 'Total Even - Yes'
        

    #total over x.x
    elif 'over' in bet and (('o/u' in bet) or ('o / u' in bet)):
        o_u = re.search('\d.\d', bet)
        bet_type = f'Total Over {float(o_u.group())}'
        bet_selection = 'Total'
    #total under x.x
    elif 'under' in bet and (('o/u' in bet) or ('o / u' in bet)):
        o_u = re.search('\d.\d', bet)
        bet_type = f'Total Under {float(o_u.group())}'
        bet_selection = 'Total'

    #------DOUBLE CHANCE SELECTIONS----------#
    #Double Chance Halftime
    elif 'ht double chance' in bet:
        if "12" in bet:
            bet_type = f'{home} Or {away}'
        elif "1x" in bet:
            bet_type = f'{home} Or X'
        elif "x2" in bet:
            bet_type = f'{away} Or X'
        else:
            bet_type = ''

        bet_selection = 'Double Chance HT'

    #Double Chance 2HT (Second Half)
    elif '2ht double chance' in bet:
        if "12" in bet:
            bet_type = f'{home} Or {away}'
        elif "1x" in bet:
            bet_type = f'{home} Or X'
        elif "x2" in bet:
            bet_type = f'{away} Or X'
        else:
            bet_type = ''

        bet_selection = 'Double Chance 2HT'

    #Double Chance - 60mins
    elif 'double chance' in bet:
        if "12" in bet:
            bet_type = f'{home} Or {away}'
        elif "1x" in bet:
            bet_type = f'{home} Or X'
        elif "x2" in bet:
            bet_type = f'{away} Or X'
        else:
            bet_type = ''

        bet_selection = 'Double Chance'


    #first goal
    elif 'next goal' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        elif 'neither' in bet:
            bet_type = 'No Goal'
        else:
            bet_type = ''
        bet_selection = 'First Goal'
    #last goal
    elif 'next goal 1' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        else:
            #'no one' in bet:
            bet_type = 'No Goal'
        bet_selection = 'Last Goal'

    #correct score
    elif 'correct score' in bet:
        bet_selection = 'Correct Score (17Way)'
        score = re.search('\d+-\d+', bet)
        bet_type = f'Correct Score {score.group()}'

    #both teams to score - 2 goals+ yes
    elif 'gg gg/ng 2+' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Each Team To Score 2 Or More - Yes'
    #both teams to score - 2 goals+ no
    elif 'ng gg/ng 2+' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Each Team To Score 2 Or More - No'

    #both teams to score - yes 
    elif 'gg gg/ng' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - Yes'
    #both teams to score - no
    elif 'ng gg/ng' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - No'
    #btts - team to score
    elif 'gg team to score' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - Yes'
    elif 'ng team to score' in bet:
        bet_selection = 'Both Teams To Score'
        bet_type = 'Both Teams To Score - No'

    
    #--- Result and Both Teams to Score -- #
    elif '1x & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} X And Both Teams To Score - Yes'
    elif '2x & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{away} X And Both Teams To Score - Yes'
    elif '12 & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} {away} And Both Teams To Score - Yes'
    elif '1x & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} X And Both Teams To Score - No'
    elif '2x & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{away} X And Both Teams To Score - No'
    elif '12 & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'{home} {away} And Both Teams To Score - No'
    elif '1 & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {home} And Both Teams To Score - Yes'
    elif '2 & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {away} And Both Teams To Score - Yes'
    elif 'x & gg dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = 'X And Both Teams To Score - Yes'
    elif '1 & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {home} And Both Teams To Score - No'
    elif '2 & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = f'W {away} And Both Teams To Score - No'
    elif 'x & ng dc & gg/ng' in bet:
        bet_selection = 'Result And Both Teams To Score'
        bet_type = 'X And Both Teams To Score - No'
    
        #!--- end of result and btts ---#

    # -- Result and in minutes --#
    elif '1x2 -' in bet:
        get_time = re.match('\d+', bet.split(' - ')[-1])
        get_result = bet.split(' ')[0]
        if '1' == get_result:
            bet_type = f'{home} To Win In {get_time.group()} Minute'
        elif '2' == get_result:
            bet_type = f'{away} To Win In {get_time.group()} Minute'
        elif 'x' == get_result:
            bet_type = f'Draw In {get_time.group()} Minute'
        else:
            bet_type = ''

        bet_selection = 'Result In Minute'

    elif 'double chance -' in bet or 'dc -' in bet: #double chance
        get_time = re.match('\d+', bet.split(' - ')[-1])
        get_result = bet.split(' ')[0]
        if '1x' == get_result:
            bet_type = f'{home} X In {get_time.group()} Minute'
        elif 'x2' == get_result:
            bet_type = f'{away} X In {get_time.group()} Minute'
        elif '12' == get_result:
            bet_type = f'{home} {away} In {get_time.group()} Minute'
        else:
            bet_type = ''

        bet_selection = 'Win or Draw In Minute'


    #HT-FT 1x2
    elif 'ht/ft' in bet:
        bet_selection = "HT-FT"
        _bet_type = bet.split(' ', 1)[0]
        if '1/1' == _bet_type:
            bet_type = f'HT-FT W {home} W {home}'
        elif '1/x' == _bet_type:#ht-ft HT-FT W UDINESE CALCIO X
            bet_type = f'HT-FT W {home} X'
        elif '1/2' == _bet_type: 
            bet_type = f'HT-FT W {home} W {away}'
        elif 'x/1' == _bet_type: #ht-ft ht-ft XW UDINESE CALCIO
            bet_type = f'HT-FT XW {home}'
        elif 'x/x' == _bet_type:
            bet_type = f'HT-FT XX'
        elif 'x/2'== _bet_type:
            bet_type = f'HT-FT XW {away}'
        elif '2/1' == _bet_type: 
            bet_type = f'HT-FT W {away} W {home}'
        elif  '2/x' == _bet_type: 
            bet_type = f'HT-FT W {away} X'
        elif '2/2' == _bet_type: 
            bet_type = f'HT-FT W {away} W {away}'
        else:
            bet_type = ''
        
    # SCORES IN EACH HALF 1ST HALF > 2ND HALF
    elif 'highest scoring half' in bet:
        bet_selection = 'Scores In Each Half'
        if '1st' in bet:
            bet_type = '1st Half > 2nd Half'
        elif '2nd' in bet:
            bet_type = '1st Half < 2nd Half'
        elif 'equal' in bet:
            bet_type = '1st Half = 2nd Half'
        else:
            bet_type = ''

    #yellow card - team
    elif 'yellow card yellow card' in bet:
        if 'yellow card - yes' in bet:
            bet_type = 'yes yellow card'
        elif 'yellow card - no' in bet:
            bet_type = 'no yellow card'
        else:
            bet_type = ''
        bet_selection = 'Yellow Card'

    #red card - team
    elif 'red card' in bet:
        if 'yes red card' in bet:
            bet_type = 'red card - yes'
        elif 'no red card' in bet:
            bet_type = 'red card - no'
        else:
            bet_type = ''
        bet_selection = 'Red Card'


    #basketball specials######
    elif ('basketball' in league or 'nba' in league) and '1x2' in bet:
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if '1HH' in bet:
            bet_type = home
        elif '2HH' in bet:
            bet_type = away
        else:
            bet_type = ''

    
    elif ('basketball' in league or 'nba' in league) and ('1x2 rt' in bet or '1x2' in bet or '1x2 (5.5)' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if 1 == bet:
            bet_type = home
        elif 2 == bet:
            bet_type = away
        else:
            bet_type = 'X'

    elif ('basketball' in league or 'nba' in league) and ('1x2 in regular time' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    # --- end of basketball special markets ----

    # -- baseball market ---
    elif '1x2' in bet.split(" ")[-1] and ('baseball' in league or 'tennis' in league):
        bet_type = bet.split(" ", 1)[-1]
        bet_selection = '1 - 2'
        # ##print("PPPPPPPJ: ", bet_type,'c', home,'d', bet, 'e', bet_selection)
        if str(bet_type).lower() in str(home).lower():
            bet_type = '1HH'
        else:
            bet_type = '2HH'
    # -- end of baseball marker ---


    elif '1x2' in bet:
        bet_type = bet.split(" ")[0]
        bet_selection = '1x2'
        ##print("PPPPPPP: ", bet_type,'c', home,'d', away,'f', bet, 'e', bet_selection, league)
        if str(bet_type).lower() == '1':
            bet_type = f'{home}'
        elif str(bet_type).lower() == '2':
            bet_type = f'{away}'
        else:
            bet_type = "Draw"

 
    else:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        #print("PPPPPPPX: ", bet_type,'c', home,'d', bet, 'e', bet_selection, league)
        if str(bet_type).lower() in str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() in str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

    return bet_type, bet_selection



def bet9ja_to_msport(bet):
    pass


###### SOURCE: 1XBET#######
# Southampton 1X2
def x1bet_to_bet9ja(bet, home, away, league):
    bet_type = ''
    bet_selection = ''

    #to qualify
    if 'to qualify' in bet:
        bet_type = bet.rsplit(' - ')[1]
        bet_selection = 'to qualify'

        if home.lower() in bet_type:
            bet_type = '1 to qualify'
        elif away.lower() in bet_type:
            bet_type = '2 to qualify'
        else:
            bet_type = ''
            
    #total over x.x
    elif 'total over' in bet:
        o_u = re.search('\d.\d', bet)
        bet_type = 'Over'
        bet_selection = f'O/U {float(o_u.group())}'
    #total under x.x
    elif 'total under' in bet:
        o_u = re.search('\d.\d', bet)
        bet_type = 'Under'
        bet_selection = f'O/U {float(o_u.group())}'

    #handicap market
    elif 'handicap' in bet:
        bet_selection = bet.split(' ', 1)[0]
        bet_type = bet.split(' ', 1)[1]
    
    #3way win
    elif 'to win by (3way)' in bet:
        bet_type = bet.split('.')[0]
        bet_selection = bet.split('.')[1]
    
    #double chance
    elif 'double chance' in bet:
        if f'{home} or {away}' in bet:
            bet_type = "12"
        elif f'{home} or x':
            bet_type = "1X"
        elif f'{away} or x' in bet_type:
            bet_type = 'X2'
        else:
            bet_type = ''

        bet_selection = ' '.join([a for a in bet.split(" ",2)[:-1]])

    #first goal
    elif 'next goal 1' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        elif 'neither' in bet:
            bet_type = 'No Goal'
        else:
            bet_type = ''
        bet_selection = 'First Goal'
    #last goal
    elif 'next goal 1' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        else:
            #'no one' in bet:
            bet_type = 'No Goal'
        bet_selection = 'Last Goal'

    #correct score
    elif 'correct score' in bet:
        bet_selection = 'Correct Score'
        bet_type = re.search('\d+-\d+', bet)

    #both teams to score - yes
    elif bet == 'both teams to score both teams to score - yes':
        bet_selection = 'GG/NG'
        bet_type = 'GG'
    #both teams to score - no
    elif bet == 'both teams to score both teams to score - no':
        bet_selection = 'GG/NG'
        bet_type = 'NG'
    
    #both teams to score - 2 goals+ yes
    elif bet == 'both teams to score each team to score 2 or more - yes':
        bet_selection = 'GG/NG 2+'
        bet_type = 'GG'
    #both teams to score - 2 goals+ no
    elif bet == 'both teams to score each team to score 2 or more - no':
        bet_selection = 'GG/NG 2+'
        bet_type = 'NG'

    #HT-FT 1x2
    elif 'ht-ft ht-ft' in bet:
        bet_selection = "HT/FT"
        _bet_type = bet.split(' ', 1)[-1]
        if f'ht-ft w {home} w {home}' == _bet_type:
            bet_type = '1/1'
        elif f'ht-ft w {home} x' == _bet_type:#ht-ft ht-ft W UDINESE CALCIO X
            bet_type = '1/X'
        elif f'ht-ft w {home} w {away}'  == _bet_type: 
            bet_type = '1/2'
        elif f'ht-ft xw {home}' == _bet_type: #ht-ft ht-ft XW UDINESE CALCIO
            bet_type = 'X/1'
        elif f'ht-ft xx' == _bet_type:
            bet_type = 'X/X'
        elif f'ht-ft xw {away}' == _bet_type:
            bet_type = 'X/2'
        elif f'ht-ft w {away} w {home}' == _bet_type: 
            bet_type = '2/1'
        elif f'ht-ft w {away} x' == _bet_type: 
            bet_type = '2/X'
        elif f'ht-ft w {away} w {away}' == _bet_type: 
            bet_type = '2/2'
        else:
            bet_type = ''
        
# SCORES IN EACH HALF 1ST HALF > 2ND HALF
    elif 'scores in each half' in bet.rsplit(' ',5):
        bet_selection = 'highest scoring half'
        _bet_type = bet.split(' ', 4)[4]
        if '1st half > 2nd half' == _bet_type:
            bet_type = '1st'
        elif '1st half < 2nd half' == _bet_type:
            bet_type = '2nd'
        elif '1st half = 2nd half' == _bet_type:
            bet_type = 'Equal'
        else:
            bet_type = ''

    #yellow card - team
    elif 'yellow card yellow card' in bet:
        if 'yellow card - yes' in bet:
            bet_type = 'yes yellow card'
        elif 'yellow card - no' in bet:
            bet_type = 'no yellow card'
        else:
            bet_type = ''

    #red card - team
    elif 'red card red card' in bet:
        if 'red card - yes' in bet:
            bet_type = 'yes red card'
        elif 'red card - no' in bet:
            bet_type = 'no red card'
        else:
            bet_type = ''


    #basketball specials######
    elif ('basketball' in league or 'nba' in league) and '1x2 in regular time' in bet:
        bet_selection = '1 - 2'
        if home.lower() in bet:
            bet_type = "1HH"
        elif away.lower() in bet:
            bet_type = '2HH'
        else:
            bet_type = ''

    #overtime - yes/no
    elif ('basketball' in league or 'nba' in league) and 'will there be overtime' in bet:
        bet_selection = 'overtime yes/no'
        bet_type = bet.split(' ', 6)[-1]
        if 'will there be overtime? - yes' == bet_type:
            bet_type = "ot yes"
        elif 'will there be overtime? - no' == bet_type:
            bet_type = 'ot no'
        else:
            bet_type = ''
    
    elif ('basketball' in league or 'nba' in league) and ('1x2 rt' in bet or '1x2' in bet or '1x2 (5.5)' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    # --- end of basketball special markets ----

    # -- baseball market ---
    elif '1x2' in bet.split(" ")[-1] and 'baseball' in league:
        bet_type = ' '.join([a for a in bet.split(" ")[:-1]])
        bet_selection = '1 - 2'
        #print("PPPPPPPJ: ", bet_type,'c', home,'d', bet, 'e', bet_selection)
        if str(bet_type).lower() in str(home).lower():
            bet_type = '1HH'
        else:
            bet_type = '2HH'
    # -- end of baseball marker ---


    elif '1x2' in bet.split(" ")[-1]:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        #print("PPPPPPP: ", bet_type,'c', home,'d', away,'f', bet, 'e', bet_selection, league)
        if str(bet_type).lower() == str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() == str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

 
    else:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        #print("PPPPPPPX: ", bet_type,'c', home,'d', bet, 'e', bet_selection, league)
        if str(bet_type).lower() in str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() in str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

    return bet_type, bet_selection
    


############## X1bet -> 22BET ###############
def x1bet_to_bet22(bet):
    bet_type = ''
    bet_selection = ''

    if 'qualify' in bet:
        bet_type = bet.rsplit(' - ')[1]
        bet_selection = bet.rsplit(' - ')[0]
    elif 'total over' in bet:
        bet_type = bet.split(' ', 1)[1]
        bet_selection = bet.split(' ', 1)[0]
    elif 'to win by (3way)' in bet:
        bet_type = bet.split('.')[1]
        bet_selection = bet.split('.')[0]
    else:
        bet_type = bet.split(' ')[1]
        bet_selection = bet.split(' ')[0]

    return bet_type, bet_selection
    

def x1bet_to_msport(bet):
    pass


###### SOURCE: 22BET#######

def bet22_to_1xbet(bet):
    pass

def bet22_to_bet9ja(bet, home, away, league):
    bet_type = ''
    bet_selection = ''

    #to qualify
    if 'to qualify' in bet:
        bet_type = bet.rsplit(' - ')[1]
        bet_selection = bet.rsplit(' - ')[1]

    #total over x.x
    elif 'total over' in bet:
        o_u = re.search('\d.\d', bet)
        bet_type = 'Over'
        bet_selection = f'O/U {float(o_u.group())}'
    #total under x.x
    elif 'total under' in bet:
        o_u = re.search('\d.\d', bet)
        bet_type = 'Under'
        bet_selection = f'O/U {float(o_u.group())}'

    #handicap market
    elif 'handicap' in bet:
        bet_selection = bet.split(' ', 1)[0]
        bet_type = bet.split(' ', 1)[1]
    
    #3way win
    elif 'to win by (3way)' in bet:
        bet_type = bet.split('.')[0]
        bet_selection = bet.split('.')[1]
    
    #double chance
    elif 'double chance' in bet:
        if f'{home} or {away}' in bet:
            bet_type = "12"
        elif f'{home} or x':
            bet_type = "1X"
        elif f'{away} or x' in bet_type:
            bet_type = 'X2'
        else:
            bet_type = ''

        bet_selection = ' '.join([a for a in bet.split(" ",2)[:-1]])

    #first goal
    elif 'next goal 1' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        elif 'neither' in bet:
            bet_type = 'No Goal'
        else:
            bet_type = ''
        bet_selection = 'First Goal'
    #last goal
    elif 'next goal 1' in bet:
        if home in bet:
            bet_type = 1
        elif away in bet:
            bet_type = 2
        else:
            #'no one' in bet:
            bet_type = 'No Goal'
        bet_selection = 'Last Goal'

    #correct score
    elif 'correct score' in bet:
        bet_selection = 'Correct Score'
        bet_type = re.search('\d+-\d+', bet)

    #both teams to score - yes
    elif bet == 'both teams to score both teams to score - yes':
        bet_selection = 'GG/NG'
        bet_type = 'GG'
    #both teams to score - no
    elif bet == 'both teams to score both teams to score - no':
        bet_selection = 'GG/NG'
        bet_type = 'NG'
    
    #both teams to score - 2 goals+ yes
    elif bet == 'both teams to score each team to score 2 or more - yes':
        bet_selection = 'GG/NG 2+'
        bet_type = 'GG'
    #both teams to score - 2 goals+ no
    elif bet == 'both teams to score each team to score 2 or more - no':
        bet_selection = 'GG/NG 2+'
        bet_type = 'NG'

    #HT-FT 1x2
    elif 'ht-ft ht-ft' in bet:
        bet_selection = "HT/FT"
        _bet_type = bet.split(' ', 1)[-1]
        if f'ht-ft w {home} w {home}' == _bet_type:
            bet_type = '1/1'
        elif f'ht-ft w {home} x' == _bet_type:#ht-ft ht-ft W UDINESE CALCIO X
            bet_type = '1/X'
        elif f'ht-ft w {home} w {away}'  == _bet_type: 
            bet_type = '1/2'
        elif f'ht-ft xw {home}' == _bet_type: #ht-ft ht-ft XW UDINESE CALCIO
            bet_type = 'X/1'
        elif f'ht-ft xx' == _bet_type:
            bet_type = 'X/X'
        elif f'ht-ft xw {away}' == _bet_type:
            bet_type = 'X/2'
        elif f'ht-ft w {away} w {home}' == _bet_type: 
            bet_type = '2/1'
        elif f'ht-ft w {away} x' == _bet_type: 
            bet_type = '2/X'
        elif f'ht-ft w {away} w {away}' == _bet_type: 
            bet_type = '2/2'
        else:
            bet_type = ''
        
# SCORES IN EACH HALF 1ST HALF > 2ND HALF
    elif 'scores in each half' in bet.rsplit(' ',5):
        bet_selection = 'highest scoring half'
        _bet_type = bet.split(' ', 4)[4]
        if '1st half > 2nd half' == _bet_type:
            bet_type = '1st'
        elif '1st half < 2nd half' == _bet_type:
            bet_type = '2nd'
        elif '1st half = 2nd half' == _bet_type:
            bet_type = 'Equal'
        else:
            bet_type = ''

    #yellow card - team
    elif 'yellow card yellow card' in bet:
        if 'yellow card - yes' in bet:
            bet_type = 'yes yellow card'
        elif 'yellow card - no' in bet:
            bet_type = 'no yellow card'
        else:
            bet_type = ''

    #red card - team
    elif 'red card red card' in bet:
        if 'red card - yes' in bet:
            bet_type = 'yes red card'
        elif 'red card - no' in bet:
            bet_type = 'no red card'
        else:
            bet_type = ''


    #basketball specials######
    elif ('basketball' in league or 'nba' in league) and '1x2' in bet:
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if home in bet_type:
            bet_type = "1HH"
        elif away in bet_type:
            bet_type = '2HH'
        else:
            bet_type = ''

    
    elif ('basketball' in league or 'nba' in league) and ('1x2 rt' in bet or '1x2' in bet or '1x2 (5.5)' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    elif ('basketball' in league or 'nba' in league) and ('1x2 in regular time' in bet):
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    # --- end of basketball special markets ----

    # -- baseball market ---
    elif '1x2' in bet.split(" ")[-1] and ('baseball' in league or 'tennis' in league):
        bet_type = ' '.join([a for a in bet.split(" ")[:-1]])
        bet_selection = '1 - 2'
        #print("PPPPPPPJ: ", bet_type,'c', home,'d', bet, 'e', bet_selection)
        if str(bet_type).lower() in str(home).lower():
            bet_type = '1HH'
        else:
            bet_type = '2HH'
    # -- end of baseball marker ---


    elif '1x2' in bet.split(" ")[-1]:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        #print("PPPPPPP: ", bet_type,'c', home,'d', away,'f', bet, 'e', bet_selection, league)
        if str(bet_type).lower() == str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() == str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

 
    else:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        #print("PPPPPPPX: ", bet_type,'c', home,'d', bet, 'e', bet_selection, league)
        if str(bet_type).lower() in str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() in str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

    return bet_type, bet_selection
    
def bet22_to_msport(bet):
    pass


###### SOURCE: MSPORT#######

def msport_to_1xbet(bet):
    pass

def msport_to_22bet(bet):
    pass

def msport_to_bet9ja(bet):
    pass

