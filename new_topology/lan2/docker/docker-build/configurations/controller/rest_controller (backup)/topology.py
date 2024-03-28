from network import Host, Honeypot, Attacker, Subnet, Network, Gateway
import random
import ipaddress
#------- NETWORK TOPOLPOGY LAN1 -------------------------------------------------------------- #    
# Nodes
class NetworkTopology:

    #PATTERN SINGLETON
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NetworkTopology, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance
    def __init__(self):
        # ------- NETWORK TOPOLOGY LAN1 -------------------------------------------------------------- #
        self.br0_dpid = 64105189026377

        # Subnets
        # ovs1
        self.subnet1 = Subnet('S1', '10.2.3.0', '255.255.255.0',self.br0_dpid)
        self.subnet2 = Subnet('S2', '10.2.4.0', '255.255.255.0',self.br0_dpid)
        self.subnet3 = Subnet('S3', '10.2.5.0', '255.255.255.0',self.br0_dpid)

        # Nodes
        # Subnet 1
        self.host = Host('host', '10.2.3.10', '08:00:27:b6:d0:46', 39, '255.255.255.0',self.subnet1)
        self.service = Host('service', '10.2.3.11', '08:00:27:6d:ec:51', 31, '255.255.255.0', self.subnet1)
        self.ssh_service = Host('ssh_service', '10.2.3.13', '08:00:27:b6:d0:61', 37, '255.255.255.0', self.subnet1)
        self.heralding = Honeypot('heralding', '10.2.3.12', '08:00:27:6c:0a:bc', 32, '255.255.255.0', self.subnet1)

        # Subnet 2
        self.ti_host1 = Host('ti_host1', '10.2.4.10', '08:00:27:b7:0e:59', 33, '255.255.255.0', self.subnet2)

        self.cowrie1 = Honeypot('cowrie1', '10.2.4.10', '08:00:27:b7:0e:59', 33, '255.255.255.0', self.subnet2)
        self.heralding1 = Honeypot('heralding1', '10.2.4.10', '08:00:27:b7:0e:59', 33, '255.255.255.0', self.subnet2)
        self.heralding2 = Honeypot('heralding2', '10.2.4.10', '08:00:27:b7:0e:59', 33, '255.255.255.0', self.subnet2)


        self.honeypots_list = [self.cowrie1, self.heralding1, self.heralding2]
        self.hosts_list= [self.ti_host1]
        self.host_redirected = ["10.2.5.1", "10.2.3.1"]

        self.elk_if1 = Host('ELK_IF1', '10.2.5.10', '08:00:27:7d:b7:b8', 8, '255.255.255.0', self.subnet3)

        self.nodes = [self.host, self.service,self.ssh_service,self.heralding,self.elk_if1]
        
        
        # Gateways
        # ovs1
        self.gw1 = Gateway('gw1', '10.2.3.1', '8a:ae:02:40:8f:96', 50, '255.255.255.0',self.subnet1)
        self.gw2 = Gateway('gw2', '10.2.4.1', 'ea:6a:20:a0:96:15', 51, '255.255.255.0',self.subnet2)
        self.gw3 = Gateway('gw3', '10.2.5.1', 'ea:6a:20:a0:96:17', 52, '255.255.255.0', self.subnet3)


        self.gateway = [self.gw1,self.gw2,self.gw3]
        # Network
        self.network1 = Network('Net1')

        # Aggiungi nodi alle subnet
        self.add_nodes_to_subnets()

        # Aggiungi subnet alle reti
        self.add_subnets_to_networks()

        self.ports = [5432, 143, 5900, 3306]



# Add nodes to subnets
# ovs1
    def add_nodes_to_subnets(self):
        # Aggiungi nodi alle subnet

        # Subnet 1
        self.subnet1.add_node(self.host, self.host.get_ovs_port())
        self.subnet1.add_node(self.heralding, self.heralding.get_ovs_port())
        self.subnet1.add_node(self.service, self.service.get_ovs_port())
        self.subnet1.add_node(self.ssh_service, self.ssh_service.get_ovs_port())
        self.subnet1.add_node(self.gw1, self.gw1.get_ovs_port())

        # Subnet 2
        self.subnet2.add_node(self.ti_host1, self.ti_host1.get_ovs_port())

        self.subnet2.add_node(self.gw2, self.gw2.get_ovs_port())

        # Subnet 3
        self.subnet3.add_node(self.elk_if1, self.elk_if1.get_ovs_port())
        self.subnet3.add_node(self.gw3, self.gw3.get_ovs_port())


    def add_subnets_to_networks(self):
        # Aggiungi subnet alle reti
        self.network1.add_subnet(self.subnet1)
        self.network1.add_subnet(self.subnet2)
        self.network1.add_subnet(self.subnet3)



    def find_free_mac_address(self):
        # Lista di tutti i MAC address utilizzati
        used_mac_addresses = set()

        # Esamina tutti i nodi nella topologia
        for node in self.honeypots_list + self.hosts_list + self.nodes:
            used_mac_addresses.add(node.get_MAC_addr())

        # Crea tre coppie casuali di caratteri per il suffisso del MAC address
        random_suffix_pairs = ["".join(random.choice("0123456789abcdef") for _ in range(2)) for _ in range(3)]

        # Combina le coppie casuali con i puntini
        random_suffix = ":".join(random_suffix_pairs)

        # Combina il prefisso fisso con la parte casuale
        mac_address = "08:00:27:" + random_suffix

        # Crea un MAC address casuale finché non trovi uno non utilizzato
        while mac_address in used_mac_addresses:
            # Rigenera il suffisso casuale
            random_suffix_pairs = ["".join(random.choice("0123456789abcdef") for _ in range(2)) for _ in range(3)]
            random_suffix = ":".join(random_suffix_pairs)
            mac_address = "08:00:27:" + random_suffix

        return mac_address
    
    def find_host_by_ip(self, ip):
        for node in self.honeypots_list + self.hosts_list + self.nodes + self.gateway:
            if node.get_ip_addr() == ip:
                return node
        return None
        
    
    def find_free_ip_address(self,subnet_str):
        # Lista di tutti gli ip address utilizzati
        used_ip_addresses = set()

        # Esamina tutti i nodi nella topologia
        for node in self.honeypots_list + self.hosts_list + self.nodes + self.gateway:
            used_ip_addresses.add(node.get_ip_addr())

        # Parsa la stringa della sottorete per ottenere l'oggetto di tipo ipaddress.IPv4Network
        subnet = ipaddress.IPv4Network(subnet_str)
        # Ottieni tutti gli indirizzi IP utilizzabili nella sottorete (escludendo indirizzo di rete e di broadcast)
        usable_ips = [str(ip) for ip in subnet.hosts()]
        # Genera un indirizzo IP casuale tra quelli utilizzabili
        random_ip = random.choice(usable_ips)

        while random_ip in used_ip_addresses:
            # Rigenera un indirizzo IP casuale tra quelli utilizzabili
            random_ip = random.choice(usable_ips)
            
        return random_ip