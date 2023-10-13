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
        
    def add_tournament(self):
        add_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "nb_rounds": self.nb_round,
            "current_round": self.current_round,
            "players": self.players.add_player(),
            "rounds": self.rounds.add_round()
        }
        return add_tournament
    
    def create_tournament():
        pass
    
    def play_tournament():
        pass