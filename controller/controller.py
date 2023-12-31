import sys
from tinydb import TinyDB
from view.vue import View
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from datetime import datetime
import random
from tabulate import tabulate


class Controller:
    """
    Controller class for managing a tournament system.

    Args:
    - object_view (View): An instance of the View class.

    Attrubutes:
    - view (View): An instance of the View class.
    - player (Player):  An instance of the Player class.
    - tournament (Tournament):  An instance of the Tournament class.
    - db (TinyDB): Database instance.
    - player_table (Table): Table for storing player data.
    - tournament_table (Table): Table for storing tournament data.
    - rounds (list): List to store tournament rounds.
    - round (Round): An instance of the Round class.
    """

    def __init__(self, object_view: View):
        """
        Initialize the Controller with a View instance and other necessary attributes.

        Args:
        - obect_view (View): An instance of the View class.
        """
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
        """
        Start the tournament system, display menu, and handle user input for differents options.
        """
        self.view.display_menu()
        selected_menu = self.view.generic_input("Sélectionnez une option: ")
        self.view.generic_print(selected_menu)
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
            self.resume_tournament()
        elif selected_menu == "5":
            self.display_list_of_tournaments()
        elif selected_menu == "6":
            self.display_list_of_players_from_selected_tournament()
        elif selected_menu == "7":
            self.display_rank_of_players_in_tournament()
        elif selected_menu == "8":
            self.display_all_rounds_of_tournament()
        elif selected_menu == "9":
            self.display_matches_of_one_tournament()
        elif selected_menu == "10":
            self.view.generic_print("Vous avez choisi de quitter le programme.")
            sys.exit()

    # afficher les joueurs
    def display_list_of_players_in_alphabetical_order(self):
        """
        Display list of players in alphabetical order with their details.
        """
        players = self.player.get_all_players()

        if players:
            players.sort(key=lambda player: player.lastname)
            table_data = []
            for player in players:
                row = [
                    player.lastname,
                    player.firstname,
                    player.sexe,
                    player.date_of_birth,
                    player.rank,
                    player.score,
                ]
                table_data.append(row)
            headers = [
                "Nom",
                "Prénom",
                "Sexe",
                "Date de naissance",
                "Classement",
                "Score",
            ]
            table = tabulate(table_data, headers=headers, tablefmt="fancy_grid")
            self.view.generic_print(table)
        else:
            self.view.generic_print(
                "Aucun joueur n'a été trouvé dans la base de données."
            )

    # création de joueur
    def create_player(self):
        """
        Create a new player and save the player's data in the database.
        """
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
        """
        Create a new tournament and add players to it.
        Return the created tournament.
        """
        self.view.generic_print("Création d'un nouveau tournoi")
        name = self.view.generic_input("Nom du tournoi: ")
        location = self.view.generic_input("Lieu du tournoi: ")
        start_date = str(datetime.now())
        description = self.view.generic_input("Description du tournoi: ")

        new_tournament = Tournament(
            name=name, location=location, start_date=start_date, description=description
        )

        self.tournament = new_tournament
        self.tournament.save_tournament_in_db()
        players = self.player.get_all_players()
        player_dict = {}
        self.view.generic_print("Liste des joueurs présents: ")
        for index, player in enumerate(players, start=1):
            player: Player
            player_dict[str(index)] = player
            self.view.generic_print(f"{index}: {player.lastname}")

        while len(self.tournament.players) <= 7:
            joueur = self.add_player(player_dict)
            if joueur:
                self.tournament.players.append(joueur)
        serialized_tournament = self.tournament.serialize_tournament()
        self.tournament.update_tournament(serialized_tournament)
        return self.tournament

    # Ajout des joueurs pour le tournois
    def add_player(self, player_dict):
        """
        Add a player to the tournament by selecting from the list or creating a new one.

        Args:
        - player_dict (dict): Dictionnary mapping player indices to player objects.

        Returns:
        - Player: The selected or created player.
        """
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
        """
        Play the tournament, including multiple rounds.

        Args:
        - tournament (Tournament): The tournament to be played.
        """
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
        """
        Create a new round for the tournament and play it.

        Args:
        - tournament (Tournament): The tournament in which the round is created.
        - first_round (bool): Flag indicating if it's the first round.
        """
        round_number = tournament.current_round
        name_of_round = self.view.generic_input(
            "Ajouter un nom au round" + str(round_number) + ":"
        )

        date_and_hour_start = datetime.now()
        list_of_matchs = []

        if first_round:
            list_of_matchs = self.select_players_for_round(
                first_round=True, tournament_name=tournament.name
            )
        else:
            list_of_matchs = self.select_players_for_round(
                first_round=False, tournament_name=tournament.name
            )

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
        if tournament.current_round == 4:
            tournament.end_date = str(datetime.now())
        serialized_tournament = tournament.serialize_tournament()
        tournament.update_tournament(serialized_tournament)
        if tournament.current_round == 5:
            self.view.generic_print("Tounoi terminé, Au revoir")
            exit(0)
        else:
            self.ask_to_exit_tournament()

    # séléction des joueurs pour les rounds
    def select_players_for_round(self, first_round, tournament_name):
        """
        Select players for a round, either randomly or based on the scores of the previous round.

        Args:
        - first_round (bool): Flag indicating if it's the first round.
        - tournament_name (str): Name of tournament.

        Returns:
        - list: List of Match objects for the round.
        """
        players = self.tournament.get_all_players_of_a_tournament(tournament_name)
        if first_round:
            random.shuffle(players)
        else:
            players = sorted(players, key=lambda player: player.score, reverse=True)

        list_matches = []
        for i in range(0, len(players), 2):
            player_1 = Player.deserialize_player(player_dict=players[i])
            player_2 = Player.deserialize_player(players[i + 1])
            match = self.create_match(player_1, player_2)
            list_matches.append(match)

        return list_matches

    # Lancement du round
    def play_round(self):
        """
        Play a round of the tournament, including all matches.
        Return the played round.
        """
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
        """
        Create a match between two players and display match details.

        Args:
        - player1 (Player): The firts player.
        - player2 (Player): The second player.

        Returns:
        - Match: The created Match object.
        """
        player1.add_opponent(player2)
        player2.add_opponent(player1)
        match = Match(player_1=player1, player_2=player2)
        self.round.list_of_matches.append(match)
        self.view.display_match(match)
        return match

    # Attribution des scores
    def play_match(self, match: Match):
        """
        Play a match and update players scors and ranks.

        Args:
        - match (Match): The Match pnject to be played.

        Returns:
        ' Match: The played Match object.
        """
        self.view.generic_print(
            f"Match en cours: {match.player_1.lastname} vs {match.player_2.lastname}"
        )

        result = self.view.get_match_result()

        if result == "1":
            match.player_1.update_score(1)
            match.player_1_result = 1
            match.player_1.update_rank(1)
            match.player_2.update_score(0)
            match.player_2_result = 0
            match.player_2.update_player_rank(0)

        elif result == "2":
            match.player_1.update_score(0)
            match.player_1_result = 0
            match.player_1.update_player_rank(0)

            match.player_2.update_score(1)
            match.player_2_result = 1
            match.player_2.update_rank(1)
        elif result == "0.5":
            match.player_1.update_score(0.5)
            match.player_2.update_score(0.5)
            match.player_1_result = 0.5
            match.player_2_result = 0.5

        match.player_1.update_player_score(match.player_1.score)
        match.player_2.update_player_score(match.player_2.score)

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
        """
        Allow the user to select a tournament from a list and return the selected tournament.

        Args:
        - tournaments (list): List of Tournament objects.

        Returns:
        - Tournament or None: The selected tournament or None if no tournament is found..
        """
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
        """
        Resume a tournament by allowing the user to choose from available tournaments whit their names and numbers.

        Returns:
        - None
        """
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
        """
        Display a list of available tournaments with their names and numbers.

        Returns:
        - None
        """
        tournaments = self.tournament.get_all_tournaments()

        if not tournaments:
            self.view.generic_print("Aucun tournoi trouvé.")
            return

        self.view.generic_print("Liste des tournois disponibles:")
        table_data = []
        for i, tournament in enumerate(tournaments, start=1):
            table_data.append(
                [i, tournament.name, tournament.start_date, tournament.end_date]
            )

        table_headers = ["Numéro", "Nom du tournoi", "Date de début", "Date de fin"]
        table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid")
        self.view.generic_print("Liste des tournois disponibles: ")
        self.view.generic_print(table)

    # afficher la liste des joueurs, par ordre alphabétique, d'un tournoi choisi
    def display_list_of_players_from_selected_tournament(self):
        """
        Display a list of players from a selected tournament with their IDs, names, and scores.

        Returns:
        - None
        """
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Liste des joueurs du tournoi {selected_tournament.name}"
            )
            players = selected_tournament.players

            table_data = []
            for player in players:
                row_data = [
                    player.player_id,
                    f"{player.lastname} {player.firstname}",
                    player.score,
                ]
                table_data.append(row_data)

            table_headers = ["ID", "Nom du joueur", "Score"]
            table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid")
            self.view.generic_print(table)
        else:
            self.view.generic_print(
                "Aucun joueur trouvé pour le tournoi {selected_tournament.name}"
            )

    # afficher le rang des joueurs d'un tournoi choisi
    def display_rank_of_players_in_tournament(self):
        """
        Display the rank of players in a selected tournament.

        Returns:
        - None
        """
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Classement des joueurs du tournoi {selected_tournament.name} :"
            )
            players = selected_tournament.players
            table_data = []
            for player in players:
                row_data = [player.firstname, player.rank]
                table_data.append(row_data)
            table_headers = ["Prénom du joueur", "Rang"]
            table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid")
            self.view.generic_print(table)
        else:
            self.view.generic_print(
                f"Aucun rang de joueurs dans le tournoi {selected_tournament.name}"
            )

    # afficher les rounds d'un tournoi choisi
    def display_all_rounds_of_tournament(self):
        """
        Display a list of rounds in a selected tournament.

        Returns:
        - None
        """
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Liste des tours du tournoi {selected_tournament.name}"
            )

            rounds = selected_tournament.rounds
            table_data = []
            for i, round in enumerate(rounds, start=1):
                row_data = [i, round.name_of_round]
                table_data.append(row_data)

            table_headers = ["Numéro du round", "Nom du round"]
            table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid")
            self.view.generic_print(table)

        else:
            self.view.generic_print(
                f"Aucun tour trouvé pour le tournoi {selected_tournament.name}"
            )

    # afficher la liste des matchs d'un tournoi choisi
    def display_matches_of_one_tournament(self):
        """
        Display a list of matches in a selected tournament, including player information and results.

        Returns:
        - None
        """
        tournaments = self.tournament.get_all_tournaments()
        selected_tournament: Tournament = self.selected_tournament_index(tournaments)

        if selected_tournament:
            self.view.generic_print(
                f"Liste des matchs du tournoi {selected_tournament.name}"
            )
            rounds = selected_tournament.rounds
            for round in rounds:
                round: Round = round
                self.view.generic_print(
                    f"Liste des matchs du round {round.name_of_round} : "
                )
                matches = round.list_of_matches
                table_data = []
                for match in matches:
                    player_1 = match.player_1
                    player_2 = match.player_2
                    player_1_result = match.player_1_result
                    player_2_result = match.player_2_result
                    row_data = [
                        f"{player_1.lastname} {player_1.firstname}",
                        f"ID: {player_1.player_id}, Score: {player_1.score}, Rang: {player_1.rank}",
                        f"{player_2.lastname}, {player_2.firstname}",
                        f"ID: {player_2.player_id}, Score: {player_2.score}, Rang: {player_2.rank}",
                        f"Résultat : {player_1_result} - {player_2_result}",
                    ]
                    table_data.append(row_data)
                table_headers = [
                    "Joueur 1",
                    "Info Joueur 1",
                    "Joueur 2",
                    "Info Joueur 2",
                    "Résultat",
                ]
                table = tabulate(
                    table_data, headers=table_headers, tablefmt="fancy_grid"
                )
                self.view.generic_print(table)
        else:
            self.view.generic_print("Aucun match trouvé pour le tournoi sélectionné")

    # Intéraction avec l'utilisateur pour continuer ou quitter le tournoi en cours
    def ask_to_exit_tournament(self):
        """
        Ask the user if they want to continue or exit the current tournament.
        """
        user_input = self.view.generic_input(
            "Continuer le tournoi? (Entrez O pour oui et N pour non.)"
        )
        if user_input == "n":
            self.view.generic_print("Vous avez quitté le tournoi.")
            exit(0)
