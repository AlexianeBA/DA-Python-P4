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

class Controller:
    def __init__(self, object_view:View):
        self.view = object_view
        self.player:Player = Player
        self.tournament = object_view
        self.view = object_view
        self.db = TinyDB('db.json')

        
    def start(self):
        print("start")
        self.view.display_menu()
        selected_menu = self.view.menu_user_response()
        print(selected_menu)
        if selected_menu == 1:
            add_player = self.create_player()
        print(add_player)
        if selected_menu == 2:
            display_list_players = self.view.display_player()
            print(display_list_players)
        if selected_menu == 3:
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
    

    #création d'un tournois   
    def create_tournament(self):
        self.tournament.create_tournament() 
    
    
    #création de joueur   
    def create_player(self):
        player= Player()
        player.lastname = self.view.get_player_lastname()
        player.firstname= self.view.get_player_firstname()
        # data = self.view.input_player()
        # player=Player(lastname=data["lastname"],
        #     firstname=data["firstname"],
        #     sexe=data["sexe"],
        #     date_of_birth=data["date of birth"],
        #     rank=data["rank"],
        #     score=data["score"],
        #     player_id=data["player_id"])
        # print(player)
        
        # self.player.save_player_in_db(player,self.db) 
    
    def play_tournament(self):
        self.tournament.play_tournament()
        
    
   