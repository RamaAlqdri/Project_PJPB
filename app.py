import csv
import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from account_handler import register_user, validate_login, get_user_data_by_username, update_user_score, update_user_profile
from artikel_handler import get_all_artikel_data, get_artikel_data_by_id

app = Flask(__name__)
app.secret_key = 'pjpb'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/user/<username>', methods=['GET'])
def getUserbyUsername(username):
    data = get_user_data_by_username(username)
    if data:
        return jsonify(data), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    username = data['username']
    password = data['password']
    print(username)
    print(password)
    if os.path.isfile('account.csv'):
        with open('account.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['email'] == email or row['username'] == username:
                    return jsonify({'error': 'Email or username already exists'}), 409
    user_data = register_user(email, username, password)
    return jsonify(user_data), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username)
    print(password)
    if validate_login(username, password):
        data = get_user_data_by_username(username)
        session['user'] = username
        session['email'] = data['email']
        session['score'] = data['score']
        return jsonify(
            { 'username': username,
                'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({"status": "Session active", "user": session['user']}), 200
    else:
        return jsonify({"status": "Session inactive"}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'You have been logged out'}), 200

@app.route('/artikel', methods=['GET'])
def get_all_artikel():
    data = get_all_artikel_data()
    return jsonify(data), 200

@app.route('/artikel/<id>', methods=['GET'])
def get_artikel_by_id(id):
    data = get_artikel_data_by_id(id)
    if data:
        return jsonify(data), 200
    return jsonify({'error': 'Artikel tidak ditemukan'}), 404

@app.route('/artikel/<id>/jawab', methods=['POST'])
def jawab_pertanyaan(id):
    # if 'user' not in session:
    #     return jsonify({'error': 'User not logged in'}), 401
    
    data = request.get_json()
    jawaban_user = data['jawaban']  # List jawaban user untuk 5 pertanyaan
    
    artikel = get_artikel_data_by_id(id)
    if not artikel:
        return jsonify({'error': 'Artikel tidak ditemukan'}), 404
    
    jawaban_benar = [
        artikel['answer1'],
        artikel['answer2'],
        artikel['answer3'],
        artikel['answer4'],
        artikel['answer5']
    ]
    
    score = 0
    for i in range(5):
        if str(jawaban_user[i]).lower() == jawaban_benar[i].lower():
            score += 1
    
    username = data['username']
    update_user_score(username, score)
    
    return jsonify({'message': 'Jawaban diterima', 'score': score}), 200

@app.route('/profil', methods=['PUT'])
def update_profile():
    # if 'user' not in session:
    #     return jsonify({'error': 'User not logged in'}), 401
    
    data = request.get_json()
    username = session['user']
    # print(username)
    
    update_user_profile(username, data)
    return jsonify({'message': 'Profil diperbarui'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
