import sqlite3
from db import db

class ArticleModel(db.Model):
    __tablename__ = 'articles'

    url =            db.Column(db.String, primary_key=True)
    title =          db.Column(db.String)
    sub_title =      db.Column(db.String)
    body =           db.Column(db.String)
    published_date = db.Column(db.String)
    article_image =  db.Column(db.String)
    source =         db.Column(db.String)

    def __init__(self, url,
                 title,
                 sub_title,
                 body,
                 published_date,
                 source,
                 article_image=None):
        self.url = url
        self.title = title
        self.sub_title = sub_title
        self.body = body
        self.published_date = published_date
        self.article_image = article_image
        self.source = source

    def json(self):
        return {
            'URL': self.url,
            'Title': self.title,
            'Sub Title': self.sub_title,
            'Body': self.body,
            'Published Date': self.published_date,
            'Article Image': self.article_image,
            'Source': self.source,
        }
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first() 
    
    @classmethod
    def save_to_db_bulk(cls, teams):
        db.session.bulk_save_objects(teams)
        db.session.commit()
    
    @classmethod
    def find_by_articles_url(cls, articles_urls):
        return cls.query.filter(ArticleModel.url.in_(articles_urls)).all() 


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()