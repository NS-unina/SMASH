from topology import NetworkTopology
import requests
import aiohttp
import mapping as map
from ti_management import HoneypotManager

from network import Honeypot, Host

man = HoneypotManager()
t = NetworkTopology()

index_to_decoy_mapping = {
    0: t.cowrie1,
    1: t.cowrie2,
    2: t.heralding1,
    3: t.heralding2,
    4: t.heralding3,
    5: t.heralding4,
}

def add_new_host(name, subnet, mac,ip_address): 
    url = 'http://10.1.3.1:8080/handle_post'  # URL host
    # Dati da inviare nel corpo della richiesta
    payload = {'name':name, 'subnet': subnet,  'mac':mac,'ip':ip_address }  
    subnet1 = t.subnet1

    #INVIO EVENTO A HOST PER DEPLOYARE UN NUOVO HOST
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("200 OK, HOST creato con successo")
         # Analizza la risposta JSON
        json_response = response.json()
    
        # recupero l'ovs_port
        ovs_port = json_response['ovs_port']

        print("La ovs port: ", ovs_port)
    else:
        print("Si è verificato un errore durante l'invio della richiesta:", response.status_code)
        print("Messaggio di errore:", response.text)
    
    # Crea un nuovo oggetto Honeypot
    netmask= "255.255.255.0"    
    new_host = Host(name, ip_address, mac, int(ovs_port), netmask,subnet1)
    # Lo aggiunge alla lista di tutti gli honeypot attivi
    t.hosts_list.append(new_host)


    man.add_new_host_ti_management(new_host)


    return new_host


def add_new_honeypot(name,host,s_hp,ports_hp): 
    url = 'http://' + host.get_ip_addr() + ':8080/handle_post'  # URL host
    # Dati da inviare nel corpo della richiesta
    payload = {'name': name, 'ssh_port': ports_hp[man.SSH_INDEX], 'ftp_port': ports_hp[man.FTP_INDEX], 'socks_port': ports_hp[man.SOCKS5_INDEX]}  

    #INVIO EVENTO A HOST PER DEPLOYARE UN NUOVO HOST
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("200 OK, Honeypot creato con successo")
    else:
        print("Si è verificato un errore durante l'invio della richiesta:", response.status_code)
        print("Messaggio di errore:", response.text)
    
    # Crea un nuovo oggetto Honeypot
    new_honeypot = Honeypot(name, host.get_ip_addr(), host.get_MAC_addr(), host.get_ovs_port(), host.get_netmask(), host.get_subnet())
    # Lo aggiunge alla lista di tutti gli honeypot attivi
    t.honeypots_list.append(new_honeypot)

    # Aggiorna dizionario decoy_mapping aggiungendo una nuova entry con chiave il nome dell'honeypot e valore l'ultimo honeypot nella lista
    map.decoy_mapping[new_honeypot.get_name()] = t.honeypots_list[-1]


    # Aggiorna dizionario index_mapping aggiungendo una nuova entry con chiave il valore massimo delle chiavi +1 e valore l'ultimo honeypot nella lista
    new_key = max(index_to_decoy_mapping.keys()) + 1
    index_to_decoy_mapping[new_key] = t.honeypots_list[-1]

    man.add_new_honeypot_ti_management(new_honeypot,host,s_hp,ports_hp)

    return new_honeypot


def find_free_port(ports_list, start_port):
    # Itera attraverso le porte nella lista a partire dalla porta specificata
    for port in range(start_port, 5000):
        # Se la porta non è presente nella lista delle porte utilizzate, restituiscila
        if port not in ports_list:
            return port
    # Se non viene trovata nessuna porta libera
    return None

