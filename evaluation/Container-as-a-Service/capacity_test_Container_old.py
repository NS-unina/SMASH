import time
import requests
import psutil
import logging
from datetime import datetime

# Configurazione del logging
logging.basicConfig(filename='monitoring.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# URL della richiesta POST
url = "http://localhost:8080/handle_post"

# Intervallo di tempo tra le richieste (in secondi)
interval = 20

# Soglia di utilizzo della RAM per interrompere lo script
ram_threshold = 90

# Inizializzazione dei contatori per il parametro name, IP e MAC
name_counter = 1

# Inizializzazione del contatore per il numero di richieste POST
post_counter = 0


port_used = []

def find_free_port(port_used):
    for port in range(6000, 6999):
        if port not in port_used:
            port_used.append(port)
            return port
    return None


# Apertura dei file per salvare i dati
response_time_file = open('response_times.csv', 'w')
cpu_usage_file = open('cpu_usage.csv', 'w')
ram_usage_file = open('ram_usage.csv', 'w')

# Scrittura delle intestazioni dei file
response_time_file.write('VM_Number,ResponseTime\n')
cpu_usage_file.write('VM_Number,CPUUsage\n')
ram_usage_file.write('VM_Number,RAMUsage\n')

def get_system_metrics():
    """Raccoglie i dati di utilizzo della CPU e della RAM."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

def make_post_request(url, data):
    """Effettua una richiesta POST e restituisce il tempo di risposta."""
    start_time = time.time()
    print(url, data)
    response = requests.post(url, data=data)
    print(response)
    response_time = time.time() - start_time
    return response, response_time



try:
    cpu_usage, ram_usage = get_system_metrics()
    response_time_file.write(f"{post_counter},{0:.2f}\n")
    cpu_usage_file.write(f"{post_counter},{cpu_usage}\n")
    ram_usage_file.write(f"{post_counter},{ram_usage}\n")
    # Log dei risultati
    logging.info(f"{post_counter} VM, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%")
    while True:
        # Genera i parametri per la richiesta
        name = f"evaluation{name_counter}"
        ssh_port = find_free_port(port_used)
        ftp_port = find_free_port(port_used)
        socks_port = find_free_port(port_used)
        data = {
            "name": name,
            "ssh_port": ssh_port,
            "ftp_port": ftp_port,
            "socks_port": socks_port
        }

        # Effettua la richiesta POST
        response, response_time = make_post_request(url, data)

        # Raccoglie i dati di utilizzo della CPU e della RAM
        cpu_usage, ram_usage = get_system_metrics()

        post_counter += 1
        # Log dei risultati
        logging.info(f"{post_counter} Containers, Name: {name}, Response Time: {response_time:.2f}s, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%")

        # Salva i dati nei file
        
        response_time_file.write(f"{post_counter},{response_time:.2f}\n")
        cpu_usage_file.write(f"{post_counter},{cpu_usage}\n")
        ram_usage_file.write(f"{post_counter},{ram_usage}\n")

        # Controlla l'utilizzo della RAM e interrompe lo script se supera la soglia
        if ram_usage >= ram_threshold:
            logging.warning(f"RAM usage has reached {ram_usage}%. Stopping the script.")
            break

        # Controlla se la risposta è 200 OK
        if response.status_code == 200:
            # Incrementa i contatori
            name_counter += 1
            # Aspetta l'intervallo di tempo prima di fare la prossima richiesta
            time.sleep(interval)
        else:
            logging.error(f"Received status code {response.status_code}. Retrying...")
            # Attende un po' prima di riprovare in caso di errore
            time.sleep(5)
except Exception as e:
    logging.error(f"An error occurred: {e}")
    # Aspetta un po' prima di riprovare in caso di eccezione
    time.sleep(5)
finally:
    # Chiude i file alla fine dello script (o nel caso di un'interruzione)
    response_time_file.close()
    cpu_usage_file.close()
    ram_usage_file.close()
