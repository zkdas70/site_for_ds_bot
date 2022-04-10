# from requests import get
#
#
# print(get('http://127.0.0.1:5000/api/news').json())
# print(get('http://localhost:5000/api/news/1').json())
# print(get('http://localhost:5000/api/news/999').json())
# print(get('http://localhost:5000/api/news/q').json())
from flask import Flask, render_template, redirect, request, make_response, \
    session, abort, jsonify
from data import db_session, news_api
from data.users_default import users_default, users_to_servers
from data.news import News
from forms.user import LoginFormDefault, RegisterFormDefault
from forms.news import NewsForm
from flask_login import LoginManager, login_user, current_user, logout_user, \
    login_required
import datetime

db_sess = db_session.create_session()

print(db_sess.query(users_to_servers).filter(users_to_servers.users == current_user.id))