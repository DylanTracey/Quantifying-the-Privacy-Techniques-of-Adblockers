from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from utils.cookies import generate_uuid

db = SQLAlchemy()

BASE_UUID_LENGTH = 32
URL_MAX_LENGTH = 256


class BaseUUID(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(BASE_UUID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def isFull(self, maximum_rows):
        return self.query.count() >= maximum_rows

    def delete_oldest(self):
        oldest_user = self.query.order_by(self.timestamp.asc()).first()
        db.session.delete(oldest_user)
        db.session.commit()

    def generate_unused_uuid(self, length):
        uuid = generate_uuid(length)
        while self.query.filter_by(uuid=uuid).count() >= 1:
            uuid = generate_uuid(length)
        return uuid


class BaseHistory(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(URL_MAX_LENGTH))
    ip = db.Column(db.String(URL_MAX_LENGTH))
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
