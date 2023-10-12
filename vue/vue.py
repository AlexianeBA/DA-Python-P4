
class View:
    def display_menu(self):
        menu = {
            1:"Ajouter des joueurs",
            2:"Afficher la liste des joueurs",
            3:"Créer un tournoi",
            4:"Lancer un tournoi",
            6:"Afficher la liste des tournois",
            7:"Afficher la liste des joueurs d'un tournoi",
            9:"Afficher le classement des joueurs d'un tounoi",
            10:"Afficher les tours d'un tournoi",
            11:"Afficher tous les matchs d'un tounoi",
            12:"Quitter"
            
        }
        
    def menu_user_response(self):
        self.user_response = input()
        return self.user_response
    
    def display_player(self):
        pass
    
    def diplay_tournament(self):
        pass
    
    def display_round(self):
        pass
    
    def display_match(self):
        pass
    
    def display_match_in_tournament(self):
        pass