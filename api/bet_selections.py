###### SOURCE: BET9JA#######

def bet9ja_to_1xbet(bet):
    pass

def bet9ja_to_22bet(bet):
    pass

def bet9ja_to_msport(bet):
    pass


###### SOURCE: 1XBET#######

def x1bet_to_bet9ja(bet, team, league):
    bet_type = ''
    bet_selection = ''
    home = team.split(' - ')[0].lower()
    away = team.split(' - ')[1].lower()

    if 'qualify' in bet:
        bet_type = bet.rsplit(' - ')[1]
        bet_selection = bet.rsplit(' - ')[0]
    elif 'total over' in bet:
        bet_type = bet.split(' ', 1)[1]
        bet_selection = bet.split(' ', 1)[0]
    elif 'to win by (3way)' in bet:
        bet_type = bet.split('.')[1]
        bet_selection = bet.split('.')[0]
    elif 'double chance' in bet:
        bet_type = bet.split(' ', 2)[1]
        if home in bet_type and away in bet_type:
            bet_type = "12"
        elif home in bet_type:
            bet_type = "1X"
        elif away in bet_type:
            bet_type = 'X2'
        else:
            bet_type = ''

        bet_selection = bet.split(' ', 2)[0]

    elif 'basketball' in league and '1x2' in bet:
        if home in bet_type:
            bet_type = "1HH"
        elif away in bet_type:
            bet_type = 'X2'
        else:
            bet_type = ''
  

    else:
        bet_type = bet.split(' ')[1]
        bet_selection = bet.split(' ')[0]

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

