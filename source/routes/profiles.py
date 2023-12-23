from source.models.users import UsersTable
from source.models.profiles import ProfilesTable
from config import api, db

from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import jwt_required

import datetime

# crud realization
class Profiles(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)


        max_per_page = 100

        if page < 1:
            return {"message": "Page number must be greater than or equal to 1"}, 400

        if per_page < 1 or per_page > max_per_page:
            return {"message": f"Invalid value for per_page. It should be between 1 and {max_per_page}"}, 400

        offset = (page - 1) * per_page
        users = UsersTable.query.offset(offset).limit(per_page).all()

        total_users = UsersTable.query.count()

        return {
            "users": [user.serialize() for user in users],
            "page": page,
            "per_page": per_page,
            "total_users": total_users
        }

    @jwt_required()
    def post(self):

        if "name" not in request.json or "lastname" not in request.json or "birthday" not in request.json:
            return make_response({"message": "Missing required fields"}, 400)
        
        data = request.get_json()
        try:
            parsed_birthday = datetime.datetime.strptime(data.get("birthday"), "%d.%m.%Y").date()
        except ValueError:
            return make_response({"message": "Invalid date format for birthday"}, 400)


        new_profile = ProfilesTable(
            name=data.get("name"),
            lastname=data.get("lastname"),
            surname=data.get("surname", None),
            birthday=parsed_birthday,
            last_edit=datetime.datetime.now()
        )

        db.session.add(new_profile)
        db.session.commit()

        return make_response({"message": "Profile created"}, 201)

    @jwt_required()
    def put(self, id):
        data = request.get_json()

        field_to_update = data.get('field_to_update')
        new_value = data.get('new_value')

        profile = ProfilesTable.query.get(id)

        if profile is None:
            return {"message": f"Profile with id {id} not found"}, 404

        if not hasattr(ProfilesTable, field_to_update):
            return make_response({"message": "Invalid field to update"}, 400)

        setattr(profile, field_to_update, new_value)
        db.session.commit()

        return make_response({"message": f"{field_to_update} updated successfully"}, 200)

    @jwt_required()
    def delete(self, id):
        profile = ProfilesTable.query.get(id)

        if profile is None:
            return {"message": f"Profile with id {id} not found"}, 404

        db.session.delete(profile)
        db.session.commit()

        return make_response({"message": "Profile deleted successfully"}, 200)

api.add_resource(Profiles, "/profiles/<int:id>")