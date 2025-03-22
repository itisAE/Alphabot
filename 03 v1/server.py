import socket
import AlphaBot

host = '192.168.1.142'
port = 22343
buffer_size = 4096
timeout_interval = 10  # Intervallo massimo di attesa tra ping

robot = AlphaBot.AlphaBot()
robot.stop()  # Ferma il robot all'inizio

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
        robot.setMotor(-80, 30)  # Sinistro più lento, destro più veloce
    elif mov == 'e':  # Avanti + Destra
        robot.setMotor(-50, 80)  # Sinistro più veloce, destro più lento
    elif mov == 'z':  # Indietro + Sinistra
        robot.setMotor(80, -30)  # Sinistro indietro più lento, destro più veloce
    elif mov == 'x':  # Indietro + Destra
        robot.setMotor(50, -80)  # Sinistro indietro più veloce, destro più lento
    elif mov == 'w':  # Solo Avanti
        # Prova a ridurre leggermente la potenza del motore destro
        robot.setMotor(-50, 48)
    elif mov == 's':  # Solo Indietro
        robot.setMotor(50, -50)
    elif mov == 'a':  # Solo Sinistra
        robot.setMotor(-50, 0)
    elif mov == 'd':  # Solo Destra
        robot.setMotor(0, 50)

    # print(f"Muovi motori: {mov}")  # Messaggio di debug
    # if mov == 'q':  # Avanti + Sinistra
    #     robot.setMotor(-80, 50)  # Sinistro più lento, destro più veloce
    # elif mov == 'e':  # Avanti + Destra
    #     robot.setMotor(-50, 80)  # Sinistro più veloce, destro più lento
    # elif mov == 'z':  # Indietro + Sinistra
    #     robot.setMotor(30, 50) # Sinistro indietro più lento, destro più veloce
    # elif mov == 'x':  # Indietro + Destra
    #     robot.setMotor(50, 30) # Sinistro indietro più veloce, destro più lento
    # elif mov == 'w':  # Solo Avanti
    #     robot.setMotor(-50, 50)
    #     # robot.forward()
    # elif mov == 's':  # Solo Indietro
    #     # robot.backward()
    #     robot.setMotor(50, -50)
    # elif mov == 'a':  # Solo Sinistra
    #     robot.setMotor(-50, 0)
    #     # robot.left()
    # elif mov == 'd':  # Solo Destra
        
    #     robot.setMotor(0, 50)
    #     # robot.right()

def comando(command):
    print(f"Comando ricevuto: {command}")  # Messaggio di debug
    dati = command.split(",")
    movimento = dati[0]
    #valore = int(dati[1])

    # Aggiungi il controllo per il comando di stop
    if movimento == 'stop':
        robot.stop()
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
            # print(f"Dati ricevuti: {data}")  # Messaggio di debug

            # Gestisci il messaggio di ping
            if data == "ping":
                conn.sendall(b"ok")
            else:
                comando(data)
                conn.sendall(b"ok")
    except (ConnectionResetError, socket.timeout) as e:
        print("Connessione persa o timeout scaduto:", e)
        robot.stop()  # Ferma il robot in caso di errore di connessione
    except Exception as e:
        print("Errore imprevisto:", e)
        robot.stop()
    finally:
        robot.stop()
        conn.close()  # Chiude la connessione
        print("Connessione chiusa e robot fermato.")