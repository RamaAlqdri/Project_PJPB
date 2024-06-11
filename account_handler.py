import csv
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(email, username, password):
    hashed_password = generate_password_hash(password)
    user_id = f"USR-{uuid.uuid4()}"
    user_data = {
        'id': user_id,
        'email': email,
        'username': username,
        'password': hashed_password,
        'score': '0'
    }
    with open('account.csv', mode='a', newline='') as csvfile:
        fieldnames = ['id', 'email', 'username', 'password', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(user_data)
    return user_data

def validate_login(username, password):
    if os.path.isfile('account.csv'):
        with open('account.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    return check_password_hash(row['password'], password)
    return False

def get_user_data_by_username(username):
    if os.path.isfile('account.csv'):
        with open('account.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    return row
    return None


def update_user_score(username, additional_score):
    users = []
    user_found = False
    if os.path.isfile('account.csv'):
        with open('account.csv', mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    user_found = True
                    row['score'] = str(int(row['score']) + additional_score)
                users.append(row)
                # Debug print untuk memastikan data pengguna ditambahkan ke list
                print(f"Updated user score: {row}")
    
    # Debug print untuk memastikan user ditemukan
    print(f"User found: {user_found}")
    print(f"Users data: {users}")

    if not user_found:
        return False  # User not found

    # Tulis kembali ke file CSV hanya jika ada data pengguna
    if users:
        with open('account.csv', mode='w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['id', 'email', 'username', 'password', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            try:
                writer.writerows(users)
                print("Write successful")
            except Exception as e:
                print(f"Write failed: {e}")
    
    return True

def update_user_profile(username, data):
    users = []
    user_found = False
    if os.path.isfile('account.csv'):
        with open('account.csv', mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    user_found = True
                    if 'email' in data:
                        row['email'] = data['email']
                    if 'password' in data:
                        row['password'] = generate_password_hash(data['password'])
                users.append(row)
                # Debug print untuk memastikan data pengguna ditambahkan ke list
                print(f"Updated user: {row}")
    
    # Debug print untuk memastikan user ditemukan
    print(f"User found: {user_found}")
    print(f"Users data: {users}")

    if not user_found:
        return False  # User not found

    # Debug print untuk memeriksa format data sebelum menulis ke file
    for user in users:
        print(f"User to write: {user}")

    # Tulis kembali ke file CSV hanya jika ada data pengguna
    if users:
        with open('account.csv', mode='w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['id', 'email', 'username', 'password', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            try:
                writer.writerows(users)
                print("Write successful")
            except Exception as e:
                print(f"Write failed: {e}")
    
    return True
