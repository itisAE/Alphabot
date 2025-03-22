from pynput import keyboard
import time

valAcc = {'w': 0, 'a': 1, 's': 2, 'd': 3}
key_states = {key: False for key in valAcc}  # Stato iniziale di tutti i tasti è False

# Set per tenere traccia dei tasti premuti
tasti_premuti = set()

# Funzione che viene chiamata quando un tasto viene premuto
def on_press(key):
    try:
        # Se il tasto è nella lista dei tasti gestiti (valAcc) e non è già stato registrato come premuto
        if key.char in valAcc and not key_states[key.char]:
            key_states[key.char] = True  # Imposta lo stato del tasto a True (premuto)
            tasti_premuti.add(key.char)  # Aggiungi il tasto al set
            print(f"Tasto premuto: {key.char}")
    except AttributeError:
        pass  # Ignora i tasti speciali come Shift, Ctrl, etc.


# Funzione che viene chiamata quando un tasto viene rilasciato
def on_release(key):
    try:
        # Se il tasto è nella lista dei tasti gestiti e il suo stato è True (è stato premuto)
        if key.char in valAcc and key_states[key.char]:
            key_states[key.char] = False  # Imposta lo stato del tasto a False (rilasciato)
            tasti_premuti.discard(key.char)  # Rimuovi il tasto dal set
            print(f"Tasto rilasciato: {key.char}")
    except AttributeError:
        pass  # Ignora i tasti speciali

# Funzione per ottenere la lista dei tasti attualmente premuti
def leggi_tasti_premuti():
    return ''.join(sorted(tasti_premuti))  # Restituisce una stringa ordinata dei tasti premuti

# Avvia il listener dei tasti
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Esegui il listener in un thread separato
from threading import Thread
listener_thread = Thread(target=start_listener)
listener_thread.daemon = True
listener_thread.start()

# Controllo periodico (esempio ogni 0.5 secondi)
while True:
    tasti = leggi_tasti_premuti()
    print(f"Tasti attualmente premuti: {tasti}")
    time.sleep(0.5)
    print(f"Tasti registrati (key_states): {key_states}")
