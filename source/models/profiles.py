from config import db, app

class ProfilesTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80))
    birthday = db.Column(db.Date, nullable=False)
    last_edit = db.Column(db.Date)


with app.app_context():
    db.create_all()