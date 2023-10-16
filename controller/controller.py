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
        self.player:Player = Player()
        self.tournament = object_view
        self.match: Match = Match()
        self.view = object_view
        self.db = TinyDB('db.json')

        
    def start(self):
        print("start")
        self.view.display_menu()
        selected_menu = self.view.menu_user_response("Séléctionnez une option")
        print(selected_menu)
        print(type(selected_menu))
        if selected_menu == "1":
            print("choix 1")
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
    



    
    #création de joueur   
    def create_player(self):
        print("create_player")
        joueur: Player= Player()
       
        joueur.lastname = self.view.get_player_lastname()
        joueur.firstname= self.view.get_player_firstname()
        joueur.sexe= self.view.get_player_sexe()
        joueur.date_of_birth= self.view.get_player_date_of_birth()
        joueur.rank = self.view.get_player_rank()
        joueur.id = self.view.get_player_id()
        
        print(joueur)
        #Sauvegarde des données du joeur
        self.player.save_player_in_db(joueur, self.db) 
    
    # def play_tournament(self):
    #     self.tournament.play_tournament()
        
 
    
       #création d'un tournois   
    def create_tournament(self):
        pass
    
    def play_tournament():
        pass