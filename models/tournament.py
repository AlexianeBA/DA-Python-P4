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
        # self.players: List[Player] = []
        self.rounds: List[Round] = []
        self.description = description
        self.db = TinyDB('db.json')
        self.table = self.db.table("Tournaments")
        self.players: List[Player] = []
        
    def serialize_tournament(self):
        list_players = []
        for player in self.players:
            list_players.append(player.serialize_player())
        
        list_rounds = []
        for round in self.rounds:
            list_rounds.append(round.serialize_round())
        serialize_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "nb_rounds": self.nb_round,
            "current_round": self.current_round,
            "desciption": self.description,
            "players": list_players,
            "rounds": list_rounds,
        }
        return serialize_tournament
    
    def save_tournament_in_db(self):
        serialize_tournament = self.serialize_tournament()
        self.table.insert(serialize_tournament)


    def add_round(self, round):
        self.rounds.append(round)
   
      # trier par score 2eme round
    def add_match(self, match):
        self.current_round = self.get_current_round()
        if self.current_round:
            self.current_round.add_match(match)
        else:
            print("Aucun tour en cours")
    def get_current_round(self):
        if isinstance(self.current_round, int) and 1 <= self.current_round <= len(self.rounds):
            return self.rounds[self.current_round - 1]
        else:
            return None
        
   