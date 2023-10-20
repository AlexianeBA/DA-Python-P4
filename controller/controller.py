#fonction pour faire tourner le script qui permet de :
    #afficher le menu
    #ajouter des joueurs à la base de données (appler methode vue (input))
    #créer un tournoi
    #lancer un tournoi
    #afficher la liste des joueurs
    #afficher la liste des joueurs du tournoi
    #afficher les tours du tournoi
    #afficher les matchs du tounoi
    #afficher le resultat du tournoi
    #afficher le classement des joueurs
from tinydb import TinyDB
from view.vue import View
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
import random

class Controller:
    def __init__(self, object_view:View):
        self.view = object_view
        self.player:Player = Player()
        self.tournament = object_view
        # self.match: Match = Match()
        self.view = object_view
        self.db = TinyDB('db.json')
        TinyDB.default_table_name = "Players"
        self.players_table = self.db.table("Players")
        self.tournament_table = self.db.table("Tournaments")
        self.rounds = []
       
        
        
        
    def start(self):
        self.view.display_menu()
        selected_menu = self.view.menu_user_response()
        print(selected_menu)
        print(type(selected_menu))
        if selected_menu == "1":
            add_player = self.create_player()
            print(add_player)
        if selected_menu == "2":
            self.view.display_list_of_players()
        if selected_menu == "3":
            create_tournament = self.create_tournament()
            print(create_tournament)
        if selected_menu == 4:
            play_tournament = self.play_tournament()
            print(play_tournament)
        if selected_menu == 5:
            display_list_tournaments = self.view. diplay_tournaments()
            print(display_list_tournaments)
        if selected_menu == 6:
            display_list_of_players_from_tournament = self.view.display_list_of_player_from_tournament()
            print(display_list_of_players_from_tournament)
        if selected_menu == 7:
            display_ranking_players_of_tournament = self.view.display_ranking_players_of_tournament()
            print(display_ranking_players_of_tournament)
        if selected_menu == 8:
            display_rounds_of_tournament = self.view.display_rounds_tournament()
            print(display_rounds_of_tournament)
        if selected_menu == 9:
            display_list_matchs_of_tournament = self.view.display_list_matchs_of_tournament()
            print(display_list_matchs_of_tournament)
        if selected_menu == 10:
            pass
    



    
    #création de joueur   
    def create_player(self):
        print(self.view.print_create_player)
        joueur: Player= Player()
        joueur.lastname = self.view.get_player_lastname()
        joueur.firstname= self.view.get_player_firstname()
        joueur.sexe= self.view.get_player_sexe()
        joueur.date_of_birth= self.view.get_player_date_of_birth()
        joueur.rank = self.view.get_player_rank()
        joueur.id = self.view.get_player_id()
        self.view.player_create()
        #Sauvegarde des données du joueur
        serialized_player = joueur.serialize_player()
        self.player.save_player_in_db(serialized_player)
        self.view.player_save()
        
    
       #création d'un tournois   
    def create_tournament(self):
        print(self.view.print_create_tournament)
        name = self.view.get_tournament_name()
        location = self.view.get_tournament_location()
        date = self.view.get_tournament_date()
        # nb_round = self.tournament.nb_rounds
        descritpion = self.view.get_tournament_description()
        
        new_tournament = Tournament(name, location, date, descritpion)
        
        self.tournament = new_tournament
        self.tournament.save_tournament_in_db()
        # TODO : créer méthode qui va appeler get_all_players. Dans cette méthode, contruire un dictionnaire
        players = self.player.get_all_players()
        player_dict = {}
        print(self.view.display_list_players_to_chose())
        for index, player in enumerate(players, start=1):
            player:Player
            player_dict[str(index)] = player
            print(f"{index}: {player.lastname}")
        
        while len(self.tournament.players)<=7:
            joueur = self.add_player(player_dict)
            self.tournament.players.append(joueur)
        self.tournament.save_tournament_in_db()
        self.create_round()
    
    def add_player(self, player_dict):
        user_input = self.view.input_index_player()
        if user_input == 'C':
            return self.create_player()
        else:
            return player_dict[user_input]
            
            
            
    def play_tournament():
        pass
    
    
        # 1er round
    def create_round(self):
        if self.rounds.current_round <= self.rounds.nb_round:
            players = self.player.get_all_players()
            if len(players)<8:
                self.view.not_enough_players()
                return
                player_group_1 = players[:4]
                player_group_2 = players[4:8]
            
                round_name = f"Round {self.current_round} - {self.name}"
                new_round = Round(name_of_round=round_name)
                new_round.create_list_of_matches(player_group_1, player_group_2)
                self.rounds.append(new_round)
                self.current_round += 1
                print(f"Round {self.current_round} - {self.name} créé.")
            
            else:
                self.view.end_of_tournament