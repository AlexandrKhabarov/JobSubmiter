import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Status(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.PENDING)
