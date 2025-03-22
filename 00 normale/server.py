import socket
import AlphaBot

robot = AlphaBot.AlphaBot()
host = '0.0.0.0'
port = 22333
buffer_size = 4096

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
    print(f"Connessione avvenuta da {addr}")
    try:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            data = data.decode()
            comando(data)
            conn.sendall(b"ok")  # Risponde al client
    except ConnectionResetError:
        print("Connessione chiusa dal client")
    finally:
        robot.stop()  # Ferma il robot in caso di eccezioni
        conn.close()

