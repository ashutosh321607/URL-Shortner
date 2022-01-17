from flask import Flask, render_template, request, flash, redirect, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import datetime
import json
from utils import *
import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs559:password@localhost/testdb'
db = SQLAlchemy(app)
# creating an API object
api = Api(app)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
PORT = '5000'
ERROR_404_NOT_FOUND_PAGE_URL = "localhost:4200/404"

# function to generate a random short url
def generate_shorten_url():
  short_url = get_random_url()
  # check short_url is not already in the database
  while URLTable.query.filter_by(shorten_url=short_url).first() is not None:
    short_url = get_random_url()
  return  short_url

# funciton get shorten url for a url given by user
def get_shorten_url(url, personalized, username):
  ## check personalized is False
  if not personalized:
    # check if url exists
    data_original_urls = URLTable.query.filter_by(original_url=url).all()

    # if the url exist, we return a previously shortened url which is not created with personalised = True
    if data_original_urls != []:
        for row in data_original_urls:
          if row.personalized == False:
            if str(row.user_id) == str(username):
              pass
            else:
              short_url = row.shorten_url
              return short_url
    short_url = generate_shorten_url()
    # else generate a new url
  else:
    user_urls = URLTable.query.filter_by(original_url = url, user_id = username).all()
    if user_urls != []:
      return ''
    short_url = generate_shorten_url()
  return short_url

# function to get original url from the database
def get_original_url_from_shorten_url(shorten_url):
  return URLTable.query.filter_by(shorten_url=shorten_url).first().original_url

# function to check if given short url is already in the database
def isAvailableShortenUrl(url):
  return URLTable.query.filter_by(shorten_url=url).first() is None

class URLTable(db.Model):
  __table_name__ ='urltable'
  # id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
  original_url = db.Column(db.String(800),nullable=False)
  shorten_url = db.Column(db.String(400), nullable=False, primary_key=True)
  expire_time = db.Column(db.DateTime, nullable=False)
  created_time = db.Column(db.DateTime, nullable=False)
  personalized = db.Column(db.Boolean)

  def __init__(self, user_id, original_url, shorten_url, expire_time, created_time, personalized):
    self.user_id = user_id
    self.original_url = original_url
    self.shorten_url = shorten_url
    self.expire_time = expire_time
    self.created_time = created_time
    self.personalized = personalized


@app.route('/', methods=['POST','GET'])
def home():
    return render_template("index.html")

@app.route('/<id>')
def url_redirect(id):
  if not isAvailableShortenUrl(id):
    original_url = get_original_url_from_shorten_url(id)
    return redirect(original_url)
  else:
    return Response("URL doesn't exist", status=400)

@app.route("/get_profile_data", methods=['GET'])
def get_profile_data():
    username = request.args.get("username")
    password = request.args.get("password")
    user_data = URLTable.query.filter_by(user_id = username).all()
    profile_data_dic = {'original url':[], 'shorten url': []}
    for item in user_data:
      profile_data_dic['original url'].append(item.original_url)
      profile_data_dic['shorten url'].append(item.shorten_url)
    return Response(json.dumps(profile_data_dic), status=201)


@app.route("/post_profile_data", methods=['POST','GET'])
def post_profile_data():
  username = request.args.get("username")
  password = request.args.get("password")
  original_url = request.args.get("original_url")
  if request.args.get("expire_time") is not None:
    expiry_time = datetime.datetime.fromtimestamp(request.args.get("expire_time"))
  else:
    expiry_time = datetime.datetime.now() + datetime.timedelta(days=30)

  if request.args.get("personalized") is not None:
    personalized = request.args.get("personalized")
    if personalized.lower() == 'false':
      personalized = False
    else:
      personalized = True
  else:
    personalized = True

  custom_shorten_url = request.args.get("custom_shorten_url")
  if custom_shorten_url is None:
    shorten_url = get_shorten_url(original_url, personalized, username)
  else:
    if isAvailableShortenUrl(custom_shorten_url):
      shorten_url = custom_shorten_url
    else:
      return Response(json.dumps({"data": "URL not available"}), status=400)
  created_time = datetime.datetime.now()
  if shorten_url == '':
    return Response(json.dumps({"data": "You Already Have Shortened this URL"}), status = 400)
  entry = URLTable(user_id=username, original_url=original_url, expire_time=expiry_time, created_time=created_time,
                    shorten_url=shorten_url, personalized=personalized)
  db.session.add(entry)
  db.session.commit()
  # logic for database entry
  return Response(json.dumps({'data': f'{host_ip}:{PORT}/{shorten_url}'}), status=200)


if __name__ == '__main__':
  db.create_all()
  app.run(debug=True, host=host_ip, port="5000")
