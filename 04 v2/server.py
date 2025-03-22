import AlphaBot

marcia = 1  # marcia dell'alphabot

robot = AlphaBot.AlphaBot()
robot.stop()  # Ferma il robot all'inizio

def muoviMotori(mov):
    global marcia
    print(f"Muovi motori: {mov}")  # Messaggio di debug
    
    # Definiamo la velocità base in base alla marcia
    velocita_base = 50 * marcia
    velocita_ridotta = 30 * marcia
    
    if mov == 'q':  # Avanti + Sinistra
        robot.setMotor(-velocita_ridotta, velocita_base)  # Sinistro più lento, destro più veloce
    elif mov == 'e':  # Avanti + Destra
        robot.setMotor(-velocita_base, velocita_ridotta)  # Sinistro più veloce, destro più lento
    elif mov == 'z':  # Indietro + Sinistra
        robot.setMotor(velocita_ridotta, -velocita_base)  # Sinistro indietro più lento, destro più veloce
    elif mov == 'x':  # Indietro + Destra
        robot.setMotor(velocita_base, -velocita_ridotta)  # Sinistro indietro più veloce, destro più lento
    elif mov == 'w':  # Solo Avanti
        # Bilanciamo leggermente i motori per garantire un movimento dritto
        robot.setMotor(-velocita_base, velocita_base)
    elif mov == 's':  # Solo Indietro
        robot.setMotor(velocita_base, -velocita_base)
    elif mov == 'a':  # Solo Sinistra (ruota sul posto)
        robot.setMotor(-velocita_base, -velocita_base)
    elif mov == 'd':  # Solo Destra (ruota sul posto)
        robot.setMotor(velocita_base, velocita_base)

def comando(command):
    global marcia
    print(f"Comando ricevuto: {command}")  # Messaggio di debug
    movimento = command
    
    # Controllo comandi speciali
    if movimento == 'stop':
        robot.stop()
        return
    elif movimento == 'm1':  # Corretto per allinearsi con l'interfaccia HTML
        marcia = 1
        print(f"Marcia impostata a: {marcia}")
        return
    elif movimento == 'm2':  # Corretto per allinearsi con l'interfaccia HTML
        marcia = 2
        print(f"Marcia impostata a: {marcia}")
        return
    else:
        muoviMotori(movimento)