# decoy_mapping.py
from ti_management import HoneypotManager
from topology import NetworkTopology


t = NetworkTopology()
man = HoneypotManager()

decoy_mapping = {
    "cowrie": t.cowrie,    
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
    "cowrie": man.COWRIE_INDEX,
    "heralding1": man.HERALDING1_INDEX,
    "heralding2": man.HERALDING2_INDEX,
    "heralding3": man.HERALDING3_INDEX,
    "heralding4": man.HERALDING4_INDEX,
    
}

index_port_mapping = {
    "21": man.FTP_INDEX,
    "22": man.SSH_INDEX,
    "23": man.TELNET_INDEX,
    "1080": man.SOCKS5_INDEX
}

