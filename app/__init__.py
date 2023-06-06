import connexion
from connexion.resolver import RestyResolver
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from app.config import *

connex_app = connexion.FlaskApp(*CONNEXION_ARGS, **CONNEXION_KWARGS)

app = connex_app.app
configure_app(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

connex_app.add_api("api_v1.yml", resolver=RestyResolver("api.v1"))

from app import models, schemas, routes
from app.models import User, Role, ApiKey
