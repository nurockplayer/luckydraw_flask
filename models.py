from datetime import datetime

from db import db


class Restaurant(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    desc = db.Column(db.String(255), nullable=False)
    site_url = db.Column(db.String(255), nullable=False)
    draw = db.Column(db.Integer, nullable=False, default=0)

    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    histories = db.relationship('History', back_populates='restaurant', cascade='all,delete')


class History(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)

    create_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow())
    update_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    restaurant_id = db.Column(db.ForeignKey(Restaurant.id))
    restaurant = db.relationship('Restaurant', back_populates='histories', cascade='all,delete', uselist=False)
