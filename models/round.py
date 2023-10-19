from typing import List
from models.match import Match
from models.player import Player
class Round:
    def __init__(self, name_of_round="", date_and_hour_start= "", date_and_hour_end=""):
        
        self.list_of_matches: List[Match]= []
        self.name_of_round = name_of_round
        self.date_and_hour_start = date_and_hour_start
        self.date_and_hour_end = date_and_hour_end
        
    #création d'une liste de matches pour un tournoi    
    def create_list_of_matches(self, player_group_1, player_group_2):
        for player_1, player_2 in zip(player_group_1, player_group_2):
            player_1: Player = player_1
            player_2: Player = player_2
            match = Match(player_1, player_2, 0,0)
            self.list_of_matches.append(match.add_opponent())
            
       
    
    #mettre à jour le score après chaque tours
    def update_score(self,user_response):
        match: Match=Match()
        if user_response == "1":
            match.player_1.update_score(1)
            match.player_1_result += 1
            print("gagant joueur 1")
        elif user_response == "2":
            print("gagnant joueur 2")
            match.player_2.update_score(1)
            match.player_2_result += 1
        elif user_response == "0":
            print("match nul")
            match.player_1.update_score(1)
            match.player_1_result += 0.5
            match.player_2.update_score(1)
            match.player_2_result += 0.5
            
    
    def serialize_round(self):
        serialize_round= {
            "name_of_round": self.name_of_round,
            "list_of_matches": self.list_of_matches,
            "date_and_hour_start": self.date_and_hour_start,
            "date_and_hour_end": self.date_and_hour_end
        }
        return serialize_round
        