from config import db, app
from config import db, app

class UsersTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(300))

    def serialize(self):
        return {
        "id": self.id,
        "login": self.id
        }
with app.app_context():
    db.create_all()