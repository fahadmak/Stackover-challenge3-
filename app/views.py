from flask import Flask, jsonify, request, abort, Response

from app.model import Question, Answer, questions, answers

from werkzeug.security import check_password_hash

import jwt

import datetime

from app import app

from .database_handler import DatabaseConnection

db = DatabaseConnection()
def checkID(questionid):
    if questionid == "":
        abort(400)
    if type(questionid) != int:
        abort(400)
    if questionid not in [question["qn_id"] for question in Question.get_all_questions()]:
        abort(404)
    return questionid

@app.route('/api/v1/auth/signup', methods=['POST'])
def signup_user():
    data = request.get_json()
    name = data['name']
    if name == "":
        abort(400)
    username = data['username']
    if username == "":
        abort(400)
    password = data['password']
    if password == "":
        abort(400)
    query = db.get_user_by_username(username)
    if query is None:        
        db.insert_user(name, username, password)
        return jsonify({"msg":"You have registered successfully"}), 201
    else:
        return jsonify({"msg":"Username already exists"}), 409

@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    if username == "":
        abort(400)
    password = data['password']
    if password == "":
        abort(400)
    user = db.get_user_by_username(username)
    if user is None:        
        return jsonify({"msg":"User not found please register"}), 404
    else:
        if check_password_hash(user.password, password):
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, "hgffgd678667578689678645354645")
            return jsonify({"msg":"Login Successful", "token": token.decode('UTF-8')}), 200   

@app.route('/api/v1/questions', methods=['GET'])
def get_all_questions():
    if len(questions) == 0:
        return jsonify({"message" : "They are currently no questions"})
    qns = Question.get_all_questions()
    return jsonify({"questions": qns})


@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def get_question_byID(question_id):
    if question_id == "":
        abort(400)
    if type(question_id) != str:
        abort(400)
    if question_id:
        question_s = Question.get_all_questions()
        for question in question_s:
            if question_id == question['qn_id']:
                return jsonify(question), 200
            return jsonify({'msg': "question not found "}), 404
    else:
        question_s = Qustion.get_all_questions()
        if question_s == []:
            response = {
                "msg": " There are no rides rides at the moment"}
            return jsonify(response), 200
        return jsonify(question_s), 200


@app.route('/api/v1/questions', methods=['POST'])
def add_questions():    
    if questions == []:
        questionid = 1
    else:
        questionid = max(question["qn_id"] for question in Question.get_all_questions()) + 1
    data = request.get_json()
    title = data['title']
    if title == "":
        abort(400)
    if type(title) != str:
        abort(400)
    body = data['body']
    if body == "":
        abort(400)
    if type(body) != str:
        abort(400)
    if Question.create_question(questionid, title, body):
        return jsonify({"msg":"Question added"}), 201

@app.route('/api/v1/questions/<int:questionid>/answers', methods=['POST'])
def add_answer(questionid):
    if answers == []:
        answerid = 1
    else:
        answerid = max(answer["qn_id"] for answer in Answer.get_all_answers()) + 1
    if questionid == "":
        abort(400)
    if type(questionid) != int:
        abort(400)
    if questionid not in [question["qn_id"] for question in Question.get_all_questions()]:
        abort(404)
    data = request.get_json()
    descr = data['descr']
    if descr == "":
        abort(400)
    if type(descr) != str:
        abort(400)

    questionid = checkID(questionid)
    if Answer.create_answer(questionid, answerid, descr):
        return jsonify({"msg":"Answer added"}), 201