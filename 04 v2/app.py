from flask import Flask, render_template_string, request


app = Flask(__name__)

# Configura le cartelle per i file statici
app.static_folder = 'static'

HTML_CONTENT = '''<!DOCTYPE html> <html lang="it"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Comandi Alphabot</title> <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet"> <style> .btn-custom { background-color: #d3d3d3; border: none; color: #333; } .btn-custom img { width: 40px; height: auto; } .btn-custom:hover { background-color: #c0c0c0; } .btn-active { background-color: #333333a2; } #joystick-container { width: 100%; height: 300px; position: relative; } </style> </head> <body> <div class="container"> <h1 class="text-center my-4">Comandi Alphabot</h1> <div id="joystick-container" class="position-relative" style="height: 300px;"> </div> <div class="text-center mt-4"> <p id="angle-degree">Prima marcia</p> </div> <div class="d-flex justify-content-center mt-4"> <form id="command-form"> <button id="m1" class="btn btn-custom mx-2 btn-active" type="button" value="m1"> <img src="{{ url_for('static', filename='img/turtle.png') }}" alt="Marcia 1"> </button> <button id="m2" class="btn btn-custom mx-2" type="button" value="m2"> <img src="{{ url_for('static', filename='img/hare.png') }}" alt="Marcia 2"> </button> </form> </div> </div> <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script> <script src="{{ url_for('static', filename='js/nipplejs.min.js') }}"></script> <script> var previousDirection = 'stop'; var joystick = nipplejs.create({ zone: document.getElementById('joystick-container'), mode: 'static', position: { left: '50%', top: '50%' }, color: 'blue', size: 200, }); joystick.on('move', function(evt, data) { if (data.angle) { var angleDegree = data.angle.degree; console.log("Angolo in gradi:", angleDegree); var direzione = 'stop'; if (angleDegree < 30 || angleDegree > 330) { direzione = 'd'; } else if (angleDegree <= 60 && angleDegree >= 30) { direzione = 'e'; } else if (angleDegree <= 330 && angleDegree >= 300) { direzione = 'x'; } else if (angleDegree < 120 && angleDegree > 60) { direzione = 'w'; } else if (angleDegree < 300 && angleDegree > 240) { direzione = 's'; } else if (angleDegree < 210 && angleDegree > 150) { direzione = 'a'; } else if (angleDegree <= 150 && angleDegree >= 120) { direzione = 'q'; } else if (angleDegree <= 240 && angleDegree >= 210) { direzione = 'z'; } if (direzione !== previousDirection) { previousDirection = direzione; document.getElementById('angle-degree').textContent = 'Direzione: ' + direzione; sendCommand(direzione); } } }); joystick.on('end', function(evt, data) { console.log("Joystick rilasciato."); document.getElementById('angle-degree').textContent = 'Direzione: stop'; if (previousDirection !== 'stop') { previousDirection = 'stop'; sendCommand('stop'); } }); document.getElementById('m1').addEventListener('click', function() { console.log("Prima marcia"); document.getElementById('angle-degree').textContent = 'Prima marcia'; this.classList.add('btn-active'); document.getElementById('m2').classList.remove('btn-active'); sendCommand('m1'); }); document.getElementById('m2').addEventListener('click', function() { console.log("Seconda marcia"); document.getElementById('angle-degree').textContent = 'Seconda marcia'; this.classList.add('btn-active'); document.getElementById('m1').classList.remove('btn-active'); sendCommand('m2'); }); function sendCommand(command) { var xhr = new XMLHttpRequest(); xhr.open("POST", "/", true); xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); xhr.onreadystatechange = function() { if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) { console.log("Command sent: " + command); } }; xhr.send("marcia=" + command); } </script> </body> </html>
'''

@app.route('/', methods=['GET', 'POST']) 
def home(): 
  if request.method == 'POST':
    marcia = request.form.get('marcia') 
    if marcia == 'm1': print("1") 
    elif marcia == 'm2': print("2") 
    elif marcia == 'stop': print("stop") 
    else: print(marcia) 
  elif request.method == 'GET': 
    return render_template_string(HTML_CONTENT) 
  return render_template_string(HTML_CONTENT) 

if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=5000, debug=True)
