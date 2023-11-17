from typing import List
from models.match import Match
from models.player import Player


class Round:
    """Represents a round in a tournament.

    Attributes:
        list_of_matches (List[Match]): List of Match instances in the round.
        name_of_round (str): The name or identifier of the round.
        date_and_hour_start (str): The start date and time of the round.
        date_and_hour_end (str): The end date and time of the round.
    """

    def __init__(
        self,
        list_of_matches=[],
        name_of_round="",
        date_and_hour_start="",
        date_and_hour_end="",
    ):
        """Initializes a Round instance.

        Args:
            list_of_matches (List[Match], optional): List of Match instances in the round. Defaults to [].
            name_of_round (str, optional): The name or identifier of the round. Defaults to "".
            date_and_hour_start (str, optional): The start date and time of the round. Defaults to "".
            date_and_hour_end (str, optional): The end date and time of the round. Defaults to "".
        """
        self.list_of_matches: List[Match] = list_of_matches
        self.name_of_round = name_of_round
        self.date_and_hour_start = date_and_hour_start
        self.date_and_hour_end = date_and_hour_end

    def serialize_round(self):
        """Serializes the Round instance to a dictionary.

        Returns:
            dict: A dictionary containing serialized round information.
        """
        serialized_matches = [match.serialize_match() for match in self.list_of_matches]
        serialize_round = {
            "name_of_round": self.name_of_round,
            "list_of_matches": serialized_matches,
            "date_and_hour_start": str(self.date_and_hour_start),
            "date_and_hour_end": str(self.date_and_hour_end),
        }
        return serialize_round

    def deserialize_round(self, round_dict):
        """Deserializes a dictionary to create a Round instance.

        Args:
            round_dict (dict): A dictionary containing serialized round information.

        Returns:
            Round: A Round instance created from the provided dictionary.
        """
        self.name_of_round = round_dict["name_of_round"]
        self.date_and_hour_start = round_dict["date_and_hour_start"]
        self.date_and_hour_end = round_dict["date_and_hour_end"]
        self.list_of_matches = []

        for serialized_match in round_dict["list_of_matches"]:
            match_instance = Match(
                player_1=Player(
                    lastname=serialized_match["player_1"]["lastname"],
                    firstname=serialized_match["player_1"]["firstname"],
                    sexe=serialized_match["player_1"]["sexe"],
                    date_of_birth=serialized_match["player_1"]["date_of_birth"],
                    rank=serialized_match["player_1"]["rank"],
                    score=serialized_match["player_1"]["score"],
                    player_id=serialized_match["player_1"]["player_id"],
                    opponent=serialized_match["player_1"]["opponent"],
                ),
                player_2=Player(
                    lastname=serialized_match["player_2"]["lastname"],
                    firstname=serialized_match["player_2"]["firstname"],
                    sexe=serialized_match["player_2"]["sexe"],
                    date_of_birth=serialized_match["player_2"]["date_of_birth"],
                    rank=serialized_match["player_2"]["rank"],
                    score=serialized_match["player_2"]["score"],
                    player_id=serialized_match["player_2"]["player_id"],
                    opponent=serialized_match["player_2"]["opponent"],
                ),
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
