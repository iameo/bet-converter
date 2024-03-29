from enum import Enum

class BetSources(str, Enum):
    betway = 'betway'
    bet9ja = 'bet9ja'
    sportybet = 'sportybet'
    bet365 = 'bet365'
    x1bet = '1xbet' #1xbet
    msport = 'msport'
    bet22 = '22bet'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))




############### LINKS ##############
link_betway = 'https://betway.com'
link_bet9ja = 'https://web.bet9ja.com/Sport/Default.aspx'
link_sportybet = 'https://www.sportybet.com/ng/sport/football/' #to evade homepage popups
link_1xbet = 'https://1xbet.ng/en/line/' #to evade homepage popups but handles one
link_msport = 'https://www.msport.com/ng/sports'
link_22bet = 'https://22bet.ng/line/'