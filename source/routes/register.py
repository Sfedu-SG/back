from source.models.users import UsersTable
from config import db, bcrypt, api

from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

class Register(Resource):
    def post(self):
        # Получение данных из JSON-запроса
        data = request.get_json()

        # Проверка наличия обязательных полей в JSON-данных
        if "login" not in data or "password" not in data:
            return make_response({"message": "Missing required fields"}, 400)

        login = data["login"]
        password = data["password"]

        # Проверка, что пользователь с таким логином не существует
        if UsersTable.query.filter_by(login=login).first():
            return make_response({"message": "Something went wrong. Try again later"}, 400)

        # Хэширование пароля
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Создание нового пользователя
        new_user = UsersTable(login=login, password=hashed_password)

        # Сохранение пользователя в базе данных
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=login)
        refresh_token = create_refresh_token(identity=login)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200


api.add_resource(Register, "/register")