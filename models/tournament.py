from typing import List
from models.round import Round
from models.player import Player
from tinydb import TinyDB, Query


class Tournament:
    def __init__(
        self,
        name="",
        location="",
        date="",
        description="",
        current_round=1,
        nb_round=4,
        players=[],
        rounds=[],
    ):
        self.name = name
        self.location = location
        self.date = date
        self.nb_round = nb_round
        self.current_round = current_round
        # self.players: List[Player] = []
        self.rounds: List[Round] = rounds
        self.description = description
        self.db = TinyDB("db.json")
        self.table = self.db.table("Tournaments")
        self.players: List[Player] = players
        self.player: Player = Player()
        self.round: Round = Round()

    def serialize_tournament(self):
        list_players = []
        for player in self.players:
            list_players.append(player.serialize_player())

        list_rounds = []
        for round in self.rounds:
            list_rounds.append(round.serialize_round())
        serialize_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "nb_round": self.nb_round,
            "current_round": self.current_round,
            "description": self.description,
            "players": list_players,
            "rounds": list_rounds,
        }
        return serialize_tournament

    def save_tournament_in_db(self):
        serialize_tournament = self.serialize_tournament()
        self.table.insert(serialize_tournament)

    def add_round(self, round):
        self.rounds.append(round)

    def is_finished(self):
        return self.current_round >= self.nb_round

    def update_tournament(self, serialized_tournament):
        QueryTournament = Query()
        self.table.update(
            serialized_tournament, QueryTournament.name == serialized_tournament["name"]
        )

    def deserialize_tournament(self, serialized_tournament):
        tournament_object = Tournament(
            name=serialized_tournament["name"],
            location=serialized_tournament["location"],
            date=serialized_tournament["date"],
            nb_round=serialized_tournament["nb_round"],
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

    def get_tournament(self, name_tournament):
        QueryTournament = Query()
        p = self.table.search(QueryTournament.name == name_tournament)
        return p

    def get_all_tournaments(self):
        tournaments = self.db.table("Tournaments").all()
        list_of_tournaments = []

        for tournament in tournaments:
            deserialized_tournament = self.deserialize_tournament(tournament)
            list_of_tournaments.append(deserialized_tournament)
        return list_of_tournaments
