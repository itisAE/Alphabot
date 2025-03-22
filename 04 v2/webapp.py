from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

nomeDB='users.db'
chiave_segreta='tpsit2024|2025'

app = Flask(__name__)

def aggiungiInDB(user,psw):
    conn = sqlite3.connect(nomeDB)
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO users (username, password) 
                            VALUES (?,?) ''',(user,psw))
    conn.commit()
    conn.close()

def cercaInDB(user,psw):
    conn = sqlite3.connect(nomeDB)
    cursor = conn.cursor()
    cursor.execute('''SELECT * 
                   FROM users 
                   WHERE username=?''',(user,))
    risultati = cursor.fetchall()
    conn.close()
    print(risultati)
    if len(risultati) > 0:  
        if check_password_hash(risultati[0][1], psw):
            return True
    return False

def controllaSePossibileCreare(user):
    conn = sqlite3.connect(nomeDB)
    cursor = conn.cursor()
    cursor.execute('''SELECT username 
                   FROM users 
                   WHERE username=?''',(user,))
    risultati = cursor.fetchall()
    conn.close()
    print(risultati)
    if len(risultati) > 0:
        return False
    return True

def validate(username,psw):
    print(username)
    if cercaInDB(username,psw):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Scadenza tra 1 ora
        }
        token = jwt.encode(payload, chiave_segreta, algorithm='HS256')
        risposta = redirect(url_for('home'))
        risposta.set_cookie('token', token, max_age=60*60*24, httponly=True, samesite='Strict')
        return risposta
    else:
        return render_template('login.html', alert='Account non esistente!')

def createAccount(username,psw):
    print(username)
    if not controllaSePossibileCreare(username):
        print('esiste gia')
        return render_template('create_account.html', alert='Account già esistente!')
    else:
        pswH = generate_password_hash(psw, method='pbkdf2:sha256')
        aggiungiInDB(username, pswH)
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Scadenza tra 1 ora
        }
        token = jwt.encode(payload, chiave_segreta, algorithm='HS256')
        risposta = redirect(url_for('home'))
        risposta.set_cookie('token', token, max_age=60*60*24, httponly=True, samesite='Strict')
        return risposta

@app.route("/", methods=["GET"])
def index():
    token=request.cookies.get('token')

    try:
    # Decodifica del token
        decoded = jwt.decode(token, chiave_segreta, algorithms=['HS256'])
        print(f'Token decodificato: {decoded}')
        
        return redirect(url_for('home'))
    except jwt.ExpiredSignatureError:
        print("Il token è scaduto.")
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        print("Token non valido.")
        return redirect(url_for('login'))


@app.route("/home", methods=["GET"])
def home():
    token=request.cookies.get('token')
    
    try:
    # Decodifica del token
        decoded = jwt.decode(token, chiave_segreta, algorithms=['HS256'])
        username=decoded['username']
        print(f'Token decodificato: {username}')
        return render_template('home.html',username=username)
    except jwt.ExpiredSignatureError:
        print("Il token è scaduto.")
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        print("Token non valido.")
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='POST':
        username=request.form['e-mail']
        password=request.form['password']
        print(username, password)
        return validate(username,password)
    return render_template('login.html')

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method=='POST':
        username=request.form.get('e-mail')
        password=request.form.get('password')
        return createAccount(username,password)
    return render_template('create_account.html')

@app.route("/logout")
def logout():
    risposta=redirect(url_for('login'))
    risposta.set_cookie('token', '', expires=0, httponly=True, samesite='Strict')
    return risposta

def creaDB():
    conn = sqlite3.connect(nomeDB)
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT) ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    creaDB()
    app.run(debug=True, host="0.0.0.0", port=4444)