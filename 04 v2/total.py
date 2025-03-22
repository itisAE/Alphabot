from server import comando
from flask import Flask, render_template, request, redirect, url_for, make_response, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta


nomeDB='users.db'
chiave_segreta='tpsit2024|2025'

HTML_CONTENT = '''<!DOCTYPE html> <html lang="it"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Comandi Alphabot</title> <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet"> <style> .btn-custom { background-color: #d3d3d3; border: none; color: #333; } .btn-custom img { width: 40px; height: auto; } .btn-custom:hover { background-color: #c0c0c0; } .btn-active { background-color: #333333a2; } #joystick-container { width: 100%; height: 300px; position: relative; } </style> </head> <body> <div class="container"> <h1 class="text-center my-4">Comandi Alphabot</h1> <div id="joystick-container" class="position-relative" style="height: 300px;"> </div> <div class="text-center mt-4"> <p id="angle-degree">Prima marcia</p> </div> <div class="d-flex justify-content-center mt-4"> <form id="command-form"> <button id="m1" class="btn btn-custom mx-2 btn-active" type="button" value="m1"> <img src="{{ url_for('static', filename='img/turtle.png') }}" alt="Marcia 1"> </button> <button id="m2" class="btn btn-custom mx-2" type="button" value="m2"> <img src="{{ url_for('static', filename='img/hare.png') }}" alt="Marcia 2"> </button> </form> </div> </div> <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script> <script src="{{ url_for('static', filename='js/nipplejs.min.js') }}"></script> <script> var previousDirection = 'stop'; var joystick = nipplejs.create({ zone: document.getElementById('joystick-container'), mode: 'static', position: { left: '50%', top: '50%' }, color: 'blue', size: 200, }); joystick.on('move', function(evt, data) { if (data.angle) { var angleDegree = data.angle.degree; console.log("Angolo in gradi:", angleDegree); var direzione = 'stop'; if (angleDegree < 30 || angleDegree > 330) { direzione = 'd'; } else if (angleDegree <= 60 && angleDegree >= 30) { direzione = 'e'; } else if (angleDegree <= 330 && angleDegree >= 300) { direzione = 'x'; } else if (angleDegree < 120 && angleDegree > 60) { direzione = 'w'; } else if (angleDegree < 300 && angleDegree > 240) { direzione = 's'; } else if (angleDegree < 210 && angleDegree > 150) { direzione = 'a'; } else if (angleDegree <= 150 && angleDegree >= 120) { direzione = 'q'; } else if (angleDegree <= 240 && angleDegree >= 210) { direzione = 'z'; } if (direzione !== previousDirection) { previousDirection = direzione; document.getElementById('angle-degree').textContent = 'Direzione: ' + direzione; sendCommand(direzione); } } }); joystick.on('end', function(evt, data) { console.log("Joystick rilasciato."); document.getElementById('angle-degree').textContent = 'Direzione: stop'; if (previousDirection !== 'stop') { previousDirection = 'stop'; sendCommand('stop'); } }); document.getElementById('m1').addEventListener('click', function() { console.log("Prima marcia"); document.getElementById('angle-degree').textContent = 'Prima marcia'; this.classList.add('btn-active'); document.getElementById('m2').classList.remove('btn-active'); sendCommand('m1'); }); document.getElementById('m2').addEventListener('click', function() { console.log("Seconda marcia"); document.getElementById('angle-degree').textContent = 'Seconda marcia'; this.classList.add('btn-active'); document.getElementById('m1').classList.remove('btn-active'); sendCommand('m2'); }); function sendCommand(command) { var xhr = new XMLHttpRequest(); xhr.open("POST", "/", true); xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); xhr.onreadystatechange = function() { if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) { console.log("Command sent: " + command); } }; xhr.send("marcia=" + command); } </script> </body> </html>
'''


app = Flask(__name__)

# Configura le cartelle per i file statici
app.static_folder = 'static'

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


@app.route("/home", methods=["GET", "POST"])
def home():
    token=request.cookies.get('token')
    
    try:
    # Decodifica del token
        decoded = jwt.decode(token, chiave_segreta, algorithms=['HS256'])
        username=decoded['username']
        print(f'Token decodificato: {username}')
        # return render_template('home.html',username=username)
    
        if request.method == 'POST':
           
            cmd = request.form.get('marcia') 
            
            print('total: '+cmd)
            comando(cmd)
            #mettere comando

        elif request.method == 'GET': 
            return render_template('controllo.html') 
        return render_template('controllo.html') 


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