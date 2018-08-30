from flask import Flask, jsonify, request
from functools import wraps
from werkzeug.security import check_password_hash
import jwt
import datetime
from api.database_handler import DatabaseConnection
from config import app_config
import re

db = DatabaseConnection()
app = Flask(__name__)

def create_app(env_name):
    app.config.from_object(app_config[env_name])
    def auth_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if not 'Authorization' in request.headers:
                return jsonify({"warning": "Authorization invalid"})
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token  = auth_header.split(" ")[1]
                data = jwt.decode(token, 'secret')
                current_user = db.get_user_by_username(data["user"])         
            if not token:
                return jsonify({"msg": "token is missing"})
            return f(current_user,*args, **kwargs)
        return decorated

    @app.route('/api/v1/auth/signup', methods=['POST'])
    def signup_user():
        data = request.get_json()
        name = data['name']
        if name == "":
            return jsonify({"msg": "name is missing"}), 401
        if len(name) < 5:
            return jsonify({"msg": "names too short"}), 401
        password = data['password']
        if password == "":
            return jsonify({"msg": "missing password"}), 401
        username = data['username']
        if username == "":
            return jsonify({"msg": "username is missing"}), 401
        if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password) is None:
            return jsonify({"msg":"invalid password"}), 401
        if re.match(r'^[a-zA-Z0-9_.-]+$', username) is None:
            return jsonify({"msg":"invalid username"}), 401
        user = db.get_user_by_username(username)
        if user is None:        
            db.insert_user(name, username, password)
            return jsonify({"msg":"You have registered successfully"}), 201      
        else:
            return jsonify({"msg":"User Exists"}), 400      

    @app.route('/api/v1/auth/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        username = data['username']
        if username == "":
            return jsonify({"msg": "username missing"}), 401
        if re.match(r'^[a-zA-Z0-9_.-]+$', username) is None:
            return jsonify({"msg":"invalid username"}), 401
        password = data['password']
        if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password) is None:
            return jsonify({"msg":"invalid password"}), 401
        if password == "":
            return jsonify({"msg": "password missing"}), 401
        user = db.get_user_by_username(username)
        if user is None:        
            return jsonify({"msg": "User not found please register"}), 404
        else:
            if check_password_hash(user["password"], password):
                payload = {
                    'user': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=12000)
                    }
                token = jwt.encode(payload, 'secret')
                return jsonify({"msg": "Login Successful", "token": token.decode('UTF-8')}), 200
            else:
                return jsonify({"msg": "password incorrect"}), 401

    @app.route('/api/v1/questions', methods=['POST'])
    @auth_required
    def post_questions(current_user):
        
        data = request.get_json()
        title = data['title']
        if title == "":
            return jsonify({"msg":"title missing"}), 401
        body = data['body']
        if body == "":
            return jsonify({"msg":"body is missing"}), 401
        userid = current_user["user_id"]
        db.insert_question(title, body, userid)
        return jsonify({"msg":"You have successfully created a question"}), 201

    @app.route('/api/v1/questions', methods=['GET'])
    @auth_required
    def get_questions(current_user):
        query = db.get_all_questions()
        if query == []:        
            return jsonify({"msg": "There are no questions"}), 200
        else:
            return jsonify({"questions": query}), 200
        
    @app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
    @auth_required
    def get_question_byid(current_user, question_id):
        if question_id == "":
            return jsonify({"msg": "ID should be a number"}), 400
        if type(question_id) == str:
            return jsonify({"msg": "ID should be a number"}), 400
        user_id = current_user["user_id"]
        query = db.get_all_questions()
        qn_ids = [question["user_id"] for question in query if user_id == question["user_id"]]
        if qn_ids is None:
            return jsonify({"msg": "There is no question by that id"}), 404
        else:
            return jsonify({"msg": "Question of {} has been retrieved".format(question_id)}), 201
            
    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    @auth_required
    def delete_question(current_user, question_id):
        if question_id == "":
            return jsonify({"msg": "ID should be a number"}), 400
        if type(question_id) == str:
            return jsonify({"msg": "ID should be a number"}), 400
        user_id = current_user["user_id"]
        query = db.get_all_questions()
        qn_ids = [question["user_id"] for question in query if user_id == question["user_id"]]
        if qn_ids is []:
            return jsonify({"msg": "there is question for that id"}), 404
        else:
            if question_id not in qn_ids:
                return jsonify({"msg": "there is question for that id"}), 404
            else:
                db.delete_question_byId(question_id, user_id)
                return jsonify({"msg": "question {} has been successfully deleted".format(question_id)}), 200

    @app.route('/api/v1/questions/<questionId>/answers', methods=['POST'])
    @auth_required
    def post_answer(current_user, questionId):
        data = request.get_json()
        descr = data['descr']
        if descr == "":
            return jsonify({"msg": "title missing"}), 401
        if len(descr) < 15:
            return jsonify({"msg": "too short"}), 401
        userid = current_user["user_id"]
        db.insert_answer(descr, questionId, userid)
        return jsonify({"msg": "You have successfully created an answer"}), 201

    @app.route('/api/v1/questions/<questionId>/answers/<answerId>', methods=['PUT'])
    @auth_required
    def update_answer(current_user, questionId, answerId):
        data = request.get_json()
        descr = data['descr']
        if descr == "":
            return jsonify({"msg": "title missing"}), 401
        if len(descr) < 15:
            return jsonify({"msg": "too short"}), 401
        user_id = current_user["user_id"]
        questions = db.get_all_questions()
        qn_ids = [question["user_id"] for question in questions if user_id == question["user_id"]]
        if qn_ids is []:
            return jsonify({"msg": "there is answers for that question id"}), 404
        if questionId not in qn_ids:
            return jsonify({"msg": "there is answers for that question id"}), 404
        db.update_answer(descr, questionId, answerId)
        return jsonify({"msg": "answer {} has been successfully deleted".format(answerId)}), 200

    return app
