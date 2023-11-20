from tinydb import TinyDB, Query


class Player:
    """Represents a participant in a tournament.

    Attributes:
        lastname (str): The last name of the player.
        firstname (str): The first name of the player.
        sexe (str): The gender of the player.
        date_of_birth (str): The date of birth of the player.
        rank (int): The rank of the player.
        score (float): The score of the player.
        player_id (str): The unique identifier for the player.
        opponent (list): List of player IDs faced by the player.
        db (TinyDB): The TinyDB instance used for database operations.
        table (TinyDB.table): The TinyDB table for storing player data.
    """

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
        """Initializes a Player instance.

        Args:
            lastname (str, optional): The last name of the player. Defaults to "".
            firstname (str, optional): The first name of the player. Defaults to "".
            sexe (str, optional): The gender of the player. Defaults to "".
            date_of_birth (str, optional): The date of birth of the player. Defaults to "".
            rank (int, optional): The rank of the player. Defaults to 0.
            score (float, optional): The score of the player. Defaults to 0.
            player_id (str, optional): The unique identifier for the player. Defaults to "".
            opponent (list, optional): List of player IDs faced by the player. Defaults to [].
        """
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
        """Updates the player's score.

        Args:
            score (float): The score to be added to the player's current score.
        """
        self.score += float(score)

    def update_rank(self, rank):
        """Updates the player's rank.

        Args:
            rank (int): The rank to be added to the player's current rank.
        """
        self.rank += int(rank)

    def add_opponent(self, faced_opponent):
        """Adds an opponent to the list of opponents faced by the player.

        Args:
            faced_opponent (Player): The opponent faced by the player.
        """
        faced_opponent: Player = faced_opponent
        self.opponent.append(faced_opponent.player_id)

    def serialize_player(self):
        """Serializes the Player instance to a dictionary.

        Returns:
            dict: A dictionary containing serialized player information.
        """
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
        """Retrieves a list of all players from the database.

        Returns:
            list: A list of Player instances representing all players.
        """
        players = self.db.table("Players").all()
        list_of_players = []
        for player in players:
            deserialized_player = self.deserialize_player(player)
            list_of_players.append(deserialized_player)
        return list_of_players

    @staticmethod
    def deserialize_player(player_dict):
        """Creates a Player instance from a serialized dictionary.

        Args:
            player_dict (dict): A dictionary containing serialized player information.

        Returns:
            Player: A Player instance created from the provided dictionary.
        """
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
        """Saves a player in the database.

        Args:
            player (Player): The Player instance to be saved in the database.
        """
        self.table.insert(player)

    def update_player_rank(self, new_rank):
        """Updates the rank of the player in the database.

        Args:
            new_rank (int): The new rank of the player.
        """
        player_id = self.player_id
        query_player_id = Query()
        player = self.table.get(query_player_id.player_id == player_id)
        if player:
            self.table.update(
                {"rank": new_rank}, query_player_id.player_id == player_id
            )

    def update_player_score(self, new_score):
        """Updates the score of the player in the database.

        Args:
            new_score (float): The new score of the player.
        """
        player_id = self.player_id
        query_player_id = Query()
        player = self.table.get(query_player_id.player_id == player_id)
        if player:
            self.table.update(
                {"score": new_score}, query_player_id.player_id == player_id
            )
