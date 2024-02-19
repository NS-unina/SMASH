import topology as t
import requests
import mapping as map
from ti_management import HoneypotManager

from network import Honeypot, Host

man = HoneypotManager()

index_to_decoy_mapping = {
    0: t.cowrie,
    1: t.heralding1,
    2: t.heralding2,
    3: t.heralding3,
    4: t.heralding4,
}

def add_new_honeypot(name,host,s_hp,ports_hp): 
    url = 'http://' + host.get_ip_addr() + ':8080/handle_post'  # URL host
    # Dati da inviare nel corpo della richiesta
    payload = {'name': name, 'ssh_port': ports_hp[man.SSH_INDEX], 'ftp_port': ports_hp[man.FTP_INDEX], 'socks_port': ports_hp[man.SOCKS5_INDEX]}  

    #INVIO EVENTO A HOST PER DEPLOYARE UN NUOVO HOST
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("Richiesta POST inviata con successo!")
    else:
        print("Si è verificato un errore durante l'invio della richiesta:", response.status_code)
        print("Messaggio di errore:", response.text)
    
    # Crea un nuovo oggetto Honeypot
    new_honeypot = Honeypot(name, host.get_ip_addr(), host.get_MAC_addr(), host.get_ovs_port(), host.get_netmask())
    # Lo aggiunge alla lista di tutti gli honeypot attivi
    t.honeypots_list.append(new_honeypot)

    # Aggiorna dizionario decoy_mapping aggiungendo una nuova entry con chiave il nome dell'honeypot e valore l'ultimo honeypot nella lista
    map.decoy_mapping[new_honeypot.get_name] = t.honeypots_list[-1]


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

