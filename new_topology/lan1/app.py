from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

# 172.28.0.2 172.28.0.3
#ip_address_container = [2,3]

@app.route('/handle_post', methods=['POST'])
def handle_post():
    # Esegui lo script Bash quando viene ricevuta una richiesta POST
    subnet = "10.1.4.0/24"
    mac = "0800276dedc2"
    name="cowrie7"
    ip_address = "10.1.4.60"
    ssh_port = "3426"

    #name = request.form.get('name')
    #ip = find_free_address(ip_address_container, 20)
    #print("IP interno:", ip)
    #ssh_port = request.form.get('ssh_port')
    # Ottieni il percorso assoluto della cartella corrente
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Costruisci il percorso completo dello script
    script_path = os.path.join(current_directory, 'script.sh')
    
    # Lista di parametri da passare allo script
    parameters = [subnet, mac,name, ip_address, ssh_port]
    
    # Esegui lo script Bash quando viene ricevuta una richiesta POST
    result=subprocess.check_output([script_path] + parameters, text=True)
    print(result)
    #subprocess.call(script_path)
    return "Script eseguito con successo", 200

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