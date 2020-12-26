import sqlite3
import UsersTeamsTable
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    teams = db.relationship(
        'TeamModel', secondary=UsersTeamsTable.UsersTeams, backref='users')

    def __init__(self, username, password, teams=[]):
        # self.id = id
        self.username = username
        self.password = password
        self.teams = teams

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def save_to_db_bulk(cls, teams):
        db.session.bulk_save_objects(teams)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'username': self.username,
                'Teams': [team.json() for team in self.teams]}
