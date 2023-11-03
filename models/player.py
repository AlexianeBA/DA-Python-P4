from tinydb import TinyDB, Query


class Player:
    def __init__(
        self,
        lastname="",
        firstname="",
        sexe="",
        date_of_birth="",
        rank=0,
        score=0,
        player_id="",
        opponent=[],
    ):
        self.lastname = lastname
        self.firstname = firstname
        self.sexe = sexe
        self.date_of_birth = date_of_birth
        self.rank = rank
        self.score = score
        self.player_id = player_id
        self.opponent = opponent
        self.db = TinyDB("db.json")
        self.table = self.db.table("Players")

    def update_score(self, score):
        self.score += float(score)

    def update_rank(self, rank):
        self.rank += int(rank)

    def add_opponent(self, faced_opponent):
        faced_opponent: Player = faced_opponent
        self.opponent.append(faced_opponent.player_id)

    def serialize_player(self):
        serialize_player = {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "sexe": self.sexe,
            "date_of_birth": self.date_of_birth,
            "rank": self.rank,
            "score": self.score,
            "player_id": self.player_id,
            "opponent": self.opponent,
        }
        return serialize_player

    # récupérer la liste des joueurs
    def get_all_players(self):
        players = self.db.table("Players").all()
        list_of_players = []
        for player in players:
            deserialized_player = self.deserialize_player(player)
            list_of_players.append(deserialized_player)
        return list_of_players

    def deserialize_player(self, player_dict):
        player_object = Player(
            lastname=player_dict["lastname"],
            firstname=player_dict["firstname"],
            sexe=player_dict["sexe"],
            date_of_birth=player_dict["date_of_birth"],
            rank=int(player_dict["rank"]),
            score=player_dict["score"],
            player_id=player_dict["player_id"],
            opponent=player_dict["opponent"],
        )
        return player_object

    # sauvgarder joueur
    def save_player_in_db(self, player):
        self.table.insert(player)

    def update_player_rank(self, new_rank):
        player_id = self.player_id
        query_player_id = Query()
        player = self.table.get(query_player_id.player_id == player_id)
        if player:
            self.table.update(
                {"rank": new_rank}, query_player_id.player_id == player_id
            )
