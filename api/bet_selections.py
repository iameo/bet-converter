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
        bet_type = bet.split(' ', 1)[0]
        bet_selection = bet.split(' ', 1)[1]
    elif 'to win by (3way)' in bet:
        bet_type = bet.split('.')[0]
        bet_selection = bet.split('.')[1]
    elif 'double chance' in bet:
        bet_type = bet.split(' ', 2)[0]
        if home in bet_type and away in bet_type:
            bet_type = "12"
        elif home in bet_type:
            bet_type = "1X"
        elif away in bet_type:
            bet_type = 'X2'
        else:
            bet_type = ''

        bet_selection = bet.split(' ', 2)[1]

    elif ('basketball' in league or 'nba' in league) and '1 - 2' in bet:
        if home in bet_type:
            bet_type = "1HH"
        elif away in bet_type:
            bet_type = '2HH'
        else:
            bet_type = ''
    
    elif ('basketball' in league or 'nba' in league) and ('1x2 rt' in bet or '1x2' in bet or '1x2 (5.5)' in bet):
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    elif ('basketball' in league or 'nba' in league) and ('1x2 in regular time' in bet):
        if home in bet_type:
            bet_type = "1"
        elif away in bet_type:
            bet_type = '2'
        else:
            bet_type = 'X'

    else:
        bet_type = bet.split(' ')[0]
        bet_selection = bet.split(' ')[1]
        if str(bet_type).lower() == str(home).lower():
            bet_type = 1
        elif str(bet_type).lower() == str(away).lower():
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

