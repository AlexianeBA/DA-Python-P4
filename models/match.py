from models.player import Player
# creer un match id
class Match:
    def __init__(self, player_1, player_2, player_1_result=0, player_2_result=0):
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.player_1_result = player_1_result
        self.player_2_result = player_2_result
    
    def serialize_match(self):
        serialize_match = {
            "player_1": self.player_1.serialize_player(),
            "player_1_result": self.player_1_result,
            "player_2": self.player_2.serialize_player(),
            "player_2_result": self.player_2_result
        }
        return serialize_match
     
    # # à supprimer  
    # def add_opponent(self):
    #     self.player_1.add_opponent(self.player_2.firstname)
    #     self.player_2.add_opponent(self.player_1.firstname)
    #     return self
        
   