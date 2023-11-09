from models.player import Player
from tinydb import TinyDB
from models.round import Round
from models.match import Match


class View:
    """Represents the view for interacting with the chess tournament application."""

    def __init__(self):
        """Initializes a View instance.

        Attributes:
            player (Player): An instance of the Player class.
            db (TinyDB): The TinyDB database instance.
            round (Round): An instance of the Round class.
        """
        self.player: Player = Player()
        self.db = TinyDB("db.json")
        self.round: Round = Round()

    def display_menu(self):
        """Displays the main menu options for the chess tournament application."""
        menu = """
1: Ajouter des joueurs
2: Afficher la liste des joueurs
3: Créer un tournoi
4: Reprendre un tournoi en cours
5: Afficher la liste des tournois
6: Afficher la liste des joueurs d'un tournoi
7: Afficher le classement des joueurs d'un tounoi
8: Afficher les tours d'un tournoi
9: Afficher tous les matchs d'un tounoi
10: Quitter"""
        self.generic_print(menu)

    # afficher la liste des tours avec les joueurs
    def display_round(self, round: Round):
        """Displays details of a tournament round.

        Args:
            round (Round): An instance of the Round class.
        """
        print("Détail du round: ")
        print(f"Nom du round: {round.name_of_round}")
        print(f"Date et heure de début: {round.date_and_hour_start}")

    # afficher la liste des matchs avec les joueurs
    def display_match(self, match: Match):
        """Displays details of a tournament match.

        Args:
            match (Match): An instance of the Match class.
        """
        print("Le joueur 1 est: ", match.player_1.firstname, match.player_1.lastname)
        print(f"Score Joueur 1: {match.player_1_result}\n")
        print("Le joueur 2 est : ", match.player_2.firstname, match.player_2.lastname)
        print(f"Score Joueur 2: {match.player_2_result}\n")

    def generic_print(self, sentance_print):
        """Generic methods to print message.

        Args:
            sentence_print (str): The message to be displayed.
        """
        print(sentance_print)

    def generic_input(self, sentance_input):
        """Generic methods to get user input.

        Args:
            sentence_input (str): The input prompt.

        Returns:
            str: The user input.
        """
        input_to_return = input(sentance_input)
        return input_to_return

    def get_match_result(self):
        """Gets the result of a tournament match from user input.

        Returns:
            str: The result (1 for player 1, 2 for player 2, or 0.5 for a draw).
        """
        result = input(
            "Entrez le gagant : 1 pour le joueur 1, 2 pour le joueur 2 ou 0.5 pour match nul."
        )
        if result in ("1", "2", "0.5"):
            return result
        else:
            print("Valeur invalide. Veuillez entrer 1,2 ou 0.5.")
