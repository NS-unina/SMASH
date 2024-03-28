from topology import NetworkTopology
from network import Host, Honeypot
from utils import Utils as u

t = NetworkTopology()
class HoneypotManager:
    #PATTERN SINGLETON
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HoneypotManager, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance
    def __init__(self):
        # indexes
        self.COWRIE_INDEX = 0
        self.HERALDING_INDEX = 1
        self.HERALDING1_INDEX = 1
        self.HERALDING2_INDEX = 2

        self.SSH_INDEX = 0
        self.TELNET_INDEX= 1
        self.FTP_INDEX = 2
        self.SOCKS5_INDEX = 3

        # Dizionari per gli indici
        self.index_honeypot = {
            "cowrie1": 0,
            "heralding": 1,
            "heralding1": 1,
            "heralding2": 2,

        }

        self.service_index = {
            "SSH_INDEX": 0,
            "TELNET_INDEX": 1,
            "FTP_INDEX": 2,
            "SOCKS5_INDEX": 3,
        }

        self.index_host = {
            "ti_host1": 0,
        }

        # Lista di host
        self.hosts = [t.ti_host1]
        # Lista di honeypots
        self.honeypots = [t.cowrie1, t.heralding1, t.heralding2]

        # Vettore per il mapping degli honeypot sui host
        self.h_h1 = [1, 1, 1]

        self.h = [self.h_h1]

        # Lista di servizi
        self.services = ["ssh", "telnet", "ftp", "socks5"]

        # Mappa dei servizi per ogni honeypot
        self.s_hp1 = [1, 1, 0, 0]
        self.s_hp2 = [1, 0, 1, 1]
        self.s_hp3 = [1, 0, 1, 1]

        self.sm = [self.s_hp1, self.s_hp2, self.s_hp3]

        # Porte per ogni servizio su ogni honeypot
        self.ports_hp1 = [22, 23, 0, 0]
        self.ports_hp2 = [2022, 0, 2021, 2080]
        self.ports_hp3 = [3022, 0, 3021, 3080]
        self.ports = [self.ports_hp1, self.ports_hp2, self.ports_hp3]

        # Porte esposte per ogni host
        self.ports_host1 = [22, 23, 2022, 2021, 2080, 3022, 3021, 3080]

        self.sdh1 = []
        for row in self.h:
            self.sdh1.append(u.product_vector_matrix(row, self.sm))

        self.sdh = [sum(elements) for elements in zip(*self.sdh1)]
    
        # Service busy: 1 if it is busy, else 0
        self.sb = [[0, 0, 0, 0], [0, 0, 0, 0],[0, 0, 0, 0]]

    def add_new_honeypot_ti_management(self, new_honeypot, host, s_h, ports_h):
        # Aggiunta dell'oggetto Honeypot alla lista honeypots
        self.honeypots.append(new_honeypot)
        # AGGIUNTA NUOVO INDICE
        # Trova l'ultimo valore indice è anche il massimo
        last_index = max(self.index_honeypot.values())
        self.index_honeypot[new_honeypot.get_name()] = last_index + 1
        # Aggiunta alla lista h
        index = self.index_host.get(host.get_name(),None)
        for row in self.h:
            if self.h.index(row) == index:
                row.append(1)
            else:
                row.append(0)
   
        #aggiunge service map dell'honeypot a matrice SM
        self.sm.append(s_h)

        # Aggiunta nuove porte a lista ports
        self.ports.append(ports_h)

        # Ricalcolo SDH
        self.sdh1 = []
        for row in self.h:
            self.sdh1.append(u.product_vector_matrix(row, self.sm))

        self.sdh = [sum(elements) for elements in zip(*self.sdh1)]
        # Aggiunta in sb
        busy_service = [0, 0, 0, 0]
        self.sb.append(busy_service)

    def add_new_host_ti_management(self,host):
        # AGGIUNTA DI UN NUOVO HOST
        self.hosts.append(host)
        num_honeypots = len(self.honeypots)
        self.h_h3  = [0] * num_honeypots
        self.h.append(self.h_h3)

        new_value = max(self.index_host.values()) + 1
        self.index_host[host.get_name()] = new_value

