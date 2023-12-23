from config import db, app

class FilesTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "path": self.path
        }

with app.app_context():
    db.create_all()