from application import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Players(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(30), nullable=False)
    player_age = db.Column(db.Integer, nullable=False)
    player_team = db.Column(db.String(100), nullable=False)
  

    def __repr__(self):
        return ''.join([
            'Player: ', self.player_name, ' ', self.player_age, '\r\n',
            'Team: ', self.player_team, '\r\n', self.player_id
            ])

class Stats(db.Model, UserMixin):
    stat_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(500), nullable=False, unique=True)
    goals = db.Column(db.String(500), nullable=False)
    assists = db.Column
    chances = db.Column
    shots = db.Column
    minutes = db.Column
    date = db.Column

    
    def __repr__(self):
        return ''.join(['UserID: ', str(self.id), '\r\n', 'Email: ', self.email])