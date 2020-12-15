import sqlite3
from db import db


class TeamModel(db.Model):
    __tablename__ = 'teams'

    team_name = db.Column(db.String(80), primary_key=True)
    one_address = db.Column(db.String)
    walla_address = db.Column(db.String)
    sport5_address = db.Column(db.String)

    def __init__(self, team_name, one_address, walla_address, sport5_address):
        # self.id = id
        self.team_name = team_name
        self.one_address = one_address
        self.walla_address = walla_address
        self.sport5_address = sport5_address

    @classmethod
    def save_to_db_bulk(cls, teams):
        db.session.bulk_save_objects(teams)
        db.session.commit()

    @classmethod
    def find_by_teams_names(cls, teams_names):
        return cls.query.filter(TeamModel.team_name.in_(teams_names)).all()

    def json(self):
        return{
            'Team Name': self.team_name,
            'One Address': self.one_address,
            'Walla Address': self.walla_address,
            'Sport5 Address': self.sport5_address
        }
