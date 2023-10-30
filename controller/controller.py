import sys
from tinydb import TinyDB
from view.vue import View
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from datetime import datetime
import random
import string


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
            created_tournament = self.create_tournament()
            self.ask_to_exit_tournament()
            self.play_tournament(created_tournament)
        if selected_menu == "4":
            self.create_round(tournament=self.tournament)
            self.select_random_players_first_round()
        if selected_menu == "5":
            self.resume_tournament()
        if selected_menu == "6":
            self.display_list_of_tournaments()
        if selected_menu == "7":
            self.display_list_of_players_from_selected_tournament()

        if selected_menu == "8":
            self.display_rank_of_players_in_tournament()
        if selected_menu == "9":
            self.display_all_rounds_of_tournament()
        if selected_menu == "10":
            self.display_matches_of_one_tournament()
        if selected_menu == "11":
            self.view.generic_print("Vous avez choisi de quitter le programme.")
            sys.exit()

    # Génération de l'ID
    def generate_random_id(self):
        numbers = random.choices(string.digits, k=4)
        player_id = "AB" + "".join(numbers)
        return player_id

    # création de joueur
    def create_player(self):
        print(self.view.print_create_player)
        joueur: Player = Player()
        joueur.lastname = self.view.generic_input("Nom de famille : ")
        joueur.firstname = self.view.generic_input("Prénom : ")
        joueur.sexe = self.view.generic_input("Sexe: ")
        joueur.date_of_birth = self.view.generic_input("Date de naissance: ")
        joueur.rank = self.view.generic_input("Niveau: ")
        joueur.player_id = self.generate_random_id()
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

        new_tournament = Tournament(name="Nom du tournoi", location="Lieu", date="Date", description="Description")

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
        serialized_tournament = self.tournament.serialize_tournament()
        self.tournament.update_tournament(serialized_tournament)
        return self.tournament

    # Ajout des joueurs pour le tournois
    def add_player(self, player_dict):
        user_input = self.view.generic_input(
            "Mettez l'index du joueur ou créez en un appuyant sur 'C'"
        )
        if user_input == "C":
            return self.create_player()
        else:
            return player_dict[user_input]

    # Lancement du tournois
    def play_tournament(self, tournament: Tournament):
        if not tournament:
            self.view.generic_print(
                "Aucun tournoi n'a été créé. Veuillez d'abord créer un tournoi."
            )
            self.create_tournament()
            return

        if not tournament.rounds:
            self.view.generic_print(
                "Aucun round n'a été créé. Veuillez d'abord créer un round."
            )

            while tournament.current_round <= 4:
                if tournament.current_round == 1:
                    round = self.create_round(tournament)
                else:
                    round = self.create_rounds_2to_4(tournament)

                for round in tournament.rounds:
                    if round.date_and_hour_end == "":
                        round = self.play_round(round)
                    tournament.current_round += 1
                    serialized_tournament = tournament.serialize_tournament()
                    tournament.update_tournament(serialized_tournament)

        return round

    # création du premier round
    def create_round(self, tournament: Tournament):
        name_of_round = self.view.generic_input("Ajouter un nom au round: ")

        date_and_hour_start = datetime.now()
        list_of_matchs = []
        if tournament.current_round == 1:
            list_of_matchs = self.select_random_players_first_round()

        else:
            list_of_matchs = self.filter_players()
        new_round = Round(
            list_of_matches=list_of_matchs,
            name_of_round=name_of_round,
            date_and_hour_start=date_and_hour_start,
        )
        tournament.rounds.append(new_round)
        serialized_tournament = tournament.serialize_tournament()
        tournament.update_tournament(serialized_tournament)
        self.ask_to_exit_tournament()
        return new_round

    # Lancement du round
    def play_round(self, round: Round):
        self.view.display_round(round)

        for match in round.list_of_matches:
            match = self.match_result(match=match)
            # round.list_of_matches.append(self.match_result(match=match))
        round.date_and_hour_end = datetime.now()
        return round

    def create_match(self, player1: Player, player2: Player):
        player1.add_opponent(player2)
        player2.add_opponent(player1)
        match = Match(player_1=player1, player_2=player2)
        self.view.display_match(match)
        return match

    # Attribution des scores
    def match_result(self, match: Match):
        self.view.generic_print(
            f"Match en cours: {match.player_1.lastname} vs {match.player_2.lastname}"
        )

        result = self.view.get_match_result()

        if result == "1":
            match.player_1.update_score("1")
            match.player_2.update_score("0")
            match.player_1_result = 1
        elif result == "2":
            match.player_1.update_score("0")
            match.player_2.update_score("1")
            match.player_2_result = 1
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

        return match

    # selection aléatoire des joueurs pour le 1er round
    def select_random_players_first_round(self):
        players = self.player.get_all_players()
        random.shuffle(players)
        list_matches = []

        for i in range(0, len(players), 2):
            player_1 = players[i]
            player_2 = players[i + 1]
            match = self.create_match(player_1, player_2)
            list_matches.append(match)

        return list_matches

        # Séléction des joueurs à partir du score
        def select_players_by_score(self, players):
            sorted_players = sorted(
                players, key=lambda player: player.score, reverse=True
            )
            list_of_matches = []

            while len(sorted_players) >= 2:
                player_1 = sorted_players.pop(0)
                player_2 = None

                # Recherche du joueur 2 qui n'a pas encore joué contre le joueur 1
                for opponent in player_1.opponent:
                    if opponent in sorted_players:
                        player_2 = opponent
                        break

                if player_2 is None:
                    # Si le joueur 1 a déjà joué contre tous les autres joueurs disponibles,
                    # choisissez un joueur au hasard parmi les joueurs restants
                    player_2 = random.choice(sorted_players)

                match = self.create_match(player_1, player_2)
                list_of_matches.append(match)

                # Mise à jour de la liste des joueurs restants
                sorted_players.remove(player_2)

            return list_of_matches

    # Intéraction avec l'utilisateur pour continuer ou quitter le tournoi en cours
    def ask_to_exit_tournament(self):
        user_input = self.view.generic_input(
            "Continuer le tournoi? (Entrez O pour oui et N pour non.)"
        )
        if user_input == "n":
            self.view.generic_print("Vous avez quitté le tournoi.")
            exit(0)

    # Création des rounds 2,3,4
    def create_rounds_2to_4(self, tournament: Tournament):
        if not tournament:
            self.view.generic_print(
                "Aucun tournoi n'a été créé. Veuillez d'abord créer un tournoi."
            )
            return

        for current_round in range(2, 5):
            name_of_round = self.view.generic_input(
                f"Ajouter un nom au round {current_round}"
            )
            date_and_hour_start = datetime.now()
            list_of_matchs = self.filter_players()
            new_round = Round(
                list_of_matches=list_of_matchs,
                name_of_round=name_of_round,
                date_and_hour_start=date_and_hour_start,
            )
            tournament.rounds.append(new_round)
            serialized_tournament = tournament.serialize_tournament()
            tournament.update_tournament(serialized_tournament)

    # Filtre des joueurs pour ne pas qu'ils se retouvent l'un contre l'autre plus d'une fois
    def filter_players(self):
        players = self.player.get_all_players()
        sorted_players = sorted(
            players, key=lambda player: self.player.score, reverse=True
        )
        print(sorted_players)
        list_of_matches = []
        while len(sorted_players) > 0:
            for i in range(0, len(sorted_players), 2):
                player_1 = sorted_players[i]
                player_2 = sorted_players[i + 1]
                player_1: Player
                player_2: Player
                if (
                    player_2 not in player_1.opponent
                    and player_1 not in player_2.opponent
                ):
                    match = self.create_match(player_1, player_2)
                    list_of_matches.append(match)
                    sorted_players.remove(player_1)
                    sorted_players.remove(player_2)

                break

        return list_of_matches

    # méthode générique pour choisir l'index du tournoi
    def selected_tournament_index(self, tournaments):
        if not tournaments:
            self.view.generic_print("Aucun tournoi trouvé.")
            return None

        self.view.generic_print("Liste des tournois disponibles")

        for i, tournament in enumerate(tournaments):
            self.view.generic_print(f"{i+1}. {tournament.name}")

        while True:
            selected_index = self.view.generic_input("Sélectionnez le numéro du tournoi : ")
            try:
                selected_index = int(selected_index) - 1
                if 0 <= selected_index < len(tournaments):
                    return selected_index
                else:
                    self.view.generic_print("Indice de tournoi invalide.")
            except ValueError:
                self.view.generic_print("Sélection invalide.")


    # reprendre un tournoi en cours
    def resume_selected_tournament(self, selected_tournament):
        if not selected_tournament:
            self.view.generic_print("Tournoi invalide")
            return

        deserialized_tournament = self.tournament.deserialize_tournament(
        selected_tournament
        )

        if not deserialized_tournament:
            self.view.generic_print("Désérialisation du tournoi échouée.")
            return

        self.view.generic_print(
            f"Tournoi {deserialized_tournament.name} repris avec succès."
        )
    # reprendre un tournoi en cours
    def resume_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_index = self.selected_tournament_index(tournaments)
        if selected_index is not None:
            selected_tournament = tournaments[selected_index]
            self.resume_selected_tournament(selected_tournament)

    # Reprendre le tournoi séléctionné
    def resume_selected_tournament(self, selected_tournament):
        if not selected_tournament:
            self.view.generic_print("Tournoi invalide")
            return

        deserialized_tournament = self.tournament.deserialize_tournament(
            selected_tournament
        )
        self.play_tournament(deserialized_tournament)

        self.view.generic_print(
            f"Tournoi {deserialized_tournament.name} repris avec succès."
        )

    # afficher la liste des tournoi disponible
    def display_list_of_tournaments(self):
        tournaments = self.tournament.get_all_tournaments()

        if not tournaments:
            self.view.generic_print("Aucun tournoi trouvé.")
            return

        self.view.generic_print("Liste des tournois disponibles:")

        for i, tournament in enumerate(tournaments, start=1):
            self.view.generic_print(f"{i}. {tournament.name}")

    # afficher la liste des joueurs d'un tournoi choisi
    def display_list_of_players_from_selected_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_index = self.selected_tournament_index(tournaments)

        if selected_index is not None:
            selected_tournament = tournaments[selected_index]
            self.view.generic_print(f"Joueurs du tournoi {selected_tournament.name} :")
            for player in selected_tournament.players:
                self.view.generic_print(player)

    # afficher le rang des joueurs d'un tournoi choisi
    def display_rank_of_players_in_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_index = self.selected_tournament_index(tournaments)

        if selected_index is not None:
            selected_tournament = tournaments[selected_index]
            self.view.generic_print(
                f"Classement des joueurs du tournoi {selected_tournament.name} :"
            )
            sorted_players = sorted(
                selected_tournament.players,
                key=lambda player: player.score,
                reverse=True,
            )
            for rank, player in enumerate(sorted_players, start=1):
                self.view.generic_print(
                    f"{rank}. {player.name} - Score : {player.score}"
                )

    # afficher les rounds d'un tournoi choisi
    def display_all_rounds_of_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_index = self.selected_tournament_index(tournaments)

        if selected_index is not None:
            selected_tournament = tournaments[selected_index]
            rounds = selected_tournament.rounds

            if not rounds:
                self.view.generic_print("Aucun round trouvé pour ce tournoi.")
        else:
            self.view.generic_print(f"Rounds du tournoi {selected_tournament.name} :")
            for i in enumerate(rounds, start=1):
                self.view.generic_print(f"Round {i}:")

    # afficher la liste des matchs d'un tournoi choisi
    def display_matches_of_one_tournament(self):
        tournaments = self.tournament.get_all_tournaments()
        selected_index = self.selected_tournament_index(tournaments)

        if selected_index is not None:
            selected_tournament = tournaments[selected_index]

        matches = selected_tournament.matches

        if not matches:
            self.view.generic_print(
                f"Aucun match trouvé pour le tournoi {selected_tournament.name}."
            )
        else:
            self.view.generic_print(f"Matchs du tournoi {selected_tournament.name} :")
            for i, match in enumerate(matches, start=1):
                self.view.generic_print(f"Match {i}: {match}")
