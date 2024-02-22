from network import Host, Honeypot, Attacker, Subnet, Network, Gateway

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
        # Nodes
        # Subnet 1
        self.host = Host('host', '10.1.3.10', '08:00:27:b6:d0:66', 15, '255.255.255.0')
        self.service = Host('service', '10.1.3.11', '08:00:27:6d:ec:62', 3, '255.255.255.0')
        self.ssh_service = Host('ssh_service', '10.1.3.13', '08:00:27:b6:d0:69', 16, '255.255.255.0')
        self.heralding = Honeypot('heralding', '10.1.3.12', '08:00:27:6c:0a:bf', 4, '255.255.255.0')

        # Subnet 2
        self.ti_host1 = Host('ti_host1', '10.1.4.10', '08:00:27:b7:0e:58', 6, '255.255.255.0')
        self.ti_host2 = Host('ti_host2', '10.1.4.17', '08:00:27:6d:ec:c4', 25, '255.255.255.0')

        self.cowrie1 = Honeypot('cowrie1', '10.1.4.10', '08:00:27:b7:0e:58', 6, '255.255.255.0')
        self.cowrie2 = Honeypot('cowrie2', '10.1.4.17', '08:00:27:6d:ec:c4', 25, '255.255.255.0')       
        self.heralding1 = Honeypot('heralding1', '10.1.4.10', '08:00:27:b7:0e:58', 6, '255.255.255.0')
        self.heralding2 = Honeypot('heralding2', '10.1.4.10', '08:00:27:b7:0e:58', 6, '255.255.255.0')
        self.heralding3 = Honeypot('heralding3', '10.1.4.17', '08:00:27:6d:ec:c4', 25, '255.255.255.0')
        self.heralding4 = Honeypot('heralding4', '10.1.4.17', '08:00:27:6d:ec:c4', 25, '255.255.255.0')

        self.honeypots_list = [self.cowrie1, self.cowrie2, self.heralding1, self.heralding2, self.heralding3, self.heralding4]

        self.elk_if1 = Host('ELK_IF1', '10.1.5.10', '08:00:27:7d:b7:b8', 8, '255.255.255.0')
        self.elk_if2 = Host('ELK_IF2', '10.1.11.10', '08:00:27:f5:6b:90', 13, '255.255.255.0')

        self.dmz_heralding = Honeypot('dmz_heralding', '10.1.10.10', '08:00:27:2c:30:92', 2, '255.255.255.0')
        self.dmz_service = Host('dmz_service', '10.1.10.11', '08:00:27:b6:d0:67', 22, '255.255.255.0')
        self.dmz_service1 = Host('dmz_service1', '10.1.10.14', '08:00:27:6d:ec:74', 21, '255.255.255.0')
        self.dmz_cowrie = Honeypot('dmz_cowrie', '10.1.10.13', '08:00:27:b7:0e:59', 20, '255.255.255.0')
        self.dmz_host = Host('dmz_host', '10.1.10.12', '08:00:27:b6:d0:68', 23, '255.255.255.0')

        # Subnets
        # ovs1
        self.subnet1 = Subnet('S1', '10.1.3.0', '255.255.255.0')
        self.subnet2 = Subnet('S2', '10.1.4.0', '255.255.255.0')
        self.subnet3 = Subnet('S3', '10.1.5.0', '255.255.255.0')
        # ovs2
        self.subnet4 = Subnet('S4', '10.1.10.0', '255.255.255.0')
        self.subnet5 = Subnet('S5', '10.1.11.0', '255.255.255.0')

        # Gateways
        # ovs1
        self.gw1 = Gateway('gw1', '10.1.3.1', '9e:c3:c6:49:0e:e8', 1, '255.255.255.0')
        self.gw2 = Gateway('gw2', '10.1.4.1', '16:67:1f:3f:86:a7', 5, '255.255.255.0')
        self.gw3 = Gateway('gw3', '10.1.5.1', 'fe:46:67:35:0d:d1', 7, '255.255.255.0')
        # ovs2
        self.gw10 = Gateway('gw10', '10.1.10.1', '8a:ae:02:40:8f:83', 10, '255.255.255.0')
        self.gw11 = Gateway('gw11', '10.1.11.1', 'ea:6a:20:a0:96:10', 11, '255.255.255.0')

        # Network
        self.network1 = Network('Net1')
        self.network2 = Network('Net2')

        # Aggiungi nodi alle subnet
        self.add_nodes_to_subnets()

        # Aggiungi subnet alle reti
        self.add_subnets_to_networks()

        self.ports = [5432, 143, 5900, 3306]
        self.br0_dpid = 64105189026373
        self.br1_dpid = 64105189026374



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
        self.subnet2.add_node(self.ti_host2, self.ti_host2.get_ovs_port())
        self.subnet2.add_node(self.gw2, self.gw2.get_ovs_port())

        # Subnet 3
        self.subnet3.add_node(self.elk_if1, self.elk_if1.get_ovs_port())
        self.subnet3.add_node(self.gw3, self.gw3.get_ovs_port())

        # Subnet 4
        self.subnet4.add_node(self.dmz_service, self.dmz_service.get_ovs_port())
        self.subnet4.add_node(self.dmz_heralding, self.dmz_heralding.get_ovs_port())
        self.subnet4.add_node(self.dmz_host, self.dmz_host.get_ovs_port())
        self.subnet4.add_node(self.dmz_cowrie, self.dmz_cowrie.get_ovs_port())
        self.subnet4.add_node(self.dmz_service1, self.dmz_service1.get_ovs_port())
        self.subnet4.add_node(self.gw10, self.gw10.get_ovs_port())

        # Subnet 5
        self.subnet5.add_node(self.elk_if2, self.elk_if2.get_ovs_port())
        self.subnet5.add_node(self.gw11, self.gw11.get_ovs_port())

    def add_subnets_to_networks(self):
        # Aggiungi subnet alle reti
        self.network1.add_subnet(self.subnet1)
        self.network1.add_subnet(self.subnet2)
        self.network1.add_subnet(self.subnet3)

        self.network2.add_subnet(self.subnet4)
        self.network2.add_subnet(self.subnet5)