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
        # self.match: Match = Match()
        self.view = object_view
        self.db = TinyDB('db.json')
        TinyDB.default_table_name = "Players"
        self.players_table = self.db.table("Players")
        self.tournament_table = self.db.table("Tournaments")
       
        
        
        
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
        if selected_menu == "2":
            display_list_players = self.view.display_list_of_players()
            print(display_list_players)
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
        print("Création des joueurs: ")
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
         
    
       #création d'un tournois   
    def create_tournament(self):
        print("Création d'un nouveau tournoi")
        name = self.view.get_tournament_name()
        location = self.view.get_tournament_location()
        date = self.view.get_tournament_date()
        # nb_round = self.tournament.nb_rounds
        descritpion = self.view.get_tournament_description()
        
        new_tournament = Tournament(name, location, date, descritpion)
        
        self.tournament = new_tournament
        self.tournament.save_tournament_in_db()
        return new_tournament
    
    def play_tournament():
        pass