# decoy_mapping.py
import ti_management as man
import topology as t

decoy_mapping = {
    "heralding": t.heralding,
    "heralding1": t.heralding1,
    "heralding2": t.heralding2,
    "heralding3": t.heralding3,
    "heralding4": t.heralding4,
    "cowrie": t.cowrie    
}
source_mapping = {
    "service": t.service,
}
index_decoy_mapping = {
    "heralding1": man.HERALDING1_INDEX,
    "heralding2": man.HERALDING2_INDEX,
    "heralding3": man.HERALDING3_INDEX,
    "heralding4": man.HERALDING4_INDEX,
    "cowrie": man.COWRIE_INDEX
}

index_port_mapping = {
    "21": man.FTP_INDEX,
    "22": man.SSH_INDEX,
    "23": man.TELNET_INDEX,
    "1080": man.SOCKS5_INDEX
}

