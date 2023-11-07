from typing import List
from models.match import Match


class Round:
    def __init__(
        self,
        list_of_matches=[],
        name_of_round="",
        date_and_hour_start="",
        date_and_hour_end="",
    ):
        self.list_of_matches: List[Match] = list_of_matches
        self.name_of_round = name_of_round
        self.date_and_hour_start = date_and_hour_start
        self.date_and_hour_end = date_and_hour_end

    def add_match(self, match):
        self.list_of_matches.append(match)

    # mettre à jour le score après chaque tours
    def update_score(self, match: Match, user_response):
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
        serialized_matches = [match.serialize_match() for match in self.list_of_matches]
        serialize_round = {
            "name_of_round": self.name_of_round,
            "list_of_matches": serialized_matches,
            "date_and_hour_start": str(self.date_and_hour_start),
            "date_and_hour_end": str(self.date_and_hour_end),
        }
        return serialize_round

    def deserialize_round(self, round_dict):
        self.name_of_round = round_dict["name_of_round"]
        self.date_and_hour_start = round_dict["date_and_hour_start"]
        self.date_and_hour_end = round_dict["date_and_hour_end"]
        self.list_of_matches = []
        serialized_matches = round_dict["list_of_matches"]

        for serialized_match in serialized_matches:
            match_instance = Match(
                player_1=serialized_match["player_1"],
                player_2=serialized_match["player_2"],
            )
            self.list_of_matches.append(match_instance)
