from models.player import Player


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
            "player_2_result": self.player_2_result,
        }
        return serialize_match

    def deserialize_match(self, deserialized_match):
        match_object = Match(
            player_1=deserialized_match["player_1"],
            player_1_result=deserialized_match["player_1_result"],
            player_2=deserialized_match["player_2"],
            player_2_result=deserialized_match["player_2_result"],
        )
        return match_object
