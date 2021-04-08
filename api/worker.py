import requests
from typing import List


class MatchExtractor(object):
    def __init__(self, source: str = None, booking_code: str = None) -> None:
        self.source = source
        self.booking_code = booking_code

    # def extractor(self) -> List[str]:
    #     pass


class Betway(MatchExtractor):
    pass
#//*[@id="mtSearch"]


class Bet9ja(MatchExtractor):
    pass


class SportyBet(MatchExtractor):
    def __init__(self, country):
        super().__init__(country: str = None)
        pass


class NairaBet(MatchExtractor):
    pass