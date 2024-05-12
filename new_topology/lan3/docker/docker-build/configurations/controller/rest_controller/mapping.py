# decoy_mapping.py
from ti_management import HoneypotManager
from topology import NetworkTopology


t = NetworkTopology()
man = HoneypotManager()

decoy_mapping = {
    "cowrie1": t.cowrie1,   
    "heralding": t.heralding,
    "heralding1": t.heralding1,
    "heralding2": t.heralding2,  
}
source_mapping = {
    "service": t.service,
}
index_decoy_mapping = {
    "cowrie1": man.index_honeypot.get("cowrie1",None),
    "heralding1": man.index_honeypot.get("heralding1",None),
    "heralding2": man.index_honeypot.get("heralding2",None),
    
}

index_port_mapping = {
    "21": man.FTP_INDEX,
    "22": man.SSH_INDEX,
    "23": man.TELNET_INDEX,
    "1080": man.SOCKS5_INDEX
}

gateway_mapping = {
    "gw1": t.gw1,
}

subnet_mapping = {
    "subnet1": t.subnet1,
}

dpid_mapping = {
    "br0": t.br0_dpid,
    "br1": t.br1_dpid
}

