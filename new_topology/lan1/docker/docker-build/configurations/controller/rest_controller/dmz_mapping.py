# decoy_mapping.py
from dmz_ti_management import HoneypotManagerDmz
from topology import NetworkTopology


t = NetworkTopology()
man = HoneypotManagerDmz()

decoy_mapping = {
    "dmz_cowrie1": t.cowrie_dmz,   
    "dmz_heralding": t.heralding1_dmz,
    "dmz_heralding1": t.heralding1_dmz,
    "heralding2": t.heralding2_dmz,  
}
source_mapping = {
    "service": t.service,
    "ssh_service": t.ssh_service,
    "dmz_service": t.dmz_service
}
index_decoy_mapping = {
    "dmz_cowrie1": man.index_honeypot.get("cowrie1",None),
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
    "gw10": t.gw10
}

subnet_mapping = {
    "subnet1": t.subnet1,
    "subnet4": t.subnet4,
    "subnet5": t.subnet5,
    "subnet6":t.subnet6
}

dpid_mapping = {
    "br0": t.br0_dpid,
    "br1": t.br1_dpid
}

