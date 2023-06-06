from flask import abort, make_response
from app import db
from app.models import Role
from app.schemas import roles_schema, role_schema


def search():
    roles = Role.query.all()
    return roles_schema.dump(roles), 200


def post(role_obj: dict):
    role_name = role_obj.get("name")
    existing_role = Role.query.filter(Role.name == role_name).one_or_none()

    if existing_role is None:
        new_role = role_schema.load(role_obj, session=db.session)
        if not new_role.name:
            abort(400, "Missing required field 'name'")
        created_role = Role(name=new_role.name, description=new_role.description)
        db.session.add(created_role)
        db.session.commit()
        return role_schema.dump(created_role), 201
    else:
        abort(409, f"Role with name '{role_name}' already exists")


def get(role_id: int):
    role = Role.query.filter(Role.id == role_id).one_or_none()

    if role is not None:
        return role_schema.dump(role), 200
    else:
        abort(404, f"Role with ID '{role_id}' not found")


def put(role_id: int, role_obj: dict):
    existing_role = Role.query.filter(Role.id == role_id).one_or_none()

    if existing_role is not None:
        role_update = role_schema.load(role_obj, session=db.session)
        if role_update.name:
            existing_name = Role.query.filter(Role.name == role_update.name).one_or_none()
            if existing_name is None:
                existing_role.name = role_update.name
            else:
                abort(409, f"Role with name '{role_update.name}' already exists")
        if role_update.description:
            existing_role.description = role_update.description
        db.session.merge(existing_role)
        db.session.commit()
        return role_schema.dump(existing_role), 200
    else:
        abort(404, f"Role with ID '{role_id}' not found")


def delete(role_id: int):
    existing_role = Role.query.filter(Role.id == role_id).one_or_none()

    if existing_role is not None:
        db.session.delete(existing_role)
        db.session.commit()
        return make_response(f"Role with ID '{role_id}' successfully deleted", 204)
    else:
        abort(404, f"Role with ID '{role_id}' not found")
