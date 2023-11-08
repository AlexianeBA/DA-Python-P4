import sys
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
        self.view.generic_print("Vous avez fait le choix: " + selected_menu)

        if selected_menu == "1":
            self.create_player()
        elif selected_menu == "2":
            self.display_list_of_players_in_alphabetical_order()
        elif selected_menu == "3":
            created_tournament = self.create_tournament()
            self.ask_to_exit_tournament()
            self.play_tournament(created_tournament)
        elif selected_menu == "4":
            self.create_new_round_and_play_it(tournament=self.tournament)
            self.select_players_for_round()
        elif selected_menu == "5":
            self.resume_tournament()
        elif selected_menu == "6":
            self.display_list_of_tournaments()
        elif selected_menu == "7":
            self.display_list_of_players_from_selected_tournament()
        elif selected_menu == "8":
            self.display_rank_of_players_in_tournament()
        elif selected_menu == "9":
            self.display_all_rounds_of_tournament()
        elif selected_menu == "10":
            self.display_matches_of_one_tournament()
        elif selected_menu == "11":
            self.view.generic_print("Vous avez choisi de quitter le programme.")
            sys.exit()

    # afficher les joueurs
    def display_list_of_players_in_alphabetical_order(self):
        players = self.player.get_all_players()

        if players:
            players.sort(key=lambda player: player.lastname)
            self.view.generic_print(
                "Liste de tous les joueurs triés par ordre alphabétique:"
            )
            for player in players:
                a = player.lastname
                b = player.firstname
                c = player.sexe
                d = player.date_of_birth
                e = player.rank
                self.view.generic_print(
                    f"Nom: {a}, Prénom: {b}, Sexe: {c}, Date de naissance: {d}, Classement: {e}"
                )
        else:
            self.view.generic_print(
                "Aucun joueur n'a été trouvé dans la base de données."
            )

    # création de joueur
    def create_player(self):
        self.view.generic_print("Création de joueur")
        joueur: Player = Player()
        joueur.lastname = self.view.generic_input("Nom de famille : ")
        joueur.firstname = self.view.generic_input("Prénom : ")
        joueur.sexe = self.view.generic_input("Sexe: ")
        joueur.date_of_birth = self.view.generic_input("Date de naissance: ")
        joueur.rank = self.view.generic_input("Niveau: ")
        joueur.player_id = self.view.generic_input("ID: ")
        self.view.generic_print("Le joueur a été créé.")
        # Sauvegarde des données du joueur
        serialized_player = joueur.serialize_player()
        self.player.save_player_in_db(serialized_player)
        self.view.generic_print("Le joueur a été enregistré dans la base de données.")

    # création d'un tournois
    def create_tournament(self):
        self.view.generic_print("Création d'un nouveau tournoi")
        name = self.view.generic_input("Nom du tournoi: ")
        location = self.view.generic_input("Lieu du tournoi: ")
        while True:
            date_str = self.view.generic_input("Date du tournoi (jj/mm/aa): ")
            try:
                date = datetime.strptime(date_str, "%d/%m/%y")
                break
            except ValueError:
                self.view.generic_print(
                    "Format de date invalide. Utilisez le format jj/mm/aa."
                )

        descritpion = self.view.generic_input("Description du tournoi: ")

        new_tournament = Tournament(
            name=name, location=location, date=date, description=descritpion
        )

        self.tournament = new_tournament
        self.tournament.save_tournament_in_db()
        players = self.player.get_all_players()
        player_dict = {}
        self.view.generic_print("Liste des joueurs présents: ")
        for index, player in enumerate(players, start=1):
            player: Player
            player_dict[str(index)] = player
            print(f"{index}: {player.lastname}")

        while len(self.tournament.players) <= 7:
            joueur = self.add_player(player_dict)
            if joueur:
                self.tournament.players.append(joueur)
        serialized_tournament = self.tournament.serialize_tournament()
        self.tournament.update_tournament(serialized_tournament)
        return self.tournament

    # Ajout des joueurs pour le tournois
    def add_player(self, player_dict):
        user_input = self.view.generic_input(
            "Mettez l'index du joueur ou créez en un appuyant sur 'c'"
        )
        if user_input == "c":
            return self.create_player()
        elif user_input in player_dict:
            return player_dict[user_input]
        else:
            self.view.generic_print("Index de joueur invalide. Réessayez.")

    # Lancement du tournois
    def play_tournament(self, tournament: Tournament):
        if not tournament:
            self.view.generic_print(
                "Aucun tournoi n'a été créé. Veuillez d'abord créer un tournoi."
            )
            self.create_tournament()
            return

        while tournament.current_round <= 4:
            self.create_new_round_and_play_it(tournament)

            serialized_tournament = tournament.serialize_tournament()
            tournament.update_tournament(serialized_tournament)

    # création des rounds 1,2,3 et 4
    def create_new_round_and_play_it(self, tournament: Tournament, first_round=True):
        round_number = tournament.current_round
        name_of_round = self.view.generic_input(
            "Ajouter un nom au round" + str(round_number) + ":"
        )

        date_and_hour_start = datetime.now()
        list_of_matchs = []

        if first_round:
            list_of_matchs = self.select_players_for_round()
        else:
            list_of_matchs = self.select_players_for_round(tournament.name)

        for match in list_of_matchs:
            self.play_match(match)

        played_round = Round(
            list_of_matches=list_of_matchs,
            name_of_round=name_of_round,
            date_and_hour_start=date_and_hour_start,
        )
        played_round.date_and_hour_end = datetime.now()
        tournament.rounds.append(played_round)
        tournament.current_round += 1
        serialized_tournament = tournament.serialize_tournament()
        tournament.update_tournament(serialized_tournament)
        self.ask_to_exit_tournament()

    def select_players_for_round(self, first_round=True, tournament_name=None):
        if first_round:
            players = self.player.get_all_players()
            random.shuffle(players)
        else:
            players = self.tournament.get_all_players_of_a_tournament(tournament_name)
            players = sorted(players, key=lambda player: player.score, reverse=True)

        list_matches = []
        for i in range(0, len(players), 2):
            player_1 = players[i]
            player_2 = players[i + 1]
            match = self.create_match(player_1, player_2)
            list_matches.append(match)

        return list_matches

    # Lancement du round
    def play_round(self):
        round: Round = Round()
        self.view.display_round(round)

        for match in round.list_of_matches:
            match = self.play_match(match=match)

        round.date_and_hour_end = datetime.now()

        self.tournament.current_round += 1
        self.tournament.update_tournament(self.tournament.serialize_tournament())
        return round

    # creation des matchs
    def create_match(self, player1: Player, player2: Player):
        player1.add_opponent(player2)
        player2.add_opponent(player1)
        match = Match(player_1=player1, player_2=player2)
        self.round.list_of_matches.append(match)
        self.view.display_match(match)
        return match

    # Attribution des scores
    def play_match(self, match: Match):
        self.view.generic_print(
            f"Match en cours: {match.player_1.lastname} vs {match.player_2.lastname}"
        )

        result = self.view.get_match_result()

        if result == "1":
            match.player_1.update_score("1")
            match.player_2.update_score("0")
            match.player_1_result = 1
            match.player_1.update_rank(1)

        elif result == "2":
            match.player_1.update_score("0")
            match.player_2.update_score("1")
            match.player_2_result = 1
            match.player_2.update_rank(1)
        elif result == "0.5":
            match.player_1.update_score("0.5")
            match.player_2.update_score("0.5")
            match.player_1_result = 0.5
            match.player_2_result = 0.5

        self.view.generic_print(
            f"Le joueur {match.player_1.firstname} a un score de {match.player_1_result}."
        )
        self.view.generic_print(
            f"Le joueur {match.player_2.firstname} a un score de {match.player_2_result}."
        )
        match.player_1.update_player_rank(match.player_1.rank)
        match.player_2.update_player_rank(match.player_2.rank)

        return match

    # méthode générique pour choisir l'index du tournoi
    def selected_tournament_index(self, tournaments):
        if not tournaments:
            self.view.generic_print("Aucun tournoi trouvé.")
            return None

        self.view.generic_print("Liste des tournois disponibles: ")

        dict_of_tournaments = {}
        for i, tournament in enumerate(tournaments):
            self.view.generic_print(f"{i}. {tournament.name}")
            dict_of_tournaments[str(i)] = tournament

        is_tournament_exist = False
        while not is_tournament_exist:
            selected_index = str(
                self.view.generic_input("Sélectionnez le numéro du tournoi : ")
            )
            try:
                # si la clé existe dans le dict alors on return le tournoi
                print(dict_of_tournaments)
                if selected_index in dict_of_tournaments:
                    return dict_of_tournaments[selected_index]
                else:
                    self.view.generic_print("Indice de tournoi invalide.")
            except ValueError:
                self.view.generic_print("Sélection invalide.")
            except Exception as e:
                self.view.generic_print(f"Il y a une erreur {e}")

    # reprendre un tournoi en cours
    def resume_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament: Tournament = self.selected_tournament_index(tournaments)

        if selected_tournament.is_finished():
            self.view.generic_print(
                "Le tournoi est déjà terminé, vous ne pouvez pas le reprendre."
            )
        else:
            self.view.generic_print(f"Reprise du tournoi: {selected_tournament.name}")
            self.play_tournament(selected_tournament)

    # afficher la liste des tournoi disponible
    def display_list_of_tournaments(self):
        tournaments = self.tournament.get_all_tournaments()

        if not tournaments:
            self.view.generic_print("Aucun tournoi trouvé.")
            return

        self.view.generic_print("Liste des tournois disponibles:")

        for i, tournament in enumerate(tournaments, start=1):
            self.view.generic_print(f"{i}. {tournament.name}")

    # afficher la liste des joueurs, par ordre alphabétique, d'un tournoi choisi
    def display_list_of_players_from_selected_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Liste des joueurs du tournoi {selected_tournament.name}"
            )
            players = selected_tournament.players
            for player in players:
                self.view.generic_print(
                    f"ID: {player.player_id} Nom : {player.lastname}, Prénom: {player.firstname}."
                )
        else:
            self.view.generic_print(
                "Aucun joueur trouvé pour le tournoi {selected_tournament.name}"
            )

    # afficher le rang des joueurs d'un tournoi choisi
    def display_rank_of_players_in_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Classement des joueurs du tournoi {selected_tournament.name} :"
            )
            players = selected_tournament.players
            for player in players:
                self.view.generic_print(
                    f"Rang du joueur {player.firstname}: {player.rank}"
                )
        else:
            self.view.generic_print(
                f"Aucun rang de joueurs dans le tournoi {selected_tournament.name}"
            )

    # afficher les rounds d'un tournoi choisi
    def display_all_rounds_of_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Liste des tours du tournoi {selected_tournament.name}"
            )

            rounds = selected_tournament.rounds
            for round in rounds:
                self.view.generic_print(f"{round.name_of_round}")

        else:
            self.view.generic_print(
                f"Aucun tour trouvé pour le tournoi {selected_tournament.name}"
            )

    # afficher la liste des matchs d'un tournoi choisi
    def display_matches_of_one_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Liste des matchs du tournoi {selected_tournament.name}"
            )
            rounds = selected_tournament.rounds
            for round in rounds:
                for serialized_match in round.list_of_matches:
                    match = self.round.deserialize_match(serialized_match)
                    player_1 = match.player_1
                    player_2 = match.player_2
                    player_1_result = match.player_1_result
                    player_2_result = match.player_2_result
                    first_player = f"{player_1['firstname']} {player_1['lastname']}"
                    second_player = f"{player_2['firstname']} {player_2['lastname']}"
                    result = f"{player_1_result} - {player_2_result}"

                    self.view.generic_print(
                        f"Match : {first_player} vs {second_player}, Résultat : {result}"
                    )
        else:
            self.view.generic_print("Aucun match trouvé pour le tournoi sélectionné")

    # Intéraction avec l'utilisateur pour continuer ou quitter le tournoi en cours
    def ask_to_exit_tournament(self):
        user_input = self.view.generic_input(
            "Continuer le tournoi? (Entrez O pour oui et N pour non.)"
        )
        if user_input == "n":
            self.view.generic_print("Vous avez quitté le tournoi.")
            exit(0)
