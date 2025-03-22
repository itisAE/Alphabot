import socket
import time
from pynput.keyboard import Listener
from threading import Thread

host = '192.168.1.118'
port = 22343
buffer_size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

valAcc = {'w': 0, 'a': 1, 's': 2, 'd': 3}
key_states = {key: False for key in valAcc}  # Stato attuale dei tasti (premuto/rilasciato)



def letturaTasti():
    
    if key_states["w"] and key_states["a"]:  # Avanti + Sinistra
        return 'q'
    elif key_states["w"] and key_states["d"]:  # Avanti + Destra
        return 'e'
    elif key_states["s"] and key_states["a"]:  # Indietro + Sinistra
        return 'z'
    elif key_states["s"] and key_states["d"]:  # Indietro + Destra
        return 'x'
    elif key_states["w"]:  # Solo Avanti
        return 'w'
    elif key_states["s"]:  # Solo Indietro
        return 's'
    elif key_states["a"]:  # Solo Sinistra
        return 'a'
    elif key_states["d"]:  
        return 'd'
    else:
        return 'stop'
        

def send_command(message):
    s.sendall(message.encode())
    data = s.recv(buffer_size)
    if data.decode() == "ok":
        print("Comando effettuato")
    else:
        print("Comando non valido, perciò non effettuato")

def on_press(key):
    try:
        if key.char in valAcc and not key_states[key.char]:
            key_states[key.char] = True  # Aggiorna lo stato del tasto a premuto
            movimento=letturaTasti()
            value = 55
            print('Si sta muovendo attualmente: '+movimento)
            message = f"{movimento},{value}"
            send_command(message)
        elif key.char == '1':
            value = 55
            message = f"pr,{value}"
            send_command(message)
        elif key.char == '2':
            value = 55
            message = f"se,{value}"
            send_command(message)
    except AttributeError:
        pass  # Ignora altri tasti

def on_release(key):
    try:
        if key.char in valAcc and key_states[key.char]:
            key_states[key.char] = False  # Aggiorna lo stato del tasto a rilasciato
            
            value = 0
            movimento=letturaTasti()
            print('Si sta muovendo attualmente: '+movimento)
            message = f"{movimento},{value}"
            send_command(message)
    except AttributeError:
        pass  # Ignora altri tasti

def ping_server():
    while True:
        time.sleep(5)  # Intervallo di ping (5 secondi)
        s.sendall(b"ping")
        data = s.recv(buffer_size)
        if data.decode() != "ok":
            print("Ping failed")
            break

# Avvia il thread per il ping
ping_thread = Thread(target=ping_server)
ping_thread.start()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

s.close()
