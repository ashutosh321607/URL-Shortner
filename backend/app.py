from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
from utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs559:password@localhost/db_testlearn'
db = SQLAlchemy(app)

def get_shortan_url(url):
  short_url = get_random_url()
 
  # check short_url is not already in the database
  while URLTable.query.filter_by(shorten_url=short_url).first() is not None:
     short_url = get_random_url()
  
  return short_url
  
class URLTable(db.Model):
  __table_name__ ='urltable'
  # id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(80), unique=False, nullable=False)
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


@app.route("/profile", methods=['POST','GET'])
def profile():
    if request.method == 'POST':
      username = request.form["username"]
      password = request.form["password"]
      user_data = URLTable.query.filter_by(user_id = username).all()
    else:
      user_data=[]


    return render_template("profile.html",user_data=user_data, username = username, password = password)
    # entry = URL_Table(pname, color)
    # db.session.add(entry)
    # db.session.commit()
@app.route("/confirm", methods=['POST','GET'])
def confirm():
  if request.method == 'POST':
    username = request.form["username"]
    password = request.form["password"]
    original_url = request.form["original_url"]
    try:
      expiry_time = convert_to_python_datetime(request.form["expiry_time"])
    except:
      expiry_time = datetime.datetime.now() + datetime.timedelta(days=30)

    if request.form["personalized"] is None:
      personalized = False
    else:
      temp = request.form["personalized"]
      if temp == 'False':
        personalized = False
      else:
        personalized = True
    shorten_url = get_shortan_url(original_url)
    created_time = datetime.datetime.now()
    entry = URLTable(user_id=username, original_url=original_url, expire_time=expiry_time, created_time=created_time,
                      shorten_url=shorten_url, personalized=personalized)
    db.session.add(entry)
    db.session.commit()
    # logic for database entry
    return render_template("confirm.html", username = username, password=password)


if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
