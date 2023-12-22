from config import app, jwt, db, bcrypt, api
import source

if __name__ == "__main__":
    api.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # db.init_app(app)
    app.run(debug=True)
    