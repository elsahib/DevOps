from application import db
from application.models import Users, Players, Stats
db.drop_all()
db.create_all()
