from models.player import Player


class Match:
    """Represents a match between two players in a tournament.

    Attributes:
        player_1 (Player): The first player participating in the match.
        player_2 (Player): The second player participating in the match.
        player_1_result (int): The result of the match for player_1.
        player_2_result (int): The result of the match for player_2.
    """

    def __init__(self, player_1, player_2, player_1_result=0, player_2_result=0):
        """Initializes a Match instance.

        Args:
            player_1 (Player): The first player participating in the match.
            player_2 (Player): The second player participating in the match.
            player_1_result (int, optional): The result of the match for player_1. Defaults to 0.
            player_2_result (int, optional): The result of the match for player_2. Defaults to 0.
        """
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.player_1_result = player_1_result
        self.player_2_result = player_2_result

    def serialize_match(self):
        """Serializes the Match instance to a dictionary.

        Returns:
            dict: A dictionary containing serialized match information.
        """
        serialize_match = {
            "player_1": self.player_1.serialize_player(),
            "player_1_result": self.player_1_result,
            "player_2": self.player_2.serialize_player(),
            "player_2_result": self.player_2_result,
        }
        return serialize_match

    @staticmethod
    def deserialize_match(deserialized_match):
        """Creates a Match instance from a serialized dictionary.

        Args:
            deserialized_match (dict): A dictionary containing deserialized match information.

        Returns:
            Match: A Match instance created from the provided dictionary.
        """
        match_object = Match(
            player_1=deserialized_match["player_1"],
            player_1_result=deserialized_match["player_1_result"],
            player_2=deserialized_match["player_2"],
            player_2_result=deserialized_match["player_2_result"],
        )
        return match_object
