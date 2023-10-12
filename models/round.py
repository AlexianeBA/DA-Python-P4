from typing import List
from models.match import Match

class Round:
    def __init__(self, name_of_round="", date_and_hour_start= "", date_and_hour_end=""):
        self.list_of_matches: List[Match]= []
        self.name_of_round = name_of_round
        self.date_and_hour_start = date_and_hour_start
        self.date_and_hour_end = date_and_hour_end