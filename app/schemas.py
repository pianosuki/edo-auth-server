from marshmallow import fields
from app import db, ma
from app.models import User, Role


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    email = fields.String(required=False)
    password = fields.String(required=False)
    is_restricted = fields.Boolean(required=False)
    is_silenced = fields.Boolean(required=False)
    roles = fields.Nested("RoleSchema", many=True, order_by="id")


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

    name = fields.String(required=False)
    description = fields.String(required=False)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
