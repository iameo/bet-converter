import re


###### SOURCE: BET9JA#######

def bet9ja_to_1xbet(bet):
    pass

def bet9ja_to_22bet(bet):
    pass

def bet9ja_to_msport(bet):
    pass


###### SOURCE: 1XBET#######
# Southampton 1X2
def x1bet_to_bet9ja(bet, home, away, league):
    bet_type = ''
    bet_selection = ''

    if 'qualify' in bet:
        bet_type = bet.rsplit(' - ')[0]
        bet_selection = bet.rsplit(' - ')[1]
    elif 'total over' in bet:
        o_u = re.search('\d.\d', bet)
        bet_type = 'Over'
        bet_selection = f'O/U {float(o_u.group())}'
    elif 'total under' in bet:
        o_u = re.search('\d.\d', bet)
        bet_type = 'Under'
        bet_selection = f'O/U {float(o_u.group())}'
    elif 'handicap' in bet:
        bet_selection = bet.split(' ', 1)[0]
        bet_type = bet.split(' ', 1)[1]
    elif 'to win by (3way)' in bet:
        bet_type = bet.split('.')[0]
        bet_selection = bet.split('.')[1]
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
    elif 'correct score (17way' in bet:
        bet_selection = 'Correct Score'
        bet_type = re.search('\d+-\d+', bet)

    elif bet == 'both teams to score both teams to score - yes':
        bet_selection = 'GG/NG'
        bet_type = 'GG'

    elif bet == 'both teams to score both teams to score - no':
        bet_selection = 'GG/NG'
        bet_type = 'NG'

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

    elif '1x2' in bet.split(" ")[-1] and 'baseball' in league:
        bet_type = ' '.join([a for a in bet.split(" ")[:-1]])
        bet_selection = '1 - 2'
        print("PPPPPPPJ: ", bet_type,'c', home,'d', bet, 'e', bet_selection)
        if str(bet_type).lower() in str(home).lower():
            bet_type = '1HH'
        else:
            bet_type = '2HH'



    elif '1x2' in bet.split(" ")[-1]:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        print("PPPPPPP: ", bet_type,'c', home,'d', away,'f', bet, 'e', bet_selection, league)
        if str(bet_type).lower() == str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() == str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

 
    else:
        bet_type = bet.split(" ")[-1]
        bet_selection = ' '.join([a for a in bet.split(" ")[:-1]])
        print("PPPPPPPX: ", bet_type,'c', home,'d', bet, 'e', bet_selection, league)
        if str(bet_type).lower() in str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() in str(away).lower():
            bet_type = 2
        else:
            bet_type = "X"

    return bet_type, bet_selection
    

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

def bet22_to_bet9ja(bet):
    pass

def bet22_to_msport(bet):
    pass


###### SOURCE: MSPORT#######

def msport_to_1xbet(bet):
    pass

def msport_to_22bet(bet):
    pass

def msport_to_bet9ja(bet):
    pass

