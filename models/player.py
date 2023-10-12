class Player:
    def __init__(self, lastname="", firstname="", sexe="", date_of_birth="", rank="", score=0):
        self.lastname = lastname
        self.firstname = firstname
        self.sexe = sexe
        self.date_of_birth = date_of_birth
        self.rank = rank
        self.score = score
        
    def update_score(self, score):
        self.score += score
        
    def update_rank(self, new_rank):
        self.rank = new_rank
        
    def add_player(self):
        add_player= {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "sexe": self.sexe,
            "date of birth": self.date_of_birth,
            "rank": self.rank,
            "score": self.score
        }
        return add_player