from tinydb import TinyDB, Query
class Player:
    def __init__(self, lastname="", firstname="", sexe="", date_of_birth="", rank="", score=0, player_id=""):
        self.lastname = lastname
        self.firstname = firstname
        self.sexe = sexe
        self.date_of_birth = date_of_birth
        self.rank = rank
        self.score = score
        self.player_id = player_id
        self.opponent = []
        self.db = TinyDB('db.json')
        self.table = self.db.table("Players")
        
        
    def update_score(self, score):
        self.score += score
        
    def update_rank(self, new_rank):
        self.rank = new_rank
    
    def add_opponent(self, opponent):
        self.opponent.append(opponent)
           
    def serialize_player(self):
        serialize_player = {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "sexe": self.sexe,
            "date_of_birth": self.date_of_birth,
            "rank": self.rank,
            "score": self.score,
            "player_id": self.player_id
        }
        return serialize_player
    
    #récupérer la liste des joueurs  
    def get_all_players(self):
        players = self.db.table("Players").all()
        list_of_players = []
        for player in players:
            deserialized_player = self.deserialize_player(player)
            list_of_players.append(deserialized_player)
        return list_of_players
    
    def deserialize_player(self, player_dict):
        player_object = Player(
            lastname=player_dict["lastname"],
            firstname=player_dict["firstname"],
            sexe=player_dict["sexe"],
            date_of_birth=player_dict["date_of_birth"],
            rank=player_dict["rank"],
            score=player_dict["score"],
            player_id=player_dict["player_id"]
            )
        return player_object
        
    
    
    #sauvgarder joueur
    def save_player_in_db(self,player):
        self.table.insert(player)
    
    
    
    #GENERATION DES PAIRES
    
    #trier les joueurs de manière croissante selon le score obtenu pendant le tournoi
    def sort_players_based_score_result_in_tournament():
        pass
    
    #associez les joueurs dans l'ordre, exemple: joueur 1 avec joueur 2 selon leur score. faire en sorte que les joueurs ne se rencontrent pas plus d'une fois et si le score des joueurs est identique, choisir aléatoirement
    def players_in_order():
        pass
    
    #tirage au sort de qui joue blanc et qui joue noir
    def draw_player_color():
        pass
    
    

    
    