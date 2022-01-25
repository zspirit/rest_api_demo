# import functools
import bcrypt

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import random
from datetime import datetime
from flask_mail import Mail, Message

#Init Flask App
app = Flask(__name__)
api = Api(app)
mail = Mail(app)

#Flask mail config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Mongodb connection
client = MongoClient("mongodb://my_db:27017")
db = client.projectDB
users = db["Users"]
invalid_user_json = {"status": 200, "msg": "Invalid Username"}
invalid_password_json = {"status": 200, "msg": "Invalid password"}
invalid_verification_json = {"status": 200, "msg": "Invalid verification code / delay"}
invalid_username_pwd_json = {"status": 200, "msg": "Invalid username/password"}


"""
HELPER FUNCTIONS
"""

def user_exist(username, email):
    return users.find_one({"Username": username, "email": email})

def verify_user(username, email, password):
    if not user_exist(username, email):
        return False
    user_hashed_pw = users.find_one({"Username": username, "email": email})["Password"]
    return bcrypt.checkpw(password.encode('utf8'), user_hashed_pw)

"""
RESOURCES
"""

@api.representation('application/json')
class HealthCheck(Resource):
    """
    This is the HealthCheck resource class
    """

    def get(self):
        return "Working fine!"

@api.representation('application/json')
class Register(Resource):
    """
    This is the Register class
    """

    def post(self):
        # Get posted data from request
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        email    = data["email"]

        # check if user exists
        if user_exist(username, email):
            return jsonify(invalid_user_json)

        # encrypt password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        codeverification = random.randint(1000, 9999)

        # Insert record
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "email": email,
            "codeverification": codeverification,
            "registration_date": datetime.now(),
            "confirmed": False
        })

        #Not tested yet
        msg = Message('Hello', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = "Hello, this is your code verification to confirm your account : " + codeverification
        mail.send(msg)

        # Return successful result
        ret_json = {
            "status": 200,
            "msg": "Registration successful, please check your mail to confirm your account"
        }
        return jsonify(ret_json)

@api.representation('application/json')
class Confirm(Resource):
    """
    This is the Confirm class
    """

    def post(self):
        # Get posted data from request
        data = request.get_json()
        confirmationcode = data["confirmationcode"]
        username = data["username"]
        email = data["email"]

        # check if user exists
        user_to_check = user_exist(username, email)
        if user_to_check:
            #check if the confirmation code is Ok & check registration date (the user got less then 1min to confirm mail adress
            if user_to_check.codeverification == confirmationcode and (datetime.now() - user_to_check.registration_date).seconds < 60:
                users.update({
                    "Username": username,
                    "confirmed": True,
                    "last_update_date": datetime.now()
                }, )
            else:
                return jsonify(invalid_verification_json)
        else:
            return jsonify(invalid_username_pwd_json)

        # Return successful result
        ret_json = {
            "status": 200,
            "msg": "Congrats !! your account is now activated"
        }
        return jsonify(ret_json)

@api.representation('application/json')
class Dashboard(Resource):
    """
    This is the Dashboard class
    """
    def post(self):
         # Get posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]
        email = data["email"]

        # check if user exists
        if not user_exist(username, email):
            return jsonify(invalid_user_json)

        # check password
        if not verify_user(username, email, password):
            return jsonify(invalid_password_json)

        # doing some stuff...
        messages = "Welcome to your dashboard"

        # Build successful response
        ret_json = {
            "status": 200,
            "obj": messages
        }

        return jsonify(ret_json)

@api.representation('application/json')
class Update(Resource):
    """
    This is the Save class
    """

    def post(self):
         # Get posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]
        email = data["email"]

        # check if user exists
        if not user_exist(username, email):
            return jsonify(invalid_user_json)

        # check password
        if not verify_user(username, email, password):
            return jsonify(invalid_password_json)

        # save the new user data
        users.update({
            "Username": username
        }, )

        ret_json = {
            "status": 200,
            "msg": "User has been saved successfully"
        }
        return jsonify(ret_json)

api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(Register, '/register')
api.add_resource(Dashboard, '/dashboard')
api.add_resource(Update, '/update')
api.add_resource(Confirm, '/confirm')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5000)
