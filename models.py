from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id
