from models.player import Player
from tinydb import TinyDB
from models.round import Round
from models.match import Match


class View:
    def __init__(self):
        self.player: Player = Player()
        self.db = TinyDB("db.json")
        self.round: Round = Round()

    def display_menu(self):
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
        print("Détail du round: ")
        print(f"Nom du round: {round.name_of_round}")
        print(f"Date et heure de début: {round.date_and_hour_start}")

    # afficher la liste des matchs avec les joueurs
    def display_match(self, match: Match):
        print("Le joueur 1 est: ", match.player_1.firstname, match.player_1.lastname)
        print(f"Score Joueur 1: {match.player_1_result}\n")
        print("Le joueur 2 est : ", match.player_2.firstname, match.player_2.lastname)
        print(f"Score Joueur 2: {match.player_2_result}\n")

    def generic_print(self, sentance_print):
        print(sentance_print)

    def generic_input(self, sentance_input):
        input_to_return = input(sentance_input)
        return input_to_return

    def get_match_result(self):
        result = input(
            "Entrez le gagant : 1 pour le joueur 1, 2 pour le joueur 2 ou 0.5 pour match nul."
        )
        if result in ("1", "2", "0.5"):
            return result
        else:
            print("Valeur invalide. Veuillez entrer 1,2 ou 0.5.")
