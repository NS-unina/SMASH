import json

from controller import ExampleSwitch13
from webob import Response
from  ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.lib import dpid as dpid_lib
from ryu.lib.packet import arp, icmp
from network import Host, Honeypot, Subnet, Network, Gateway
from utils import Utils as u
from randmac import RandMac
import topology as t
import ti_management as man
import mapping as map
import functions as f
import requests

from ti_management import HoneypotManager
man = HoneypotManager()

name = 'rest_controller'
url = '/rest_controller/insert'
sub = '10.1.3.'
ips = []





class RestController(ExampleSwitch13):
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(RestController, self).__init__(*args, **kwargs)
        self.switches = {}
        wsgi = kwargs['wsgi']
        wsgi.register(SimpleSwitchController,
                      {name: self})


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        super(RestController, self).switch_features_handler(ev)
        datapath = ev.msg.datapath
        self.switches[datapath.id] = datapath
        self.mac_to_port.setdefault(datapath.id, {})


    def add_new_honeypot(name,host,s_hp,ports_hp):
        url = host.get_ip_addr() + ':8080/handle_post'  # URL host
        # Dati da inviare nel corpo della richiesta
        payload = {'name': name, 'ssh_port': ports_hp[man.SSH_INDEX], 'ftp_port': ports_hp[man.FTP_INDEX], 'socks_port': ports_hp[man.SOCKS5_INDEX]}  

        #INVIO EVENTO A HOST PER DEPLOYARE UN NUOVO HOST
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("Richiesta POST inviata con successo!")
        else:
            print("Si è verificato un errore durante l'invio della richiesta:", response.status_code)
            print("Messaggio di errore:", response.text)
        
        new_honeypot = Honeypot(name, host.get_ip_addr(), host.get_MAC_addr(), host.get_ovs_port(), host.get_netmask())
        t.honeypots_list.append(new_honeypot)
        map.decoy_mapping[new_honeypot.get_name] = t.honeypots_list[-1]
        man.add_new_honeypot_ti_management(new_honeypot,host,s_hp,ports_hp)

    

    def redirect_to(self, dpid, src_ip, tcp_port, source, destination, gw,destination_port):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.permit_tcp_dstIP_dstPORT(parser, destination.get_ip_addr(), destination.get_ovs_port(), int(destination_port), datapath)
        actions = [
            parser.OFPActionSetField(eth_dst=gw.get_MAC_addr()),
            parser.OFPActionSetField(ipv4_dst=destination.get_ip_addr()),
            parser.OFPActionSetField(tcp_dst=int(destination_port)),
            parser.OFPActionOutput(gw.get_ovs_port())
        ]
        match = parser.OFPMatch(
            eth_type=0x0800, ipv4_src=src_ip,
            ipv4_dst=source.get_ip_addr(), ip_proto=6, tcp_dst=int(tcp_port)
        )
        self.add_flow(datapath, 1000, match, actions, 1)

    def change_decoy_src(self, dpid, src_ip, subnet, decoy, tcp_port,gw,destination,destination_port):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=destination.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=destination.get_MAC_addr()),
                   parser.OFPActionSetField(tcp_src=int(tcp_port)),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=decoy.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src= gw.get_MAC_addr(), ip_proto=6, tcp_src=int(destination_port))                
        self.add_flow(datapath, 1000, match, actions, 1)



       
    # REDIRECTION TO COWRIE
    # Presuppongo che applico il MTD esclusivamente nella subnet1 (rete interna)

    def redirect_to_cowrie_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.ssh_service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_cowrie_src_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.ssh_service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)


    def redirect_to_heralding_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.ssh_service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_heralding_src_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.ssh_service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)   


    def change_heralding_src_ssh_int(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)     

    # PORT HOPPING
    def drop_http_syn(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet1, src_ip)
        actions = []
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=t.service.get_ip_addr(), 
                                eth_src=src_mac, ip_proto=6, tcp_dst=80)
        self.add_flow(datapath, 1000, match, actions, 0)

    def redirect_socks5_syn(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser        
        src_mac = u.host_to_mac(t.subnet1, src_ip)
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), 1080, datapath)

        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=t.service.get_ip_addr(), 
                                eth_src=src_mac, ip_proto=6, tcp_dst=1080)
        self.add_flow(datapath, 1000, match, actions, 0)

    def change_heralding_src_socks5(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip) 
        actions = [parser.OFPActionSetField(eth_src=t.service.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=1080)
        self.add_flow(datapath, 1000, match, actions, 0)


    # REDIRECTION TO HERALDING FOR DMZ HOST (SERVICE SSH, PORT 22)
    def redirect_to_heralding_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=t.gw10.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw10.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.dmz_service.get_ip_addr(), ip_proto=6, tcp_dst=22)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_heralding_src_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.dmz_service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=t.dmz_service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw10.get_MAC_addr(), ip_proto=6, tcp_src=22)                
        self.add_flow(datapath, 1000, match, actions, 1)
    
    # REDIRECT TO COWRIE FROM DMZ HOST (SERVICE SSH, PORT 22)
    def redirect_to_cowrie_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=t.gw10.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
                   parser.OFPActionOutput(t.gw10.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.dmz_service.get_ip_addr(), ip_proto=6, tcp_dst=22)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_cowrie_src_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.dmz_service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=t.dmz_service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw10.get_MAC_addr(), ip_proto=6, tcp_src=22)                
        self.add_flow(datapath, 1000, match, actions, 1)   

class SimpleSwitchController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[name]

    @route('restswitch', '/rest_controller/redirect_traffic', methods=['POST'])
    def redirect_traffic(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            tcp_port = richiesta['Tcp_port']
            decoy_json = richiesta['Decoy']
            source_json = richiesta['Source']
            gw=t.gw1
            subnet=t.subnet1
            #dpid = int(dpid)     
            dpid = t.br0_dpid

            
            
            decoy = map.decoy_mapping.get(decoy_json, None)
            source= map.source_mapping.get(source_json,None)
            decoy_index = map.index_decoy_mapping.get(decoy_json,None)
            port_index = map.index_port_mapping.get(tcp_port,None)

            # Trova il primo honeypot libero per quel servizio
            decoy_index = u.find_free_honeypot_by_service(man.sb, man.sm, port_index)
            

            #Da testare
            if decoy_index is None:
                print("Creazione nuovo honeypot")
                index = max(man.index_honeypot.values()) + 1
                #IL NOME SCELTO SARA DEL TIPO "heralding5"
                name ="heralding"+str(index)
                host = t.ti_host1
                new_ssh_port= f.find_free_port(man.ports_host1,4000)
                man.ports_host1.append(new_ssh_port)
                new_ftp_port= f.find_free_port(man.ports_host1,4000)
                man.ports_host1.append(new_ftp_port)
                new_socks_port= f.find_free_port(man.ports_host1,4000)
                man.ports_host1.append(new_socks_port)
                s_hp = [1, 0, 1, 1]
                ports_hp = [0, 0, 0, 0]
                ports_hp[0] = new_ssh_port
                ports_hp[1] = 0
                ports_hp[2] = new_ftp_port
                ports_hp[3] = new_socks_port
                print("Porte scelte",ports_hp)
                print("Porte host",man.ports_host1)
                f.add_new_honeypot(name,host,s_hp,ports_hp)
                decoy_index = u.find_free_honeypot_by_service(man.sb, man.sm, port_index)

            
            
            decoy = f.index_to_decoy_mapping.get (decoy_index,None)
            print("Matrice SB:",man.sb)
            print("Matrice SM:", man.sm)
            print("Matrice porte:", man.ports)

            print("L'honeypot libero per il servizio ", tcp_port, "è :", decoy.get_name())


           
            destination_port = man.ports[decoy_index][port_index]

            #In teoria questo if si puo togliere poichè andche per ssh viene trovato il primo honeypot libero con preferenza cowrie
            '''
            if(int(tcp_port) == 22):
                print("TCP 22")   
                a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
                b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]
                if (a and b) == 0:
                    decoy_index = man.COWRIE_INDEX
                    decoy = t.cowrie                    
                    destination_port = man.ports_hp1[man.SSH_INDEX]
                    print("Cowrie")
                    

                else: 
                    decoy_index = man.HERALDING_INDEX
                    #decoy=t.heralding1
                    decoy = t.heralding1
                    destination_port = man.ports_hp2[man.SSH_INDEX]
                    print("heralding")
            '''

            man.sb[decoy_index][port_index] = 1 
            
            print("Redirection dell'utente: ",src_IP, "del service:", source.get_ip_addr(), "All'honeypot: ", decoy.get_ip_addr(), "da porta: ", tcp_port, "to: ", destination_port)
            simple_switch.redirect_to(dpid,src_IP,tcp_port,source,decoy,gw,destination_port)
            simple_switch.change_decoy_src(dpid, src_IP,subnet,decoy,tcp_port,gw,source,destination_port)
            return Response(status=200)
        else:
            return Response(status=400)




    @route('restswitch', '/rest_controller/http_port_hopping', methods=['POST'])
    def http_port_hopping(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            #dpid = int(dpid)       
            dpid = t.br0_dpid
            man.sb[man.HERALDING_INDEX][man.SOCKS5_INDEX] = 1
            simple_switch.drop_http_syn(dpid, src_IP)
            simple_switch.redirect_socks5_syn(dpid, src_IP)
            simple_switch.change_heralding_src_socks5(dpid, src_IP)
     
            #simple_switch.change_http_port(dpid, src_IP)
            #simple_switch.drop_pop3_rst(dpid, src_IP)
            #simple_switch.send_to_controller(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
    
    @route('restswitch', '/rest_controller/redirect_ssh_dmz', methods=['POST'])
    def redirect_to_heralding_dmz_ssh(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            #dpid = int(dpid) 
            dpid = t.br1_dpid
            a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
            b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

            if (a and b) == 0: 
                man.sb[man.COWRIE_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_cowrie_ssh_ext(dpid, src_IP)
                simple_switch.change_cowrie_src_ssh_ext(dpid, src_IP)
            else:           
                man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_heralding_ssh_ext(dpid, src_IP)
                simple_switch.change_heralding_src_ssh_ext(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
        

    @route('restswitch', '/rest_controller/push_int_server_out', methods=['POST'])
    def push_int_server_out(self, req, **kwargs):
            richiesta = req.json
            simple_switch = self.simple_switch_app
            if richiesta:
                print(richiesta)
                src_IP = richiesta['Source_IP']
                #dpid = int(dpid) 
                dpid = t.br0_dpid

                a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
                b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

                #if (a and b) == 0: 
                man.sb[man.COWRIE_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_cowrie_ssh_int_dup(dpid, src_IP)
                simple_switch.change_cowrie_src_ssh_int_dup(dpid, src_IP)
                #else:           
                    #man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                    #simple_switch.redirect_to_heralding_ssh_int_dup(dpid, src_IP)
                    #simple_switch.change_heralding_src_ssh_int_dup(dpid, src_IP)
                return Response(status=200)
            else:
                return Response(status=400)
            
    @route('restswitch', '/rest_controller/push_dmz_server_out', methods=['POST'])
    def push_dmz_server_out(self, req, **kwargs):
            richiesta = req.json
            simple_switch = self.simple_switch_app
            if richiesta:
                print(richiesta)
                src_IP = richiesta['Source_IP']
                #dpid = int(dpid) 
                dpid = t.br1_dpid

                a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
                b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

                #if (a and b) == 0: 
                man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_heralding_ssh_ext(dpid, src_IP)
                simple_switch.change_heralding_src_ssh_ext(dpid, src_IP)
                #else:           
                    #man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                    #simple_switch.redirect_to_heralding_ssh_int_dup(dpid, src_IP)
                    #simple_switch.change_heralding_src_ssh_int_dup(dpid, src_IP)
                return Response(status=200)
            else:
                return Response(status=400)


name ="claudio"
host = t.ti_host1
s_hp = [1, 0, 1, 1]
ports_hp = [7022, 0, 6021, 6080]

#f.add_new_honeypot(name,host,s_hp,ports_hp)