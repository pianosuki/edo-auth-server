from typing import Tuple
from flask import abort
from app import db
from app.models import ApiKey, AccessToken, RefreshToken
from app.utils import generate_token


def api_key_info(apikey: str, required_scopes) -> dict:
    info = ApiKey.query.filter_by(key=apikey).first()

    if not info:
        abort(401, "Invalid API Key")

    return {"uid": info.user_id}


def generate_token_pair(user_id: int) -> Tuple[str, str]:
    access_token = AccessToken(token=generate_token(AccessToken.default_token_length), user_id=user_id)
    db.session.add(access_token)
    db.session.commit()
    refresh_token = RefreshToken(token=generate_token(RefreshToken.default_token_length), user_id=user_id, access_token_id=access_token.id)
    db.session.add(refresh_token)
    db.session.commit()
    return access_token.token, refresh_token.token


def refresh_access_token(access_token_id: int) -> str:
    access_token = AccessToken.query.filter(AccessToken.id == access_token_id).first()
    access_token.token = generate_token(AccessToken.default_token_length)
    db.session.merge(access_token)
    db.session.commit()
    return access_token.token


def revoke_token_pair(refresh_token_id: int):
    refresh_token = RefreshToken.query.filter(RefreshToken.id == refresh_token_id).first()
    access_token = AccessToken.query.filter(AccessToken.id == refresh_token.access_token_id).first()
    refresh_token.is_revoked = True
    access_token.is_revoked = True
    db.session.merge(refresh_token)
    db.session.merge(access_token)
    db.session.commit()
