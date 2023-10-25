# fonction pour faire tourner le script qui permet de :
# afficher le menu
# ajouter des joueurs à la base de données (appler methode vue (input))
# créer un tournoi
# lancer un tournoi
# afficher la liste des joueurs
# afficher la liste des joueurs du tournoi
# afficher les tours du tournoi
# afficher les matchs du tounoi
# afficher le resultat du tournoi
# afficher le classement des joueurs
from tinydb import TinyDB
from view.vue import View
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from datetime import datetime
import random


class Controller:
    def __init__(self, object_view: View):
        self.view = object_view
        self.player: Player = Player()
        self.tournament: Tournament = Tournament()
        self.view = object_view
        self.db = TinyDB("db.json")
        TinyDB.default_table_name = "Players"
        self.players_table = self.db.table("Players")
        self.tournament_table = self.db.table("Tournaments")
        self.rounds = []
        self.round: Round = Round()

    def start(self):
        self.view.display_menu()
        selected_menu = self.view.generic_input("Sélectionnez une option: ")
        print(selected_menu)

        if selected_menu == "1":
            add_player = self.create_player()
            print(add_player)
        if selected_menu == "2":
            self.view.display_list_of_players()
        if selected_menu == "3":
            create_tournament = self.create_tournament()
            print(create_tournament)
        if selected_menu == "4":
            # play_tournament = self.play_tournament()
            # print(play_tournament)
            self.create_round()
            self.select_random_players_first_round()
        if selected_menu == "5":
            display_list_tournaments = self.view.diplay_tournaments()
            print(display_list_tournaments)
        if selected_menu == "6":
            display_list_of_players_from_tournament = (
                self.view.display_list_of_player_from_tournament()
            )
            print(display_list_of_players_from_tournament)
        if selected_menu == "7":
            display_ranking_players_of_tournament = (
                self.view.display_ranking_players_of_tournament()
            )
            print(display_ranking_players_of_tournament)
        if selected_menu == "8":
            display_rounds_of_tournament = self.view.display_rounds_tournament()
            print(display_rounds_of_tournament)
        if selected_menu == "9":
            display_list_matchs_of_tournament = (
                self.view.display_list_matchs_of_tournament()
            )
            print(display_list_matchs_of_tournament)
        if selected_menu == "10":
            pass

    # création de joueur
    def create_player(self):
        print(self.view.print_create_player)
        joueur: Player = Player()
        joueur.lastname = self.view.generic_input("Nom de famille : ")
        joueur.firstname = self.view.generic_input("Prénom : ")
        joueur.sexe = self.view.generic_input("Sexe: ")
        joueur.date_of_birth = self.view.generic_input("Date de naissance: ")
        joueur.rank = self.view.generic_input("Niveau: ")
        joueur.player_id = self.view.generic_input("Identifiant: ")
        self.view.player_create()
        # Sauvegarde des données du joueur
        serialized_player = joueur.serialize_player()
        self.player.save_player_in_db(serialized_player)
        self.view.player_save()

    # création d'un tournois
    def create_tournament(self):
        print(self.view.generic_print("Création d'un nouveau tournoi"))
        name = self.view.generic_input("Nom du tournoi: ")
        location = self.view.generic_input("Lieu du tournoi: ")
        date = self.view.generic_input("Date du tournoi: ")
        # nb_round = self.tournament.nb_rounds
        descritpion = self.view.generic_input("Description du tournoi: ")

        new_tournament = Tournament(name, location, date, descritpion)

        self.tournament = new_tournament
        self.tournament.save_tournament_in_db()
        players = self.player.get_all_players()
        player_dict = {}
        print(self.view.generic_print("Liste des joueurs présents: "))
        for index, player in enumerate(players, start=1):
            player: Player
            player_dict[str(index)] = player
            print(f"{index}: {player.lastname}")

        while len(self.tournament.players) <= 7:
            joueur = self.add_player(player_dict)
            self.tournament.players.append(joueur)
        self.tournament.save_tournament_in_db()
        self.create_round()
        # ajouter un input ou on demande à l'user si il veut quitter ou si il veut lancer le tournoi. si il veut le lancer alors la fonction create round se lance sinon on quitte l(e script
        # self.view.rest_of_tournament()

    def add_player(self, player_dict):
        user_input = self.view.generic_input(
            "Mettez l'index du joueur ou créez en un appuyant sur 'C'"
        )
        if user_input == "C":
            return self.create_player()
        else:
            return player_dict[user_input]

    def play_tournament(self):
        if not self.tournament:
            self.view.generic_print(
                "Aucun tournoi n'a été créé. Veuillez d'abord créer un tournoi."
            )
            self.create_tournament()
            return

        if not self.tournament.rounds:
            self.view.generic_print(
                "Aucun round n'a été créé. Veuillez d'abord créer un round."
            )
            self.create_round

        while not self.tournament.is_finished():
            current_round = self.tournament.get_current_round()

            if current_round:
                self.view.generic_print(f"Tour en cours: {current_round.name_of_round}")

                for match in current_round.list_of_matches:
                    self.play_match(match)
                    self.view.generic_print("Voulez-vous quitter le tournoi maintenant ? (Entrez 'O' pour oui, 'N' pour non)")
                    user_input = self.view.generic_input()
                if user_input.lower() == 'o':
                    self.quit_tournament()
                    return

            else:
                self.view.generic_print(
                    "Tous les rounds ont été joués. Le tournoi est terminé."
                )

            self.view.generic_print("Le tournoi est terminé.")

        # 1er round

    def create_round(self):
        name_of_round = self.view.generic_input("Ajouter un nom au round: ")
        date_and_hour_start = datetime.now()
        new_round = Round(name_of_round, date_and_hour_start)
        
        self.tournament.rounds.append(new_round)
        self.view.display_round()
        self.select_random_players_first_round()
        
        round_data = {
            "name": new_round.name_of_round,
            "list_of_matches": new_round.list_of_matches,
            "date_and_hour_start": new_round.date_and_hour_start,
            "date_and_hour_end": new_round.date_and_hour_end
        }
        
        self.tournament.add_round_to_db(round_data)

    def create_match(self, player1, player2):
        match = Match(player_1=player1, player_2=player2)
        self.tournament.add_match(match)
        self.view.display_match(match)
        return match

    def match_result(self, match: Match):
        self.view.generic_print(
            f"Match en cours: {match.player_1.lastname} vs {match.player_2.lastname}"
        )

        result = self.view.get_match_result()

        if result == "1":
            match.player_1.update_score("1")
            match.player_2.update_score("0")
        elif result == "2":
            match.player_1.update_score("0")
            match.player_2.update_score("1")
        elif result == "0.5":
            match.player_1.update_score("0.5")
            match.player_2.update_score("0.5")

        self.view.generic_print(
            "Le joueur {match.player_1.firstname} a un score de {match.player_1.score}."
        )
        self.view.generic_print(
            "Le joueur {match.player_2.firstname} a un score de {match.player_2.score}."
        )

    def select_random_players_first_round(self):
        players = self.player.get_all_players()
        random.shuffle(players)

        current_round = self.tournament.get_current_round()
        if current_round:
            for i in range(0, len(players), 2):
                player_1 = players[i]
                player_2 = players[i + 1]
                match = self.create_match(player_1, player_2)
                self.match_result(match)
        else:
            self.view.generic_print("Aucun tour en cours.")

    def quit_tournament(self):
        self.view.generic_print(
            "Quitter le tournoi? (Entrez O pour oui et N pour non.)"
        )
        user_input = self.view.generic_input()
        if user_input == "O":
            self.tournament = None
            self.view.generic_print("Le tournoi est quitté.")
