from typing import List
from models.round import Round
from models.player import Player


class Tournament:
    def __init__(self, name="", location="", date="", nb_round=4, description=""):
        self.name = name 
        self.location = location
        self.date= date
        self.nb_round= nb_round
        self.current_round = 1
        self.players: List[Player] = []
        self.rounds: List[Round] = []
        self.description = description
        
    