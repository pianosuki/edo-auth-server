import json, os
from dotenv import load_dotenv
from app import app, db, bcrypt
from app.models import User, Role, ApiKey
from app.config import ROOT_DIR


def setup():
    with app.app_context():
        os.makedirs(ROOT_DIR / "instance/", exist_ok=True)

        db.drop_all()
        db.create_all()

        with open("app/conf/table_defaults.json", "r") as table_defaults:
            table_data = json.load(table_defaults)
            try:
                for role_data in table_data["roles"]:
                    role = Role(**role_data)
                    db.session.add(role)
                    db.session.commit()
                for index, user_data in enumerate(table_data["users"]):
                    if index == 0:
                        load_dotenv()
                        email = os.getenv("DEFAULT_ADMIN_EMAIL")
                        password = os.getenv("DEFAULT_ADMIN_PASSWORD")
                    else:
                        email = user_data["email"]
                        password = user_data["password"]
                    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
                    user = User(email=email, password=hashed_password)
                    for role_name in user_data["roles"]:
                        role = Role.query.filter_by(name=role_name).first()
                        user.roles.append(role)
                    db.session.add(user)
                    db.session.commit()
                for api_key_data in table_data["api_keys"]:
                    api_key = ApiKey(**api_key_data)
                    db.session.add(api_key)
                    db.session.commit()
                    print(f"Added API Key: {api_key} for User ID: {api_key.user_id}")
            except KeyError as e:
                raise ValueError(f"Incomplete configuration in 'table_defaults.json': {e}")
