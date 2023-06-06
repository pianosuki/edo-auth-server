from flask import abort, make_response
from app import db, bcrypt
from app.models import User, Role
from app.schemas import users_schema, user_schema


def search():
    users = User.query.all()
    return users_schema.dump(users), 200


def post(user_obj: dict):
    email = user_obj.get("email")
    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user_obj, session=db.session)
        if not new_user.email:
            abort(400, "Missing required field 'email'")
        if not new_user.password:
            abort(400, "Missing required field 'password'")
        if not new_user.roles:
            default_role = Role.query.filter(Role.name == Role.default_role_name).first()
            roles = [default_role]
        else:
            roles = []
            for role in new_user.roles:
                existing_role = Role.query.filter(Role.name == role.name).one_or_none()
                if existing_role is not None:
                    roles.append(existing_role)
                else:
                    abort(400, f"Role with name '{role.name}' does not exist")
        hashed_password = bcrypt.generate_password_hash(new_user.password).decode("utf-8")
        created_user = User(email=new_user.email, password=hashed_password)
        created_user.roles = roles
        db.session.add(created_user)
        db.session.commit()
        return user_schema.dump(created_user), 201
    else:
        abort(409, f"User with email '{email}' already exists")


def get(user_id: int):
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        return user_schema.dump(existing_user), 200
    else:
        abort(404, f"User with ID '{user_id}' not found")


def put(user_id: int, user_obj: dict):
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        user_update = user_schema.load(user_obj, session=db.session)
        if user_update.email:
            existing_email = User.query.filter(User.email == user_update.email).one_or_none()
            if existing_email is None:
                existing_user.email = user_update.email
            else:
                abort(409, f"User with email '{user_update.email}' already exists")
        if user_update.password:
            hashed_password = bcrypt.generate_password_hash(user_update.password).decode("utf-8")
            existing_user.password = hashed_password
        if user_update.is_restricted:
            existing_user.is_restricted = user_update.is_restricted
        if user_update.is_silenced:
            existing_user.is_silenced = user_update.is_silenced
        if user_update.roles:
            roles_update = []
            for role in user_update.roles:
                role_update = Role.query.filter(Role.name == role.name).one_or_none()
                if role_update is not None:
                    roles_update.append(role_update)
                else:
                    abort(400, f"Role with name '{role.name}' does not exist")
            if roles_update: existing_user.roles = roles_update
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 200
    else:
        abort(404, f"User with ID '{user_id}' not found")


def delete(user_id: int):
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"User with ID '{user_id}' successfully deleted", 204)
    else:
        abort(404, f"User with ID '{user_id}' not found")
