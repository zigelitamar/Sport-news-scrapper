import os
import scrapy
import json
import subprocess
from consts import ONE_TEAMS_PAGES, WALLA_TEAMS_PAGES, SPORT5_TEAMS_PAGES, TEAMS

from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from Article import ArticleModel
from TeamModel import TeamModel
from one_handler import OneHandler
from walla_handler import WallaHandler
from sport5_handler import Sport5Handler
from manager import ArticlesManager
from User import UserModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLAlchemy has its own tracker that is better
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
manager = ArticlesManager([])

@app.before_first_request
def create_tables():
    db.create_all()
    init_teams()

def init_teams():
    teams = []

    for team in TEAMS:
        team_obj = TeamModel(team_name=team,
                             one_address=ONE_TEAMS_PAGES[team],
                             walla_address=WALLA_TEAMS_PAGES[team],
                             sport5_address=SPORT5_TEAMS_PAGES[team])
        teams.append(team_obj)
    
    TeamModel.save_to_db_bulk(teams)



@app.route('/article/<path:start_urls>')
def article(start_urls):
    articles = []
    if os.path.exists("./out.json"):
        os.remove("./out.json")
    
    # start_urls = ' '.join(start_urls)
    
    
    subprocess.run(['scrapy', 'crawl', 'Article', "-a", f"start_urls={start_urls}", '-o', 'out.json'])
    with open('out.json') as json_file:
        data = json.load(json_file)
        for article in data:
            article_object = Article(**article)
            articles.append(article_object.as_json())

        return articles

@app.route('/articlespaths')
def articles_paths():
    manager = ArticlesManager(['MACCABI_TEL_AVIV', 'IRONI_KIRYAT_SHMONA'])
    return manager.get_new_articles()


@app.route('/articles')
def get_all_articles():
    start_urls = articles_paths()
    articles = article(', '.join(start_urls))
    print(articles)
    return jsonify(articles)

@app.route('/create_user')
def create_user():
    user = UserModel(username='asd', password='asd')
    user.save_to_db()
    return jsonify(user.as_json())

@app.route('/get_user/<id>')
def get_user(id):
    user = UserModel.find_by_id(id)
    return user.json()

@app.route('/register')
def regiter():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.find_by_username(username)

    if user:
        return {'Message': 'username exists already!'}, 400
    user = UserModel(username=username, password=password)
    user.save_to_db()
    return {'Message': f'Succsefully registered {user.username}'}, 201

@app.route('/login', methods=['PUT'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.find_by_username(username)

    if not user:
        return {'Message': f'{username} is not exists in database'}, 404
    
    if user.password != password:
        return {'Message': f'incorrect password'}, 401
    
    user.is_login = True
    user.save_to_db()
    return {'Message': user.json()}, 200

@app.route('/teams', methods=['POST'])
def add_teams():
    data = request.get_json()
    username =  data.get('username')
    password =  data.get('password')
    teams =     data.get('teams')

    user = UserModel.find_by_username(username)
    teams_obj_to_add = get_teams(teams)
    print(user.teams)
    user.teams.extend(teams_obj_to_add)
    user.save_to_db()

    return {'Message': user.json()}, 200


def get_teams(teams):
    data = request.get_json()
    teams =  data.get('teams')

    teams = TeamModel.find_by_teams_names(teams)
    return teams

@app.route('/get_new_articles')
def get_new_articles():
    data = request.get_json()
    username =  data.get('username')
    password =  data.get('password')

    user = UserModel.find_by_username(username=username)

    one_teams_pages = []
    walla_teams_pages = []
    sport5_teams_pages = []

    for team in user.teams:
        one_teams_pages.append(team.one_address)
        walla_teams_pages.append(team.walla_address)
        sport5_teams_pages.append(team.sport5_address)

    return manager.get_new_articles(one_teams_pages,
                                    walla_teams_pages,
                                    sport5_teams_pages)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)