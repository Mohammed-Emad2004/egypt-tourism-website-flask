from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from app.models import Place
from dotenv import load_dotenv
import os

from app.models import db

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)


def ensure_database_exists():
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]

    url = make_url(db_uri)

    db_name = url.database

    server_uri = (
        f"{url.drivername}://"
        f"{url.username}:{url.password}"
        f"@{url.host}:{url.port}"
    )

    engine = create_engine(server_uri)

    with engine.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                "CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_unicode_ci"
            )
        )
        conn.commit()


from app.routes.home import home_bp
from app.routes.about import about_bp
from app.routes.contact import contact_bp
from app.routes.gallery import gallery_bp
from app.routes.destinations import destinations_bp
from app.routes.place_details import place_details_bp
from app.routes.auth import auth_bp
from app.routes.flights import flights_bp
from app.routes.profile import profile_bp
from app.routes.admin import admin_bp

app.register_blueprint(home_bp)
app.register_blueprint(about_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(destinations_bp)
app.register_blueprint(place_details_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(flights_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    ensure_database_exists()
    upgrade()
    try:
        from app.models import Place
        if db.session.query(Place.id).first() is None:
            from seed import seed_database
            seed_database()
    except Exception:
        pass