from flask import Flask, request, jsonify
import os
import subprocess
import random
import sys
import signal

app = Flask(__name__)

# 172.28.0.2 172.28.0.3
#ip_address_container = [2,3]

# Costruisci il percorso del file basato sulla directory corrente
file_name = "Vagrantfile"
file_path = os.path.join(os.getcwd(), 'vagrant', 'ubuntu',file_name)

# Leggi il contenuto iniziale del file YAML
with open(file_path, 'r') as f:
    initial_config = f.read()

# Definisci la funzione da eseguire al momento dell'arresto del server
def cleanup():
    # Scrivi il contenuto iniziale nel file YAML per ripristinarlo
    with open(file_path, 'w') as f:
        f.write(initial_config)

# Collega la funzione di cleanup al segnale di interruzione (CTRL+C)
def signal_handler(sig, frame):
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


occupied_port = [3200,3201,3202,3203,3204,3205,3206,3207,3208,3209,3210,3211,3212,3213]

@app.route('/handle_post', methods=['POST'])
def handle_post():
    # Esegui lo script Bash quando viene ricevuta una richiesta POST
    name = request.form.get('name')
    subnet = request.form.get('subnet')
    mac = request.form.get('mac')
    mac_formatted = mac.replace(":", "")
    ip_address = request.form.get('ip')
    # Genera un numero casuale tra 3200 e 4000
    ssh_port = random.randint(3200, 4000)

    # Controlla se il numero casuale generato è presente nella lista occupied_port
    while ssh_port in occupied_port:
        ssh_port = random.randint(3200, 4000)

    occupied_port.append(ssh_port)

    
    #ip = find_free_address(ip_address_container, 20)
    #print("IP interno:", ip)
    #ssh_port = request.form.get('ssh_port')
    # Ottieni il percorso assoluto della cartella corrente
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Costruisci il percorso completo dello script
    script_path = os.path.join(current_directory, 'script.sh')
    
    # Lista di parametri da passare allo script
    parameters = [subnet, mac_formatted,name, ip_address, str(ssh_port)]

    # Esegui lo script Bash in modo non bloccante
    process = subprocess.Popen([script_path] + parameters, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Attendi il completamento del processo e acquisisci l'output
    stdout, stderr = process.communicate()

    # Ottieni il risultato
    result = stdout.decode('utf-8')

    print("IL risultato è: ", result)
     # Costruisci la risposta JSON
    response_data = {
        "status": 200,  
        "message": "Script eseguito con successo",
        "ovs_port": result,
    }
    
    # Invia la risposta JSON
    return jsonify(response_data)


def find_free_address(address_list, start_address):
    # Itera attraverso le porte nella lista a partire dalla porta specificata
    for address in range(start_address, 253):
        # Se la porta non è presente nella lista delle porte utilizzate, restituiscila
        if address not in address_list:
            ip = "172.28.0." + str(address)
            #ip_address_container.append(address)
            return  ip
    # Se non viene trovata nessuna porta libera
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)