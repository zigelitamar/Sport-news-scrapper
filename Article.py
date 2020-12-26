import sqlite3
import ArticlesTeamsTable
from datetime import datetime
from db import db


class ArticleModel(db.Model):
    __tablename__ = 'articles'

    url = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    sub_title = db.Column(db.String)
    body = db.Column(db.String)
    published_date = db.Column(db.Integer)
    article_image = db.Column(db.String)
    source = db.Column(db.String)
    article_teams = db.relationship(
        'TeamModel', secondary=ArticlesTeamsTable.ArticlesTeamTable, backref='articles')

    def __init__(self, url,
                 title,
                 sub_title,
                 body,
                 published_date,
                 source,
                 article_teams=[],
                 article_image=None):
        self.url = url
        self.article_teams = article_teams
        self.title = title
        self.sub_title = sub_title
        self.body = body
        self.published_date = int(datetime.strptime(
            published_date, '%d/%m/%Y %H:%M').timestamp())
        self.article_image = article_image
        self.source = source

    def set_team(self, x):
        self.team = x

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_team(cls, team):
        return cls.query.filter_by(team=team, source='One')

    @classmethod
    def save_to_db_bulk(cls, article_teams):
        db.session.bulk_save_objects(article_teams)
        db.session.commit()

    @classmethod
    def find_by_articles_url(cls, articles_urls):
        return cls.query.filter(ArticleModel.url.in_(articles_urls)).all()

    @classmethod
    def find_by_articles_url_one(cls, url):
        return cls.query.filter_by(url=url).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'title': self.title,
            'sub_title': self.sub_title,
            'body': self.body,
            'date': datetime.utcfromtimestamp(self.published_date).strftime('%d-%m-%Y %H:%M'),
            'image': self.article_image,
            'source': self.source
        }
