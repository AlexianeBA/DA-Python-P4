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

        for serialized_match in round_dict["list_of_matches"]:
            match_instance = Match(
                player_1=serialized_match["player_1"],
                player_2=serialized_match["player_2"],
                player_1_result=serialized_match["player_1_result"],
                player_2_result=serialized_match["player_2_result"],
            )
            self.list_of_matches.append(match_instance)

        deserializer_round = Round(
            name_of_round=round_dict["name_of_round"],
            date_and_hour_start=["date_and_hour_start"],
            date_and_hour_end=["date_and_hour_end"],
            list_of_matches=self.list_of_matches,
        )

        return deserializer_round
