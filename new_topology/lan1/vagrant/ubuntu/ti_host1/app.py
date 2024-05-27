from flask import Flask, request
import os
import subprocess
import signal
import sys
import os

app = Flask(__name__)

# Ottieni la directory corrente
current_directory = os.getcwd()

# Costruisci il percorso del file basato sulla directory corrente
file_name = "docker-compose.yaml"
file_path = os.path.join(current_directory, 'docker', 'docker-build-capacity-test',file_name)

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


class Container:
    def __init__(self, name = None, ssh_port = None, ftp_port = None, socks_port = None):
        self.name = name
        self.ssh_port = ssh_port
        self.ftp_port = ftp_port
        self.socks_port = socks_port
        
    # GET METHODS
    def get_name(self):
        return self.name
    
    def get_ssh_port(self):
        return self.ssh_port
    def get_ftp_port(self):
        return self.ftp_port
    def get_socks_port(self):
        return self.socks_port

    # SET METHODS
    def set_name(self, name):
        self.name = name   
    def set_ssh_port(self, ssh_port):
        self.ssh_port = ssh_port
    def set_ftp_port(self, ftp_port):
        self.ftp_portp_port = ftp_port
    def set_socks_port(self, socks_port):
        self.socks_port = socks_port


# 172.28.0.2 172.28.0.3
ip_address_container = [2,3]
containers_name = []
containers = []


@app.route('/handle_post', methods=['POST'])
def handle_post():
    # Esegui lo script Bash quando viene ricevuta una richiesta POST

    name = request.form.get('name')
    ip = find_free_address(ip_address_container, 20)
    print("IP interno:", ip)
    ssh_port = request.form.get('ssh_port')
    ftp_port = request.form.get('ftp_port')
    socks_port = request.form.get('socks_port')
    # Ottieni il percorso assoluto della cartella corrente
    current_directory = os.path.dirname(os.path.abspath(__file__))
    new_container = Container(name,ssh_port,ftp_port,socks_port)
    # Costruisci il percorso completo dello script
    script_path = os.path.join(current_directory, 'docker', 'script.sh')
    
    if name not in containers_name:

        # Lista di parametri da passare allo script
        parameters = [name, ip, ssh_port, ftp_port,socks_port]
        # Esegui lo script Bash quando viene ricevuta una richiesta POST
        subprocess.call([script_path] + parameters)
        containers_name.append(name)
        containers.append(new_container)

        return "Script eseguito con successo", 200
    else:
        print("CONTAINER GIA PRESENTE")
        return "Script eseguito con successo", 200

def find_free_address(address_list, start_address):
    # Itera attraverso le porte nella lista a partire dalla porta specificata
    for address in range(start_address, 253):
        # Se la porta non è presente nella lista delle porte utilizzate, restituiscila
        if address not in address_list:
            ip = "172.28.0." + str(address)
            ip_address_container.append(address)
            return  ip
    # Se non viene trovata nessuna porta libera
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)