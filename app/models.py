from datetime import datetime
from app import db
from app.utils import generate_uuid, generate_token

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False, default=generate_uuid)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_restricted = db.Column(db.Boolean, default=False)
    is_silenced = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        lazy="select",
        backref=db.backref("users", lazy="dynamic")
    )


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    default_role_name = "User"

    def __repr__(self):
        return self.name


class ApiKey(db.Model):
    __tablename__ = "api_keys"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, default=generate_token(32))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.key


class AccessToken(db.Model):
    __tablename__ = "access_tokens"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, default=generate_token(32))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_revoked = db.Column(db.Boolean, default=False)
    refresh_token = db.relationship(
        "RefreshToken",
        back_populates="access_token"
    )

    default_token_length = 32

    def __repr__(self):
        return self.token


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, default=generate_token(32))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    access_token_id = db.Column(db.Integer, db.ForeignKey("access_tokens.id"), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_revoked = db.Column(db.Boolean, default=False)
    access_token = db.relationship(
        "AccessToken",
        back_populates="refresh_token"
    )

    default_token_length = 32

    def __repr__(self):
        return self.token
