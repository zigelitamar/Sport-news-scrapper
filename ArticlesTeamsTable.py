from db import db
ArticlesTeamTable = db.Table('ArticlesTeamTable',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('url', db.String, db.ForeignKey('articles.url')),
    db.Column('team_name', db.String, db.ForeignKey('teams.team_name')))