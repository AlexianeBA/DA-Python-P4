from models.player import Player

class Match:
    def __init__(self, player_1, player_2, player_1_result, player_2_result):
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.player_1_result = player_1_result
        self.player_2_result = player_2_result
        
    def add_opponent(self):
        self.player_1.add_opponent(self.player_2.firstname)
        self.player_2.add_opponent(self.player_1.firstname)
        return self
        
    def add_match(self):
        add_match = {
            "player_1": self.player_1.add_match(),
            "player_1_result": self.player_1_result.add_match(),
            "player_2": self.player_2.add_match(),
            "player_2_result": self.player_2_result.add_match()
        }
        return add_match