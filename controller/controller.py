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
from datetime import datetime
import random

class Controller:
    def __init__(self, object_view:View):
        self.view = object_view
        self.player:Player = Player()
        self.tournament: Tournament = Tournament()
        # self.match: Match = Match()
        self.view = object_view
        self.db = TinyDB('db.json')
        TinyDB.default_table_name = "Players"
        self.players_table = self.db.table("Players")
        self.tournament_table = self.db.table("Tournaments")
        self.rounds = []
        self.round: Round = Round()
       
        
        
        
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
        if selected_menu == "4":
            # play_tournament = self.play_tournament()
            # print(play_tournament)
            self.create_round()
            self.select_random_players_first_round()
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
        #ajouter un input ou on demande à l'user si il veut quitter ou si il veut lancer le tournoi. si il veut le lancer alors la fonction create round se lance sinon on quitte l(e script
        self.view.rest_of_tournament()
        
    
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
       first_round = Round(name_of_round="Round 1", date_and_hour_start=datetime.now())
       self.tournament.add_round(round=first_round)
       self.view.display_round()
      
           
    def select_random_players_first_round(self):
        players = self.player.get_all_players()
        random.shuffle(players)
        
        current_round = self.tournament.get_current_round()
        if current_round:
            for i in range(0, len(players), 2):
                match = Match(player_1 = players[i], player_2 = players[i+1])
                self.tournament.add_match(match)
                self.view.display_match(match)
        else:
            self.view.no_round_in_progress()
        
        