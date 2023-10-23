from models.player import Player
from tinydb import TinyDB
from models.tournament import Tournament
from models.round import Round
from models.match import Match

class View:
    def __init__(self):
        self.player: Player = Player()
        self.db = TinyDB("db.json")
        self.round: Round = Round()
        
    def display_menu(self):
        menu = '''
1: Ajouter des joueurs
2: Afficher la liste des joueurs
3: Créer un tournoi
4: Lancer un tournoi
5: Afficher la liste des tournois
6: Afficher la liste des joueurs d'un tournoi
7: Afficher le classement des joueurs d'un tounoi
8: Afficher les tours d'un tournoi
9: Afficher tous les matchs d'un tounoi
10: Quitter    
        '''
        print(menu)
        
    def player_create(self):
        print("Le joueur a été créé.")
    
    def player_save(self):
        print("Le joueur a été enregistré dans la base de données.")
   #afficher les joueurs
    def display_list_of_players(self):
        player: Player = Player()
        players = self.player.get_all_players()
        if players:
            print("Liste des joueurs :")
            for player in players:
                print(f"Nom : {player.lastname}, Prénom : {player.firstname}, Sexe : {player.sexe}, Date de naissance : {player.date_of_birth}, Classement : {player.rank}")
        else:
            print("Aucun joueur n'a été trouvé dans la base de données.")
       
    def print_create_player(self):
        create_player = print("Création des joueurs: ")   
        return create_player
 
    def input_index_player_invalible(self):
        print("Index du joueur invalide.")
        
    def not_enough_players(self):
        print("Il n'y a pas assez de joueurs.")
        
    def end_of_tournament(self):
        print("Le tournoi est terminé.")
        
    #afficher le tournoi
    def diplay_tournaments(self):
        pass
    
    #afficher la liste des tours avec les joueurs
    def display_round(self):
        print("Détail du round: ")
        print(f"Nom du round: {self.round.name_of_round}")
        print(f"Date et heure de début: {self.round.date_and_hour_start}")
        
        
    #afficher la liste des matchs avec les joueurs
    def display_match(self, match: Match):
        print("Le joueur 1 est: ", match.player_1.firstname, match.player_1.lastname)
        print(f"Score Joueur 1: {match.player_1_result}")
        print("Le joueur 2 est : ", match.player_2.firstname, match.player_2.lastname)
        print(f"Score Joueur 2: {match.player_2_result}")
    #afficher la liste des match dans un tournois
    
    
    # afficher la liste des joueurs d'un tournoi
    def display_list_of_player_from_tournament(self):
        pass
    #afficher les scores pour chaque tours
     
    #afficher le score pour chaque matchs
    
    #afficher le gagnant pour chaque tour
    
    #afficher le gagnant pour chaque match
    
    #afficher le gagnant pour chaque tournoi
    
    
   #afficher le classement des joueurs d'un tournoi 
    def display_ranking_players_of_tournament():
       pass
   #afficher les tours d'un trounoi
    def display_rounds_tournament():
       pass
   #afficher la liste des match d'un tounoi
    def display_list_matchs_of_tournament():
        pass

    def rest_of_tournament(self):
        user_response = input('Souhaitez-vous lancer le tournoi ou le quitter? Entrer "lancer" ou "quitter"')
        if user_response == "lancer":
            print("Vous avez choisi de lancer le tournoi")
        elif user_response == "quitter":
            print("Vous avez choisi de quitter le tournoi.")
        else:
            print("Réponse invalide. Veuillez entrer 'lancer' ou 'quitter'.")
            
    def display_first_round_matches(self, match_first_round):
        for match in match_first_round:
            print(f"Match: {match[0]} vs {match[1]}")
        
    def generic_print(self,sentance_print):
        print(sentance_print) 
    def generic_input(self,sentance_input):
        input_to_return = input(sentance_input)
        return input_to_return
    
    def get_match_result(self):
        pass
    
    def display_player_score(self):
        pass
