from models.player import Player

class Match:
    def __init__(self, player_1, player_2, player_1_result, player_2_result):
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.player_1_result = player_1_result
        self.player_2_result = player_2_result