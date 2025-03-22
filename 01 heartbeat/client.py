import socket
import time
from pynput.keyboard import Listener
from threading import Thread

host = '192.168.1.142'
port = 22333
buffer_size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

valAcc = {'w': 0, 'a': 1, 's': 2, 'd': 3}
last_sent = ''
last_time = 0
debounce_delay = 0.2  # 200 ms debounce delay

def send_command(message):
    global last_sent, last_time
    current_time = time.time()
    if message != last_sent or (current_time - last_time) > debounce_delay:
        s.sendall(message.encode())
        last_sent = message
        last_time = current_time
        data = s.recv(buffer_size)
        if data.decode() == "ok":
            print("Command executed correctly")
        else:
            print("Command not valid")

def on_press(key):
    try:
        if key.char in valAcc:
            value = 55
            message = f"{valAcc[key.char]},{value}"
            send_command(message)
    except AttributeError:
        pass  # Ignora altri tasti

def on_release(key):
    try:
        if key.char in valAcc:
            value = 0
            message = f"{valAcc[key.char]},{value}"
            send_command(message)
    except AttributeError:
        pass  # Ignora altri tasti


def ping_server():
    while True:
        time.sleep(5)  # Intervallo di ping (5 secondi)
        try:
            s.sendall(b"ping")
            data = s.recv(buffer_size)
            if data.decode() != "ok":
                print("Ping failed")
                break
        except socket.error:
            print("Error while sending/receiving ping.")
            break


# Avvia il thread per il ping
ping_thread = Thread(target=ping_server, daemon=True)
ping_thread.start()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

s.close()
