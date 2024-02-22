# decoy_mapping.py
from ti_management import HoneypotManager
from topology import NetworkTopology


t = NetworkTopology()
man = HoneypotManager()

decoy_mapping = {
    "cowrie1": t.cowrie1,   
    "cowrie2":t.cowrie2, 
    "heralding": t.heralding,
    "heralding1": t.heralding1,
    "heralding2": t.heralding2,
    "heralding3": t.heralding3,
    "heralding4": t.heralding4,    
}
source_mapping = {
    "service": t.service,
    "ssh_service": t.ssh_service
}
index_decoy_mapping = {
    "cowrie1": man.index_honeypot.get("cowrie1",None),
    "cowrie2": man.index_honeypot.get("cowrie2",None),
    "heralding1": man.index_honeypot.get("heralding1",None),
    "heralding2": man.index_honeypot.get("heralding1",None),
    "heralding3": man.index_honeypot.get("heralding1",None),
    "heralding4": man.index_honeypot.get("heralding1",None),
    
}

index_port_mapping = {
    "21": man.FTP_INDEX,
    "22": man.SSH_INDEX,
    "23": man.TELNET_INDEX,
    "1080": man.SOCKS5_INDEX
}

