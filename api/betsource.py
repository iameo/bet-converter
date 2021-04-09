from enum import Enum

class BetSources(str, Enum):
    betway = 'betway'
    bet9ja = 'bet9ja'
    sportybet = 'sportybet'
    bet365 = 'bet365'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

