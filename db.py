from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # type: SQLAlchemy

migrate = Migrate()
