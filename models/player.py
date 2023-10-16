
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
        
    def update_score(self, score):
        self.score += score
        
    def update_rank(self, new_rank):
        self.rank = new_rank
    
    def add_opponent(self, opponent):
        self.opponent.append(opponent)
           
    def serialize_player(self, player):
        serialize_player = {
            "lastname": player.lastname,
            "firstname": player.firstname,
            "sexe": player.sexe,
            "date of birth": player.date_of_birth,
            "rank": player.rank,
            "score": player.score,
            "player_id": player.player_id
        }
        return serialize_player
      
   
        
    #sauvgarder joueur
    
    def save_player_in_db(self,player, db):
        serialize_player = self.serialize_player(player)
        db.insert(serialize_player)
        print(serialize_player)
    
    
    
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
    
    
 
    
    