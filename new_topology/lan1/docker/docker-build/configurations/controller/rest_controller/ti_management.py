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
        self.HERALDING3_INDEX = 3
        self.HERALDING4_INDEX = 4

        self.SSH_INDEX = 0
        self.TELNET_INDEX= 1
        self.FTP_INDEX = 2
        self.SOCKS5_INDEX = 3

        # Dizionari per gli indici
        self.index_honeypot = {
            "cowrie1": 0,
            "cowrie2":1,
            "heralding": 2,
            "heralding1": 2,
            "heralding2": 3,
            "heralding3": 4,
            "heralding4": 5,
        }

        self.service_index = {
            "SSH_INDEX": 0,
            "TELNET_INDEX": 1,
            "FTP_INDEX": 2,
            "SOCKS5_INDEX": 3,
        }

        # Lista di host
        self.hosts = [t.ti_host1, t.ti_host2]
        # Lista di honeypots
        self.honeypots = [t.cowrie1, t.cowrie2, t.heralding1, t.heralding2, t.heralding3, t.heralding4]

        # Vettore per il mapping dei servizi sui host
        self.h_h1 = [1, 0, 1, 1, 0, 0]
        self.h_h2 = [0, 1, 0, 0, 1, 1]

        # Lista di servizi
        self.services = ["ssh", "telnet", "ftp", "socks5"]

        # Mappa dei servizi per ogni honeypot
        self.s_hp1 = [1, 1, 0, 0]
        self.s_hp2 = [1, 1, 0, 0]
        self.s_hp3 = [1, 0, 1, 1]
        self.s_hp4 = [1, 0, 1, 1]
        self.s_hp5 = [1, 0, 1, 1]
        self.s_hp6 = [1, 0, 1, 1]
        self.sm = [self.s_hp1, self.s_hp2, self.s_hp3, self.s_hp4, self.s_hp5,self.s_hp6]

        # Porte per ogni servizio su ogni honeypot
        self.ports_hp1 = [22, 23, 0, 0]
        self.ports_hp2 = [22, 23, 0, 0]
        self.ports_hp3 = [2022, 0, 2021, 2080]
        self.ports_hp4 = [3022, 0, 3021, 3080]
        self.ports_hp5 = [2022, 0, 2021, 2080]
        self.ports_hp6 = [3022, 0, 3021, 3080]
        self.ports = [self.ports_hp1, self.ports_hp2, self.ports_hp3, self.ports_hp4, self.ports_hp5,self.ports_hp6]

        # Porte esposte per ogni host
        self.ports_host1 = [22, 23, 2022, 2021, 2080, 3022, 3021, 3080]
        self.ports_host2 = [22, 23, 2022, 2021, 2080, 3022, 3021, 3080]

        # Service distribution on a host hk
        self.sd_h1 = u.product_vector_matrix(self.h_h1, self.sm)
        self.sd_h2 = u.product_vector_matrix(self.h_h2, self.sm)
        self.sdh = [elem1 + elem2 for elem1, elem2 in zip(self.sd_h1, self.sd_h2)]

        # Service busy: 1 if it is busy, else 0
        self.sb = [[0, 0, 0, 0], [0, 0, 0, 0],[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def add_new_honeypot_ti_management(self, new_honeypot, host, s_h, ports_h):
        # Aggiunta dell'oggetto Honeypot alla lista honeypots
        self.honeypots.append(new_honeypot)
        # AGGIUNTA NUOVO INDICE
        # Trova l'ultimo valore indice è anche il massimo
        last_index = max(self.index_honeypot.values())
        self.index_honeypot[new_honeypot.get_name()] = last_index + 1
        # Aggiunta alla lista h_h1 e h_h2
        if host == t.ti_host1:
            self.h_h1.append(1)
            self.h_h2.append(0)
        if host == t.ti_host2:
            self.h_h1.append(0)
            self.h_h2.append(1)
        #aggiunge service map dell'honeypot a matrice SM
        self.sm.append(s_h)

        # Aggiunta nuove porte a lista ports
        self.ports.append(ports_h)

        # Ricalcolo SDH
        self.sd_h1 = u.product_vector_matrix(self.h_h1, self.sm)
        self.sd_h2 = u.product_vector_matrix(self.h_h2, self.sm)
        self.sdh = [elem1 + elem2 for elem1, elem2 in zip(self.sd_h1, self.sd_h2)]
        # Aggiunta in sb
        busy_service = [0, 0, 0, 0]
        self.sb.append(busy_service)