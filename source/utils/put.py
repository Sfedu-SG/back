from config import db
from flask import make_response

def update_attr(table, object_from_database, field_to_update, new_value):
    if not hasattr(table, field_to_update):
        return make_response({"message": "Invalid field to update"}, 400)

    setattr(object_from_database, field_to_update, new_value)
    db.session.commit()
    return make_response({"message": f"{field_to_update} updated successfully"}, 200)