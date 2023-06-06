import pathlib, json, os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
APP_DIR = ROOT_DIR / "app/"
CONF_DIR = APP_DIR / "conf/"

with open(f"{CONF_DIR}/options.json") as f:
    OPTIONS = json.load(f)

CONNEXION_ARGS = [
    "Edo Authentication Server"
]

CONNEXION_KWARGS = {
    "specification_dir": CONF_DIR,
    "options": OPTIONS,
    "server": "flask",
    "server_args": {
        "static_url_path": "/",
        "static_folder": "static/",
        "template_folder": "app/templates/"
    }
}


def configure_app(app: Flask):
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{ROOT_DIR / 'instance/database.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
