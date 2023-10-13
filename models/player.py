
class Player:
    def __init__(self, lastname="", firstname="", sexe="", date_of_birth="", rank="", score=0, player_id=""):
        self.lastname = lastname
        self.firstname = firstname
        self.sexe = sexe
        self.date_of_birth = date_of_birth
        self.rank = rank
        self.score = score
        self.player_id = player_id
        
    def update_score(self, score):
        self.score += score
        
    def update_rank(self, new_rank):
        self.rank = new_rank
        
    def serialize_player(self):
        serialize_player= {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "sexe": self.sexe,
            "date of birth": self.date_of_birth,
            "rank": self.rank,
            "score": self.score,
            "player_id": self.player_id
        }
        return serialize_player
    
    
    #get player
    def get_player_by_id(self, player_id):
        player_data = db.get_player_by_id(player_id)
        
        if player_data:
            return {
                "lastname":player_data["lastname"],
                "firstname":player_data["firstname"],
                "sexe":player_data["sexe"],
                "date_of_birth":player_data["date of birth"],
                "rank":player_data["rank"],
                "score":player_data["score"],
                "player_id":player_data["player_id"]
            }
        else:
            return None
        
    #sauvgarder joueur
    
    def save_player_in_db(self,p,db):
        serialize_player = self.serialize_player(p)
        db.insert(serialize_player)
    
    
    
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
    
    
 
    
    