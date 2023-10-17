from typing import List
from models.round import Round
from models.player import Player
from tinydb import TinyDB, Query

class Tournament:
    def __init__(self, name="", location="", date="", description=""):
        self.name = name 
        self.location = location
        self.date= date
        self.nb_round= 4
        self.current_round = 1
        self.players: List[Player] = []
        self.rounds: List[Round] = []
        self.description = description
        self.db = TinyDB('db.json')
        self.table = self.db.table("Tournaments")
        self.player:Player = Player()
        
    def serialize_tournament(self):
        
        serialize_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "nb_rounds": self.nb_round,
            "current_round": self.current_round,
            "desciption": self.description,
            "players": self.player.get_all_players(),
            # "rounds": self.rounds.add_round()
        }
        return serialize_tournament
    
    def save_tournament_in_db(self):
        serialize_tournament = self.serialize_tournament()
        self.table.insert(serialize_tournament)



    
    