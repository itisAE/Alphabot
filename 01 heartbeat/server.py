import socket
import AlphaBot

robot = AlphaBot.AlphaBot()
host = '192.168.1.142'
port = 22333
buffer_size = 4096
timeout_interval = 7 #tempo di timeout. se superato chiude la connessione

robot.stop()  # Ferma il robot all'inizio

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

def comando(command):
    dati = command.split(",")
    movimento = int(dati[0])
    valore = int(dati[1])
    if movimento in range(0, 4):
        if valore > 0:
            if movimento == 0:  # Avanti
                robot.forward()
            elif movimento == 1:  # Sinistra
                robot.left()
            elif movimento == 2:  # Indietro
                robot.backward()
            elif movimento == 3:  # Destra
                robot.right()
        else:
            robot.stop()

while True:
    print("In attesa di connessione...")
    conn, addr = s.accept()
    conn.settimeout(timeout_interval)  # Imposta il timeout per la connessione
    print(f"Connessione avvenuta da {addr}")
    try:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            data = data.decode()
            
            if data == "ping": #gestisco il ping
                conn.sendall(b"ok")
            else:
                comando(data)
                conn.sendall(b"ok")
    except (ConnectionResetError, socket.timeout) as e:
        print("Connessione persa o timeout scaduto:", e)
        robot.stop()  # Ferma il robot in caso di errore di connessione
    finally:
        conn.close()  # Chiude la connessione
        print("Connessione chiusa e robot fermato.")
