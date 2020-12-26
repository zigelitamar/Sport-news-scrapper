

import os
import scrapy
import jwt
import json
import subprocess
from datetime import datetime, timedelta
from consts import ONE_TEAMS_PAGES, WALLA_TEAMS_PAGES, SPORT5_TEAMS_PAGES, TEAMS
import time
import atexit
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, current_app
from flask import request
from flask import jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from Article import ArticleModel
from TeamModel import TeamModel
from one_handler import OneHandler
from walla_handler import WallaHandler
from sport5_handler import Sport5Handler
from manager import ArticlesManager
from User import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'noonewilleverknowiswear'
# SQLAlchemy has its own tracker that is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# To allow flask propagating exception even if debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True
manager = ArticlesManager([])
login_manager = LoginManager()
login_manager.init_app(app)


@app.before_first_request
def create_tables():
    if not os.path.exists('data.db'):
        db.create_all()
        init_teams()
    scheduler.start()


def init_teams():
    """Create teams table in DB
    """
    teams = []
    for team in TEAMS:
        team_obj = TeamModel(team_name=team,
                             one_address=ONE_TEAMS_PAGES[team],
                             walla_address=WALLA_TEAMS_PAGES[team],
                             sport5_address=SPORT5_TEAMS_PAGES[team])
        teams.append(team_obj)
    TeamModel.save_to_db_bulk(teams)


def get_new_articles():
    """Fetch new articles from One, Walla, Spot5 sites for all teams
    """
    with app.app_context():
        print("*******************************************************************************")
        print("started seearhing for articles..")
        print('Amit')
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
                  seconds=60*10, next_run_time=datetime.now()+timedelta(seconds=30))


def token_required(f):
    """Decorator methos to handle the authontication before the methods that only registered user can do.

    Args:
        f (method): Do this method if the authenticatopn succeed.

    Raises:
        RuntimeError: raise error if the authentication failed

    """
    @wraps(f)
    def _verify(*args, **kwargs):
        print(request.headers)
        auth_headers = request.headers.get('Authorization', '').split()
        print("^^")
        print(auth_headers)
        print("^^")
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = UserModel.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            # 401 is Unauthorized HTTP status code
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route('/register', methods=['POST'])
def regiter():
    """Register a new user to the web

    Returns:
        (message, status): Method results message, Status code
    """
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
    """Login to web
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.find_by_username(username)

    if not user:
        return {'Message': f'incorrect username or password'}, 401

    if not check_password_hash(user.password, password):
        return {'Message': f'incorrect username or password'}, 401

    token = jwt.encode({
        'sub': user.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    print(token)
    return jsonify({'token': token.decode('UTF-8')})


@app.route('/get_my_articles')
@token_required
def get_my_articles(auth):
    """Get the teams articls of the user that is logged in.

    Args:
        auth (UserModel): Curret logged-in user.

    Returns:
        articles (dict): List of articles as JSON format.
    """
    user = auth

    articles = {}
    for team in user.teams:
        toAdd = []

        team_articles = team.team_articles
        team_articles_sorted = sorted(
            team_articles, key=lambda k: k.published_date, reverse=True)

        for article in team_articles_sorted:
            toAdd.append(article.json())
        articles[team.team_name] = toAdd
    return articles


@app.route('/logout')
@token_required
def logout():
    """Log out the User

    Returns:
        (str): Logout message
    """
    logout_user()
    return "loggedout"


@app.route('/teams', methods=['POST'])
@token_required
def add_teams(auth):
    """Add teams to User

    Args:
        auth (UserModel): The user to add team.

    Returns:
        (message, status): Method results message, Status code
    """
    data = request.get_json()
    # username = data.get('username')
    # password = data.get('password')
    print(data)
    teams = data

    print(auth)
    user = auth

    teams_obj_to_add = get_teams(teams)
    print(user.teams)
    user.teams.extend(teams_obj_to_add)
    user.save_to_db()

    return {'Message': user.json()}, 200


@app.route('/teams')
@token_required
def get_my_teams(auth):
    """Get User teams

    Args:
        auth (UserModel): Current logged-in user

    Returns:
        (message, status): Method results message, Status code
    """
    user = auth
    res = [x.team_name for x in user.teams]
    print(res)

    return {'Message': res}, 200


@app.route('/teamsRem', methods=['POST'])
@token_required
def remove_teams(auth):
    """Remove teams from the current logged-in user

    Args:
        auth (UserModel): Current logged-in user

    Returns:
        (message, status): Method results message, Status code
    """
    data = request.json

    teams = data.get('teams')
    user = auth

    teams_remove = get_teams(teams)
    user.teams.remove(teams_remove[0])
    user.save_to_db()
    return {'Message': user.json()}, 200


def get_teams(teams):
    data = request.get_json()
    teams = data

    teams = TeamModel.find_by_teams_names(teams)
    print(teams)
    return teams


atexit.register(lambda: scheduler.shutdown())
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
