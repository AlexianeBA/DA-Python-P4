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
        
        serialize_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "nb_rounds": self.nb_round,
            "current_round": self.current_round,
            "desciption": self.description,
            "players": self.players,
            "rounds": self.rounds
        }
        return serialize_tournament
    
    def save_tournament_in_db(self):
        serialize_tournament = self.serialize_tournament()
        self.table.insert(serialize_tournament)

    # 1er round
    def create_round(self):
        
        if self.current_round <= self.nb_round:
            players = self.player.get_all_players()
            if len(players)<8:
                print("Il n'y a pas assez de joueurs")
                return
            player_group_1 = players[0:4]
            player_group_2 = players[4:8]
            
            round_name = f"Round {self.current_round} - {self.name}"
            new_round = Round(name_of_round=round_name)
            new_round.create_list_of_matches(player_group_1, player_group_2)
            self.rounds.append(new_round)
            self.current_round += 1
            print(f"Round {self.current_round} - {self.name} créé.")
            
        else:
            print("Le tournoi est terminé.")

    
      # trier par score 2eme round
    