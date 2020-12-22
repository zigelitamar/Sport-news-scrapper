import os
import scrapy
import json
import subprocess
from datetime import datetime, timedelta
from consts import ONE_TEAMS_PAGES, WALLA_TEAMS_PAGES, SPORT5_TEAMS_PAGES, TEAMS
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Article import ArticleModel
from TeamModel import TeamModel
from one_handler import OneHandler
from walla_handler import WallaHandler
from sport5_handler import Sport5Handler
from manager import ArticlesManager
from User import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'noonewilleverknowiswear'
# SQLAlchemy has its own tracker that is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# To allow flask propagating exception even if debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True
manager = ArticlesManager([])
login_manager = LoginManager()
login_manager.init_app(app)


def get_new_articles():
    with app.app_context():
        print("*******************************************************************************")
        print("started seearhing for articles..")
        print("*******************************************************************************")
        one_teams_pages = []
        walla_teams_pages = []
        sport5_teams_pages = []
        for team in TEAMS:
            one_teams_pages.append(ONE_TEAMS_PAGES[team])
            walla_teams_pages.append(WALLA_TEAMS_PAGES[team])
            sport5_teams_pages.append(SPORT5_TEAMS_PAGES[team])
        manager.get_new_articles(one_teams_pages,
                                 walla_teams_pages,
                                 sport5_teams_pages)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("finished seearhing for articles..")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_new_articles, trigger="interval",
                  seconds=60*15, next_run_time=datetime.now()+timedelta(seconds=15))


@app.before_first_request
def create_tables():
    print('hi')
    # init_teams()
    # scheduler.start()

    # def init_teams():
    #     teams = []
    #     for team in TEAMS:
    #         team_obj = TeamModel(team_name=team,
    #                              one_address=ONE_TEAMS_PAGES[team],
    #                              walla_address=WALLA_TEAMS_PAGES[team],
    #                              sport5_address=SPORT5_TEAMS_PAGES[team])
    #         teams.append(team_obj)
    #     TeamModel.save_to_db_bulk(teams)


@login_manager.user_loader
def load_user(userid):
    return UserModel.query.get(int(userid))


# @app.route('/')
# def start():
#     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#     return render_template("index.html")


@app.route('/register', methods=['POST'])
def regiter():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.find_by_username(username)

    if user:
        return {'Message': 'username exists already!'}, 400
    user = UserModel(username=username,
                     password=generate_password_hash(password))

    user.save_to_db()
    return {'Message': f'Succsefully registered {user.username}'}, 201


@app.route('/login', methods=['POST'])
def login():
    print("i got here")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.find_by_username(username)
    login_user(user)
    if not user:
        return {'Message': f'incorrect username or password'}, 401

    if not check_password_hash(user.password, password):
        return {'Message': f'incorrect username or password'}, 401

    user.save_to_db()
    return {'Message': user.json()}, 200


@app.route('/get_my_articles')
@login_required
def get_my_articles():

    user = current_user

    articles = {}
    for team in user.teams:
        toAdd = []
        for article in ArticleModel.find_by_team(team.team_name).all():
            toAdd.append(article.json())
        articles[team.team_name] = toAdd
    return articles


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "loggedout"


@app.route('/teams', methods=['POST'])
@login_required
def add_teams():
    data = request.get_json()
    # username = data.get('username')
    # password = data.get('password')
    teams = data.get('teams')

    user = current_user

    teams_obj_to_add = get_teams(teams)
    print(user.teams)
    user.teams.extend(teams_obj_to_add)
    user.save_to_db()

    return {'Message': user.json()}, 200


@app.route('/teamsRem', methods=['POST'])
@login_required
def remove_teams():
    data = request.json
    teams = data.get('teams')
    user = current_user

    teams_remove = get_teams(teams)
    user.teams.remove(teams_remove[0])
    user.save_to_db()
    return {'Message': user.json()}, 200


def get_teams(teams):
    data = request.get_json()
    teams = data.get('teams')

    teams = TeamModel.find_by_teams_names(teams)
    print(teams)
    return teams


atexit.register(lambda: scheduler.shutdown())
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
