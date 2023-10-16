class View:
    def display_menu(self):
        menu = {
            1:"Ajouter des joueurs",
            2:"Afficher la liste des joueurs",
            3:"Créer un tournoi",
            4:"Lancer un tournoi",
            5:"Afficher la liste des tournois",
            6:"Afficher la liste des joueurs d'un tournoi",
            7:"Afficher le classement des joueurs d'un tounoi",
            8:"Afficher les tours d'un tournoi",
            9:"Afficher tous les matchs d'un tounoi",
            10:"Quitter"
            
        }
        print(menu)
        
    def menu_user_response(self, prompt):
        self.user_response = input(prompt)
        return self.user_response
    
    #input player
    # def input_player():
    #     print("Veillez entrer vos informations : ")
    #     lastname = input("Nom de famille : ")
    #     firstname = input("Prénom : ")
    #     sexe= input("Sexe : ")
    #     date_of_birth = input("Date de naissance : ")
    #     rank = input("Classement : ")
    #     player_id = input("Votre identifiant de joeur : ")
        
    #     player_data = {
    #         "lastname": lastname,
    #         "firstname": firstname,
    #         "sexe": sexe,
    #         "date of birth": date_of_birth,
    #         "rank": rank,
    #         "player_id": player_id
    #     }
    #     return player_data
    
    def get_player_lastname(self):
        print("get_player_lastname")
        lastname = input("Nom de famille : ")
        return lastname
    
    def get_player_firstname(self):
        firstname = input("Prénom : ")
        return firstname
    
    def get_player_sexe(self):
        sexe = input("Sexe: ")
        return sexe
    
    def get_player_date_of_birth(self):
        date_of_birth = input("Date de naissance: ")
        return date_of_birth
    
    def get_player_rank(self):
        rank = input("Niveau: ")
        return rank
    
    def get_player_id(self):
        player_id = input("Identifiant: ")
        return player_id
        
   #afficher les joueurs
    def display_player(self):
        pass
   
    #afficher le tournoi
    def diplay_tournaments(self):
        pass
     #afficher la liste des tours avec les joueurs
    def display_round(self):
        pass
    #afficher la liste des matchs avec les joueurs
    def display_match(self):
        pass
    #afficher la liste des match dans un tournois
    def display_match_in_tournament(self):
        pass
    
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
   