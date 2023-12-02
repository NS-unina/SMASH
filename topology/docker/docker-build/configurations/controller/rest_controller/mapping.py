# decoy_mapping.py
import ti_management as man
import topology as t

decoy_mapping = {
    "heralding": t.heralding,
    "heralding1": t.heralding1,
    "cowrie": t.cowrie    
}
source_mapping = {
    "service": t.service,
}
index_decoy_mapping = {
    "heralding1": man.HERALDING_INDEX,
    "cowrie": man.COWRIE_INDEX
}

index_port_mapping = {
    "21": man.FTP_INDEX,
    "22": man.SSH_INDEX,
    "23": man.TELNET_INDEX
}

