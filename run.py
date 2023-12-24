'''
Для всех заглянувших: ответственность за всё безобразие описанное в этой части проекта несет
в основном один человек, его контакты:
Telegram: @legannyst
VK: @marklav
GitHub: github.com/Leganyst
'''

from config import app, jwt, db, bcrypt, api
import source

if __name__ == "__main__":
    api.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.run(debug=True)
    