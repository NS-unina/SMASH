import time
import requests
import psutil
import logging
import argparse
import os
from datetime import datetime



def get_system_metrics():
    """Raccoglie i dati di utilizzo della CPU e della RAM."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

def increment_ip(base_ip, counter):
    """Incrementa l'ultima parte dell'indirizzo IP."""
    parts = base_ip.split('.')
    parts[-1] = str(counter)
    return '.'.join(parts)

def increment_mac(base_mac, counter):
    """Incrementa l'ultima parte dell'indirizzo MAC."""
    mac_int = int(base_mac, 16) + counter
    return '{:012x}'.format(mac_int)

def make_post_request(url, data):
    """Effettua una richiesta POST e restituisce il tempo di risposta."""
    start_time = time.time()
    print(url, data)
    response = requests.post(url, data=data)
    print(response)
    response_time = time.time() - start_time
    return response, response_time

def main(reps):
    # Configurazione del logging
    directory_log = "log_1024"
    if not os.path.exists(directory_log):
        os.makedirs(directory_log)

    log_path = os.path.join(directory_log, f'monitoring_{reps}.log')
    
    logging.basicConfig(filename=log_path, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # URL della richiesta POST
    url = "http://localhost:8080/handle_post"

    # Intervallo di tempo tra le richieste (in secondi)
    interval = 20

    # Soglia di utilizzo della RAM per interrompere lo script
    ram_threshold = 90

    # Inizializzazione dei contatori per il parametro name, IP e MAC
    name_counter = 1
    ip_counter = 50
    mac_counter = 2

    # Inizializzazione del contatore per il numero di richieste POST
    post_counter = 0

    # Apertura dei file per salvare i dati
    # Nome della cartella dove salvare i file
    directory_response_time = "response_time_1024"
    directory_cpu_usage = "cpu_usage_1024"
    directory_ram_usage = "ram_usage_1024"
    
    # Crea la cartella se non esiste
    if not os.path.exists(directory_response_time):
        os.makedirs(directory_response_time)
    if not os.path.exists(directory_cpu_usage):
        os.makedirs(directory_cpu_usage)
    if not os.path.exists(directory_ram_usage):
        os.makedirs(directory_ram_usage)

    response_time_file_path = os.path.join(directory_response_time, f'response_times_{reps}.csv')
    cpu_usage_file_path = os.path.join(directory_cpu_usage, f'cpu_usage_{reps}.csv')
    ram_usage_file_path = os.path.join(directory_ram_usage, f'ram_usage_{reps}.csv')

    response_time_file = open(response_time_file_path, 'w')
    cpu_usage_file = open(cpu_usage_file_path, 'w')
    ram_usage_file = open(ram_usage_file_path, 'w')

    # Scrittura delle intestazioni dei file
    response_time_file.write('VM_Number,ResponseTime\n')
    cpu_usage_file.write('VM_Number,CPUUsage\n')
    ram_usage_file.write('VM_Number,RAMUsage\n')

    try:
        print("Ripetizione: ",reps)
        cpu_usage, ram_usage = get_system_metrics()
        response_time_file.write(f"{post_counter},{0:.2f}\n")
        cpu_usage_file.write(f"{post_counter},{cpu_usage}\n")
        ram_usage_file.write(f"{post_counter},{ram_usage}\n")
        # Log dei risultati
        logging.info(f"{post_counter} VM, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%")
        while True:
            # Genera i parametri per la richiesta
            name = f"evaluation{name_counter}"
            ip = increment_ip("10.1.4.1", ip_counter)
            mac = increment_mac("0800276dedd8", mac_counter)
            
            data = {
                "name": name,
                "subnet": "10.1.4.0/24",
                "ip": ip,
                "mac": mac
            }

            # Effettua la richiesta POST
            response, response_time = make_post_request(url, data)

            # Raccoglie i dati di utilizzo della CPU e della RAM
            cpu_usage, ram_usage = get_system_metrics()

            post_counter += 1
            # Log dei risultati
            logging.info(f"{post_counter} VM, Name: {name}, IP: {ip}, MAC: {mac}, Response Time: {response_time:.2f}s, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%")

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
                ip_counter += 1
                mac_counter += 1
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluation.')
    parser.add_argument('reps', type=str, help='Number of Repetition.')

    args = parser.parse_args()
    main(args.reps)
