from flask import Flask, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, abort
import datetime
from utils import *
import socket

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
db = SQLAlchemy(app)

host_name = socket.gethostname()
host_private_ip = socket.gethostbyname(host_name)
host_public_ip = socket.gethostbyname(host_name)
PORT = '5000'

SHORT_URL_LENGTH = 6
API_KEY_LENGTH = 32


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.full_name}', '{self.password}', '{self.api_key}')"
    

class UnvarifiedUserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=False)
    varifiation_otp = db.Column(db.String(120), nullable=False)


class URLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=False, nullable=False)
    long_url = db.Column(db.String(800), nullable=False)
    short_url = db.Column(db.String(100), nullable=False, unique=True)
    expire_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"URLModel(id = {self.id}, user_id = {self.user_id}, long_url = {self.long_url}, short_url = {self.short_url}, expire_time = {self.expire_time}, created_time = {self.created_time})"

# argument parser for shorten url
url_post_args = reqparse.RequestParser()
url_post_args.add_argument(
    'long_url', type=str, required=True, help='long url is required')
url_post_args.add_argument('short_url', type=str,
                           required=False, help='custom short url optional')
url_post_args.add_argument(
    'api_key', type=str, required=True, help='api key is required')
url_post_args.add_argument('time_period', type=int,
                           required=False, help='time period optional')




def get_user_id_from_api_key(api_key):
    return UserModel.query.filter_by(api_key=api_key).first().id

# function to generate a random short url


def generate_shorten_url():
    short_url = get_random_string(SHORT_URL_LENGTH)
    # check short_url is not already in the database
    while URLModel.query.filter_by(short_url=short_url).first() is not None:
        short_url = get_random_string(SHORT_URL_LENGTH)
    return short_url


class ShortURL(Resource):
    def post(self):
        # cool down if user is trying to post too many urls
        # need to be added

        args = url_post_args.parse_args()
        user_id = get_user_id_from_api_key(args['api_key'])
        if user_id is None:
            abort(http_status_code=401, message="Unauthorized / Invalid API Key")
        url = URLModel(user_id=user_id, long_url=args.long_url,
                       created_time=datetime.datetime.now())

        # if the user has shorten the long url before
        if URLModel.query.filter_by(long_url=args.long_url).filter_by(user_id=user_id).first() is not None:
            abort(http_status_code=409, message=f"URL already shortened", link=f"http://{host_public_ip}:{PORT}/{URLModel.query.filter_by(long_url=args.long_url).filter_by(user_id=user_id).first().short_url}")


        if args.short_url:
            # check if short url is unique
            if URLModel.query.filter_by(short_url=args.short_url).first():
                abort(http_status_code=400, message="Short URL is already taken")
            url.short_url = args.short_url
        else:
            url.short_url = generate_shorten_url()

        if args.time_period:
            url.expire_time = datetime.datetime.now(
            ) + datetime.timedelta(seconds=args.time_period)
        else:
            url.expire_time = datetime.datetime.now() + datetime.timedelta(days=1)

        db.session.add(url)
        db.session.commit()
        return {'short_url': f"http://{host_public_ip}:{PORT}/{url.short_url}"}, 201


# argument parser for register user
user_register_args = reqparse.RequestParser()
user_register_args.add_argument(name='email', type=str, required=True)
user_register_args.add_argument(name='full_name', type=str, required=True)
user_register_args.add_argument(name='password', type=str, required=True)


class RegisterUser(Resource):
    def post(self):
        args = user_register_args.parse_args()
        user = UnvarifiedUserModel(email=args.email,
                         full_name=args.full_name, password=args.password)

        # check if user already exists
        if UserModel.query.filter_by(email=args.email).first():
            abort(http_status_code=400, message="User already exists")
        
        # check if user had requested to register before delete that request
        if UnvarifiedUserModel.query.filter_by(email=args.email).first():
            UnvarifiedUserModel.query.filter_by(email=args.email).first().delete()
        
        # generate otp and send email
        otp = generate_otp()
        
        # send email
        try:
            send_email_with_otp(email=args.email, otp=otp)
        except Exception as e:
            abort(http_status_code=500, message="Internal Server Error")
        
        # generate api key
        user.api_key = get_random_string(length=API_KEY_LENGTH)
        while UserModel.query.filter_by(api_key=user.api_key).first() is not None:
            user.api_key = get_random_string(length=API_KEY_LENGTH)

        db.session.add(user)
        db.session.commit()
        return {'message': 'OTP sent to email'}, 201

# argument parser for user varification
user_varification_args = reqparse.RequestParser()
user_varification_args.add_argument(name='email', type=str, required=True)
user_varification_args.add_argument(name='otp', type=str, required=True)

class VerifyUser(Resource):
    def post(self):
        args = user_varification_args.parse_args()
        entry = UnvarifiedUserModel.query.filter_by(email=args.email).filter_by(varifiation_otp=args.otp).first()
        # check if otp and email is valid
        if entry is None:
            abort(http_status_code=400, message="OTP is invalid")
        
        user = UserModel(email=entry.email, full_name=entry.full_name, password=entry.password, api_key=entry.api_key)
        UnvarifiedUserModel.query.filter_by(email=args.email).delete()
        db.session.add(user)
        db.session.commit()
        return {'api_key': user.api_key}, 201
        


# argument parser for login user
user_login_args = reqparse.RequestParser()
user_login_args.add_argument(name='email', type=str, required=True)
user_login_args.add_argument(name='password', type=str, required=True)


class loginUser(Resource):
    def post(self):
        args = user_login_args.parse_args()
        user = UserModel.query.filter_by(email=args.email).first()
        if user is None:
            abort(http_status_code=400, message="User does not exist")
        if user.password != args.password:
            abort(http_status_code=400, message="Wrong password")
        return {'api_key': user.api_key}, 201


# url redirection to long url
@app.route('/<shortlink>')
def url_redirect(shortlink):
    if URLModel.query.filter_by(short_url=shortlink).first() is not None:
        long_url = URLModel.query.filter_by(short_url=shortlink).first().long_url
        return redirect(long_url)
    else:
        return redirect(f"{host_public_ip}:{PORT}/404")


api.add_resource(ShortURL, '/api/shorten')
api.add_resource(loginUser, '/api/login')
api.add_resource(RegisterUser, '/api/register')
api.add_resource(VerifyUser, '/api/verify')


# # funciton get shorten url for a url given by user


# def get_shorten_url(url, personalized, username):
#     # check personalized is False
#     if not personalized:
#         # check if url exists
#         data_long_urls = URLTable.query.filter_by(long_url=url).all()

#         # if the url exist, we return a previously shortened url which is not created with personalised = True
#         if data_long_urls != []:
#             for row in data_long_urls:
#                 if row.personalized == False:
#                     if str(row.user_id) != str(username):
#                         short_url = row.shorten_url
#                         return short_url
#         short_url = generate_shorten_url()
#         # else generate a new url
#     else:
#         user_urls = URLTable.query.filter_by(
#             long_url=url, user_id=username).all()
#         if user_urls != []:
#             return ''
#         short_url = generate_shorten_url()
#     return short_url

# # function to get original url from the database


# def get_long_url_from_shorten_url(shorten_url):
#     return URLTable.query.filter_by(shorten_url=shorten_url).first().long_url


# @app.route('/', methods=['POST', 'GET'])
# def home():
#     return render_template("index.html")


# @app.route("/get_profile_data", methods=['GET'])
# def get_profile_data():
#     username = request.args.get("username")
#     password = request.args.get("password")
#     user_data = URLTable.query.filter_by(user_id=username).all()
#     profile_data_dic = {'original url': [], 'shorten url': []}
#     for item in user_data:
#         profile_data_dic['original url'].append(item.long_url)
#         profile_data_dic['shorten url'].append(item.shorten_url)
#     return Response(json.dumps(profile_data_dic), status=201)


# @app.route("/post_profile_data", methods=['POST', 'GET'])
# def post_profile_data():
#     username = request.args.get("username")
#     password = request.args.get("password")
#     long_url = request.args.get("long_url")
#     if request.args.get("expire_time") is not None:
#         expiry_time = datetime.datetime.fromtimestamp(
#             request.args.get("expire_time"))
#     else:
#         expiry_time = datetime.datetime.now() + datetime.timedelta(days=30)

#     if request.args.get("personalized") is not None:
#         personalized = request.args.get("personalized")
#         if personalized.lower() == 'false':
#             personalized = False
#         else:
#             personalized = True
#     else:
#         personalized = True

#     custom_shorten_url = request.args.get("custom_shorten_url")
#     if custom_shorten_url is None:
#         shorten_url = get_shorten_url(long_url, personalized, username)
#     else:
#         if isAvailableShortenUrl(custom_shorten_url):
#             shorten_url = custom_shorten_url
#         else:
#             return Response(json.dumps({"data": "URL not available"}), status=400)
#     created_time = datetime.datetime.now()
#     if shorten_url == '':
#         return Response(json.dumps({"data": "You Already Have Shortened this URL"}), status=400)
#     entry = URLTable(user_id=username, long_url=long_url, expire_time=expiry_time, created_time=created_time,
#                      shorten_url=shorten_url, personalized=personalized)
#     db.session.add(entry)
#     db.session.commit()
#     # logic for database entry
#     return Response(json.dumps({'data': f'{host_ip}:{PORT}/{shorten_url}'}), status=200)


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    app.run(debug=True, host=host_public_ip, port="5000")
