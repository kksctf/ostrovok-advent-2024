from pathlib import Path

from ext import db, login_manager
from flask import Flask
from routes import main
from migration_db import create_users_notes_logs


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(__file__).parent}/notes.db"

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        create_users_notes_logs()

    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=1337)
