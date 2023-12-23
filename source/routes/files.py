from source.models.users import UsersTable
from source.models.profiles import ProfilesTable
from source.models.files import FilesTable
from source.utils.put import update_attr
from config import api, db

from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import jwt_required



class Files(Resource):
    @jwt_required()
    def get(self, user_id):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        max_per_page = 100

        if page < 1:
            return {"message": "Page number must be greater than or equal to 1"}, 400

        if per_page < 1 or per_page > max_per_page:
            return {"message": f"Invalid value for per_page. It should be between 1 and {max_per_page}"}, 400

        offset = (page - 1) * per_page
        files = FilesTable.query.filter_by(user_id=user_id).offset(offset).limit(per_page).all()

        total_files = FilesTable.query.filter_by(user_id=user_id).count()

        return {
            "files": [file.serialize() for file in files],
            "page": page,
            "per_page": per_page,
            "total_files": total_files
        }

    @jwt_required()
    def post(self, user_id):
        if "name" not in request.json or "path" not in request.json:
            return make_response({"message": "Missing required fields"}, 400)

        data = request.get_json()
        new_file = FilesTable(
            user_id=user_id,
            name=data.get("name"),
            path=data.get("path"),
        )

        db.session.add(new_file)
        db.session.commit()

        return make_response({"message": "File created"}, 201)

api.add_resource(Files, "/profiles/<int:id>/files")

class FileOne(Resource):
    @jwt_required()
    def get(self, user_id, file_id):
        file = FilesTable.query.filter_by(id=file_id, user_id=user_id).first()
        if file is None:
            return make_response({"message": "File not found"}, 404)
        return file.serialize()

    @jwt_required()
    def put(self, user_id, file_id):
        if "name" not in request.json or "path" not in request.json:
            return make_response({"message": "Missing required fields"}, 400)

        data = request.get_json()
        file = FilesTable.query.filter_by(id=file_id, user_id=user_id).first()

        field_to_update = data.get("field_to_update")
        new_value = data.get("new_value")

        if not hasattr(ProfilesTable, field_to_update):
            return make_response({"message": "Invalid field to update"}, 400)

        return update_attr(FilesTable, file, field_to_update, new_value)

    @jwt_required()    
    def delete(self, user_id, file_id):
        file = FilesTable.query.filter_by(id=file_id, user_id=user_id).first()
        if file is None:
            return make_response({"message": "File not found"}, 404)
        db.session.delete(file)
        db.session.commit()
        return make_response({"message": "File deleted successfully"}, 200)
    

api.add_resource(FileOne, "/profiles/<int:user_id>/files/<int:file_id>")