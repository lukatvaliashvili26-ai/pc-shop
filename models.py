from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    secure_password = db.Column(db.String(200), nullable=False)
    orders = db.relationship('UserCart', backref='owner', lazy=True)

    @property
    def id_str(self):
        return str(self.id)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    tech_type = db.Column(db.String(50), nullable=False)  # მაგალითად: CPU, GPU, RAM, SSD
    cost = db.Column(db.Float, nullable=False)
    info = db.Column(db.Text, nullable=False)
    img_link = db.Column(db.String(255), nullable=False)

class UserCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    component_id = db.Column(db.Integer, db.ForeignKey('component.id'), nullable=False)
    item = db.relationship('Component')
