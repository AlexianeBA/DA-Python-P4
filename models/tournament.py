from typing import List
from models.round import Round
from models.player import Player
from tinydb import TinyDB, Query


class Tournament:
    """Represents a chess tournament.

    Attributes:
        name (str): The name of the tournament.
        location (str): The location where the tournament is held.
        date (str): The date when the tournament takes place.
        description (str): A description or additional information about the tournament.
        current_round (int): The current round of the tournament.
        nb_rounds (int): The total number of rounds in the tournament.
        rounds (List[Round]): List of Round instances in the tournament.
        players (List[Player]): List of Player instances participating in the tournament.
    """

    def __init__(
        self,
        name="",
        location="",
        start_date="",
        end_date="",
        description="",
        current_round=1,
        nb_rounds=4,
        players=[],
        rounds=[],
    ):
        """Initializes a Tournament instance.

        Args:
            name (str, optional): The name of the tournament. Defaults to "".
            location (str, optional): The location where the tournament is held. Defaults to "".
            date (str, optional): The date when the tournament takes place. Defaults to "".
            description (str, optional): A description or additional information about the tournament. Defaults to "".
            current_round (int, optional): The current round of the tournament. Defaults to 1.
            nb_rounds (int, optional): The total number of rounds in the tournament. Defaults to 4.
            players (List[Player], optional): List of Player instances participating in the tournament. Defaults to [].
            rounds (List[Round], optional): List of Round instances in the tournament. Defaults to [].
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.nb_rounds = nb_rounds
        self.current_round = current_round
        self.rounds: List[Round] = rounds
        self.description = description
        self.db = TinyDB("db.json")
        self.table = self.db.table("Tournaments")
        self.players: List[Player] = players
        self.player: Player = Player()
        self.round: Round = Round()

    def serialize_tournament(self):
        """Serializes the Tournament instance to a dictionary.

        Returns:
            dict: A dictionary containing serialized tournament information.
        """
        list_players = []
        for player in self.players:
            list_players.append(player.serialize_player())

        list_rounds = []
        for round in self.rounds:
            list_rounds.append(round.serialize_round())

        serialize_tournament = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "nb_rounds": self.nb_rounds,
            "current_round": self.current_round,
            "description": self.description,
            "players": list_players,
            "rounds": list_rounds,
        }
        return serialize_tournament

    def save_tournament_in_db(self):
        """Saves the serialized tournament information in the database."""
        serialize_tournament = self.serialize_tournament()
        self.table.insert(serialize_tournament)

    def is_finished(self):
        """Checks if the tournament has finished.

        Returns:
            bool: True if the tournament has finished, False otherwise.
        """
        return self.current_round > self.nb_rounds

    def update_tournament(self, serialized_tournament):
        """Updates the tournament information in the database.

        Args:
            serialized_tournament (dict): A dictionary containing serialized tournament information.
        """
        QueryTournament = Query()
        self.table.update(
            serialized_tournament, QueryTournament.name == serialized_tournament["name"]
        )

    def deserialize_tournament(self, serialized_tournament):
        """Deserializes a dictionary to create a Tournament instance.

        Args:
            serialized_tournament (dict): A dictionary containing serialized tournament information.

        Returns:
            Tournament: A Tournament instance created from the provided dictionary.
        """
        if isinstance(serialized_tournament, dict):
            tournament_object = Tournament(
                name=serialized_tournament["name"],
                location=serialized_tournament["location"],
                start_date=serialized_tournament["start_date"],
                end_date=serialized_tournament["end_date"],
                nb_rounds=serialized_tournament["nb_rounds"],
                current_round=serialized_tournament["current_round"],
                description=serialized_tournament["description"],
            )
            tournament_object.players = [
                self.player.deserialize_player(player_dict)
                for player_dict in serialized_tournament["players"]
            ]

            tournament_object.rounds = [
                self.round.deserialize_round(round_dict)
                for round_dict in serialized_tournament["rounds"]
            ]

            return tournament_object

    def get_all_tournaments(self):
        """Gets a list of all tournaments from the database.

        Returns:
            List[Tournament]: A list of Tournament instances.
        """
        tournaments = self.db.table("Tournaments").all()
        list_of_tournaments = []

        for tournament in tournaments:
            deserialized_tournament = self.deserialize_tournament(tournament)
            list_of_tournaments.append(deserialized_tournament)
        return list_of_tournaments

    def get_all_players_of_a_tournament(self, tournament_name):
        """Gets the list of players from a specific tournament.

        Args:
            tournament_name (str): The name of the tournament.

        Returns:
            List[Player]: A list of Player instances participating in the tournament.
        """
        tournaments = self.db.table("Tournaments")
        players_list = []
        for tournament_key in tournaments.all():
            tournament_data = tournaments.get(doc_id=tournament_key.doc_id)
            if tournament_data["name"] == tournament_name:
                players_list = tournament_data.get("players", [])
                return players_list
        return players_list
