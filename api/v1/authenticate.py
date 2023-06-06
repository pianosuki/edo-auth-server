from flask import abort, make_response, jsonify
from app import bcrypt
from app.models import User, AccessToken, RefreshToken
from app.auth import generate_token_pair, refresh_access_token, revoke_token_pair


def search(access_token: str):
    valid_access_token = AccessToken.query.filter(AccessToken.token == access_token, AccessToken.is_revoked is False).one_or_none()

    if valid_access_token is not None:
        user = User.query.filter(User.id == valid_access_token.user_id).first()
        return jsonify({"uuid": user.uuid}), 200
    else:
        abort(401, "Invalid access token")


def post(credentials_obj: dict):
    if "email" in credentials_obj and "password" in credentials_obj:
        existing_user = User.query.filter(User.email == credentials_obj["email"]).one_or_none()
        if existing_user is not None:
            valid_password = bcrypt.check_password_hash(existing_user.password, credentials_obj["password"])
            if valid_password:
                access_token, refresh_token = generate_token_pair(existing_user.id)
                return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 201
            else:
                abort(401, "Invalid credentials")
        else:
            abort(401, "Invalid credentials")
    else:
        abort(400, "Missing required property(s)")


def put(refresh_token: str):
    valid_refresh_token = RefreshToken.query.filter(RefreshToken.token == refresh_token, RefreshToken.is_revoked is False).one_or_none()

    if valid_refresh_token is not None:
        access_token = refresh_access_token(valid_refresh_token.access_token_id)
        return jsonify({"access_token": access_token}), 200
    else:
        abort(401, "Invalid refresh token")


def delete(refresh_token: str):
    valid_refresh_token = RefreshToken.query.filter(RefreshToken.token == refresh_token, RefreshToken.is_revoked is False).one_or_none()

    if valid_refresh_token is not None:
        revoke_token_pair(valid_refresh_token.id)
        return make_response("Token pair successfully revoked", 204)
    else:
        abort(401, "Invalid refresh token")
