from source.models.users import UsersTable
from config import bcrypt, api, jwt

from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

# crud realization
class Profiles(Resource):
    @jwt_required()
    def get(self):
        # Получаем параметры запроса (query parameters)
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Определите максимальное количество записей на странице (по вашему выбору)
        max_per_page = 100

        # Проверка входных данных
        if page < 1:
            return {"message": "Page number must be greater than or equal to 1"}, 400

        if per_page < 1 or per_page > max_per_page:
            return {"message": f"Invalid value for per_page. It should be between 1 and {max_per_page}"}, 400

        # Рассчитываем смещение и получаем записи с учетом пагинации
        offset = (page - 1) * per_page
        users = UsersTable.query.offset(offset).limit(per_page).all()

        # Можно также вернуть общее количество записей для создания навигации на клиенте
        total_users = UsersTable.query.count()

        return {
            "users": [user.serialize() for user in users],
            "page": page,
            "per_page": per_page,
            "total_users": total_users
        }

api.add_resource(Profiles, "/profiles")