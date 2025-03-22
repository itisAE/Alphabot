import socket


host = 'localhost'
port = 22343
buffer_size = 4096
timeout_interval = 10  # Intervallo massimo di attesa tra ping

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server avviato su {host}:{port}")
except Exception as e:
    print(f"Errore durante l'avvio del server: {e}")
    exit(1)

caratteri = ['w', 'a', 's', 'd', 'q', 'e', 'z', 'x']

def muoviMotori(mov):
    print(f"Muovi motori: {mov}")  # Messaggio di debug
    if mov == 'q':  # Avanti + Sinistra
        print('robot.setMotor(-25, -50)')  # Sinistro più lento, destro più veloce
    elif mov == 'e':  # Avanti + Destra
        print('robot.setMotor(-50, -25)')  # Sinistro più veloce, destro più lento
    elif mov == 'z':  # Indietro + Sinistra
        print('robot.setMotor(25, 50)')  # Sinistro indietro più lento, destro più veloce
    elif mov == 'x':  # Indietro + Destra
        print('robot.setMotor(50, 25)')  # Sinistro indietro più veloce, destro più lento
    elif mov == 'w':  # Solo Avanti
        print('robot.forward()')
    elif mov == 's':  # Solo Indietro
        print('robot.backward()')
    elif mov == 'a':  # Solo Sinistra
        print('robot.left()')
    elif mov == 'd':  # Solo Destra
        print('robot.right()')

def comando(command):
    print(f"Comando ricevuto: {command}")  # Messaggio di debug
    dati = command.split(",")
    movimento = dati[0]
    valore = int(dati[1])

    # Aggiungi il controllo per il comando di stop
    if movimento == 'stop':
        print('robot.stop()')
        return
    else:
        muoviMotori(movimento)

while True:
    print("In attesa di connessione...")
    conn, addr = s.accept()
    print(f"Connessione avvenuta da {addr}")
    conn.settimeout(timeout_interval)  # Imposta il timeout per la connessione

    try:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            data = data.decode()
            print(f"Dati ricevuti: {data}")  # Messaggio di debug

            # Gestisci il messaggio di ping
            if data == "ping":
                conn.sendall(b"ok")
            else:
                comando(data)
                conn.sendall(b"ok")
    except (ConnectionResetError, socket.timeout) as e:
        print("Connessione persa o timeout scaduto:", e)
        #robot.stop()  # Ferma il robot in caso di errore di connessione
    except Exception as e:
        print("Errore imprevisto:", e)
        #robot.stop()
    finally:
        conn.close()  # Chiude la connessione
        print("Connessione chiusa e robot fermato.")