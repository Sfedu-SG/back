from source.models.users import UsersTable
from config import bcrypt, api

from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token


class Auth(Resource):
    def post(self):
        data = request.get_json()

        if "login" not in data or "password" not in data:
            return make_response({"message": "Missing required fields"}, 400)

        login = data["login"]
        password = data["password"]

        user = UsersTable.query.filter_by(login=login).first()
        if not user:
            return make_response({"message": "Something went wrong. Try again later"}, 404)

        if not bcrypt.check_password_hash(user.password, password):
            return make_response({"message": "Something went wrong. Try again later"}, 401)

        access_token = create_access_token(identity=login)
        refresh_token = create_refresh_token(identity=login)

        return make_response({"access_token": access_token, "refresh_token": refresh_token}, 200)

api.add_resource(Auth, "/auth")