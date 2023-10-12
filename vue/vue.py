
class Menu:
    def display_menu(self):
        menu = {
            1:"Ajouter des joueurs",
            2:"Afficher la liste des joueurs",
            3:"Créer un tournoi",
            4:"Lancer un tournoi",
            5:"Afficher la liste des tournois",
            6:"Ajouter un nom de tournoi",
            7:"Ajouteur les dates de tournoi",
            8:"Afficher la liste des joueurs d'un tournoi par ordre alphabétique",
            9:"Sauvgarder le tournoi",
            10:"Afficher le classement des joueurs d'un tounoi",
            11:"Afficher les tours d'un tournoi",
            12:"Afficher tous les marchs d'un tounoi",
            13:"Quitter"
            
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