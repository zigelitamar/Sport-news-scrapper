from db import db

UsersTeams = db.Table('UsersTeams',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('username', db.String, db.ForeignKey('users.username')),
    db.Column('team_name', db.String, db.ForeignKey('teams.team_name')))