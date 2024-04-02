# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.hub import spawn
from utils import Utils as u
from network import Host, Honeypot, Attacker, Subnet, Network, Gateway
from ryu.lib.packet import tcp, icmp, arp, ipv4, vlan
import random
from topology import NetworkTopology
from ti_management import HoneypotManager
from dmz_ti_management import HoneypotManagerDmz
import mapping as map
import dmz_mapping as dmz_map
import functions as f
t = NetworkTopology()
man = HoneypotManager()
man_dmz = HoneypotManagerDmz()

class ExampleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ExampleSwitch13, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}
        self.mac_to_ip = {}
        self.port = None
        self.attacker = None
        self.dpid_br0 = 64105189026373
        self.dpid_br1 = 64105189026374

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id

        print(dpid)

        if dpid == t.br0_dpid:
            print(dpid)
            self.port = t.ports[random.randint(0, 3)]
            # install the table-miss flow entry.
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                            ofproto.OFPCML_NO_BUFFER)]
            #self.send_set_async(datapath)
            self.add_flow(datapath, 0, match, actions, 0)
            self.add_default_rules_br0(datapath)
            
        
        if dpid == t.br1_dpid:
            # install the table-miss flow entry
            print(dpid)
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, 0, match, actions, 0)
            self.add_default_rules_br1(datapath)
            
    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id


        if dpid == t.br0_dpid:
            if msg.cookie == 4:
                values = msg.match.items()
                print(values)
                ipv4_dst = values[1][1]
                port_dst = values[3][1]
                #self.drop_tcp_dstIP_dstPORT(parser, ipv4_dst, port_dst, datapath) 
            
                self.port = t.ports[random.randint(0, 3)]
                self.redirect_protocol_syn(parser, datapath, self.port)
                self.change_heralding_src_protocol(parser, datapath, self.port)
        
        if dpid == t.br1_dpid:
            pass
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        ip_dst = None
        tcp_ports = ["22","21", "23", "1080"]
        decoy_ip = ["10.1.3.12", "10.1.3.18", "10.1.10.10"]
        trigger_port = ["22,21"]

        # get the ipv4 destination address
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
        arp_pkt = pkt.get_protocol(arp.arp)
        if ipv4_pkt or arp_pkt:
            if ipv4_pkt:
                ip_dst = ipv4_pkt.dst
                src_ip = ipv4_pkt.src
                #print(ip_dst, "PACCHETTO IP")

            elif arp_pkt:
                ip_dst = arp_pkt.dst_ip
                src_ip = arp_pkt.src_ip
                #print(ip_dst, "PACCHETTO ARP")
            
            dst_port = "22"
            # install a redirection flow
            
            
            if ip_dst in decoy_ip and src_ip not in t.host_redirected:
                
                source = t.service
                gw= t.gw1
                host = t.find_host_by_ip(src_ip)
                subnet = host.get_subnet()
                print(host.get_ip_addr())
                br_dpid = subnet.get_br()


                if br_dpid == t.br1_dpid:
                    source = t.dmz_service
                    gw = t.gw10
                    for tcp_port in tcp_ports:
                        spawn(self.redirect_traffic_dmz,self,src_ip,tcp_port,source,gw,subnet,br_dpid)                  
                        print("REGOLA REDIRECTION INSERITA DIRETTAMENTE DAL CONTROLLER DMZ")   
                else:
                    for tcp_port in tcp_ports:
                        spawn(self.redirect_traffic,self,src_ip,tcp_port,source,gw,subnet,br_dpid)                  
                        print("REGOLA REDIRECTION INSERITA DIRETTAMENTE DAL CONTROLLER")

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']
        out_port = ofproto.OFPP_FLOOD

        if dpid == t.br0_dpid:
            if dst == t.host.get_MAC_addr():
                out_port = t.host.get_ovs_port()
            elif dst == t.service.get_MAC_addr():
                out_port = t.service.get_ovs_port()
            elif dst == t.heralding.get_MAC_addr():
                out_port = t.heralding.get_ovs_port()
            elif dst == t.gw1.get_MAC_addr():
                out_port = t.gw1.get_ovs_port()
            elif dst == t.gw2.get_MAC_addr():
                out_port = t.gw2.get_ovs_port()
            elif dst == t.elk_if1.get_MAC_addr():
                out_port = t.elk_if1.get_ovs_port()
            elif dst == t.gw3.get_MAC_addr():
                out_port = t.gw3.get_ovs_port()
            elif dst == t.ti_host1.get_MAC_addr():
                out_port = t.ti_host1.get_ovs_port()
            elif dst == t.ti_host2.get_MAC_addr():
                out_port = t.ti_host2.get_ovs_port()


            actions = [parser.OFPActionOutput(out_port)]

            # install a flow to avoid packet_in next time.
            if out_port != ofproto.OFPP_FLOOD:
                match = parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions, 0)

            # construct packet_out message and send it.
            out = parser.OFPPacketOut(datapath=datapath,
                                    buffer_id=ofproto.OFP_NO_BUFFER,
                                    in_port=in_port, actions=actions,
                                    data=msg.data)
            datapath.send_msg(out)

        if dpid == t.br1_dpid:
            if dst == t.dmz_service.get_MAC_addr():
                out_port = t.dmz_service.get_ovs_port()
            elif dst == t.dmz_heralding.get_MAC_addr():
                out_port = t.dmz_heralding.get_ovs_port()
            elif dst == t.dmz_host.get_MAC_addr():
                out_port = t.dmz_host.get_ovs_port()
            elif dst == t.gw10.get_MAC_addr():
                out_port = t.gw10.get_ovs_port()
            elif dst == t.elk_if2.get_MAC_addr():
                out_port = t.elk_if2.get_ovs_port()
            elif dst == t.gw11.get_MAC_addr():
                out_port = t.gw11.get_ovs_port()
            elif dst == t.ti_host1.get_MAC_addr():
                out_port = t.ti_host1.get_ovs_port()
            elif dst == t.ti_host2.get_MAC_addr():
                out_port = t.ti_host2.get_ovs_port()
            elif dst == t.ti_host_dmz.get_MAC_addr():
                out_port = t.ti_host_dmz.get_ovs_port()

            actions = [parser.OFPActionOutput(out_port)]
            
            

            # install a flow to avoid packet_in next time.
            if out_port != ofproto.OFPP_FLOOD:
                match = parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions, 0)

            # construct packet_out message and send it.
            out = parser.OFPPacketOut(datapath=datapath,
                                    buffer_id=ofproto.OFP_NO_BUFFER,
                                    in_port=in_port, actions=actions,
                                    data=msg.data)
            datapath.send_msg(out)

    # UTILITY FUNCTIONS
    def add_flow(self, datapath, priority, match, actions, cookie):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, cookie=cookie,
                                match=match, instructions=inst, idle_timeout=0, 
                                hard_timeout=0)
        datapath.send_msg(mod)

    def add_flow_with_hard(self, datapath, priority, match, actions, cookie):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, cookie=cookie,
                                match=match, instructions=inst, flags=ofproto.OFPFF_SEND_FLOW_REM, idle_timeout=0, hard_timeout=20)
        datapath.send_msg(mod)

    def del_rules(self, datapath, cookie, match):
        ofproto = datapath.ofproto
        inst = []
        flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, ofproto.OFPTT_ALL,
                                                      ofproto.OFPFC_DELETE, 0, 0,
                                                      0,
                                                      ofproto.OFPCML_NO_BUFFER,
                                                      ofproto.OFPP_ANY,
                                                      ofproto.OFPG_ANY, 0,
                                                      match, inst)
        datapath.send_msg(flow_mod)

    def add_default_rules_br0(self, datapath):
        parser = datapath.ofproto_parser
        self.drop_arp_srcIP_srcMAC(parser, t.gw1.get_ip_addr(), t.gw2.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw1.get_ip_addr(), t.gw3.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw1.get_ip_addr(), '5c:87:9c:33:d9:d4', datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw1.get_ip_addr(), t.gw10.get_MAC_addr(), datapath, 2)        
        self.drop_arp_srcIP_srcMAC(parser, t.gw1.get_ip_addr(), t.gw11.get_MAC_addr(), datapath, 2) 

        self.drop_arp_srcIP_srcMAC(parser, t.gw2.get_ip_addr(), t.gw1.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw2.get_ip_addr(), t.gw3.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw2.get_ip_addr(), '5c:87:9c:33:d9:d4', datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw2.get_ip_addr(), t.gw10.get_MAC_addr(), datapath, 2)        
        self.drop_arp_srcIP_srcMAC(parser, t.gw2.get_ip_addr(), t.gw11.get_MAC_addr(), datapath, 2)

        self.drop_arp_srcIP_srcMAC(parser, t.gw3.get_ip_addr(), t.gw1.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw3.get_ip_addr(), t.gw2.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw3.get_ip_addr(), '5c:87:9c:33:d9:d4', datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, t.gw3.get_ip_addr(), t.gw10.get_MAC_addr(), datapath, 2)        
        self.drop_arp_srcIP_srcMAC(parser, t.gw3.get_ip_addr(), t.gw11.get_MAC_addr(), datapath, 2)


        # DROP host to elk
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.host.get_ip_addr(), t.host.get_MAC_addr(), 
                                         t.elk_if1.get_ip_addr(), datapath)
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.host.get_ip_addr(), t.host.get_MAC_addr(), 
                                         t.elk_if1.get_ip_addr(), datapath)
        
        # DROP host to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.host.get_ip_addr(), t.host.get_MAC_addr(), 
                                         '10.1.5.100', datapath)      
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.host.get_ip_addr(), t.host.get_MAC_addr(), 
                                         '10.1.5.100', datapath)  
             
        # DROP service to elk
        # self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.service.get_ip_addr(), t.service.get_MAC_addr(), 
        #                                  t.elk_if1.get_ip_addr(), datapath)        
        # self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.service.get_ip_addr(), t.service.get_MAC_addr(), 
        #                                  t.elk_if1.get_ip_addr(), datapath)    
           
        # DROP service to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.service.get_ip_addr(), t.service.get_MAC_addr(), 
                                         '10.1.5.100', datapath)
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.service.get_ip_addr(), t.service.get_MAC_addr(), 
                                         '10.1.5.100', datapath)    
           
        # DROP heralding to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.heralding.get_ip_addr(), t.heralding.get_MAC_addr(), 
                                         '10.1.5.100', datapath)    
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.heralding.get_ip_addr(), t.heralding.get_MAC_addr(), 
                                         '10.1.5.100', datapath)  
        
        # DROP ti_host1 to controller    
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_MAC_addr(), 
                                         '10.1.5.100', datapath)    
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_MAC_addr(), 
                                         '10.1.5.100', datapath)
        
        # DROP ti_host2 to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_MAC_addr(), 
                                         '10.1.5.100', datapath)    
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_MAC_addr(), 
                                         '10.1.5.100', datapath)          

        # DROP arp input to service
        #self.drop_tcp_dstIP(parser, t.service.get_ip_addr(), datapath)
        self.permit_tcp_host1_host2(parser, t.gw1.get_ip_addr(), t.service.get_ip_addr(), t.service.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.service.get_ip_addr(), t.service.get_ovs_port(), datapath)

        # PERMIT tcp input to service port 22
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), 22, datapath)

        # PERMIT tcp input to service port 23
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), 23, datapath)

        # PERMIT tcp input to service port 80
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), 80, datapath)

        # PERMIT tcp input to service port 21
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), 21, datapath)

        # DROP arp input to heralding
        self.drop_tcp_dstIP(parser, t.heralding.get_ip_addr(), datapath)

        # PERMIT tcp input from service to heralding
        self.permit_tcp_host1_host2(parser, t.service.get_ip_addr(), t.heralding.get_ip_addr(), t.heralding.get_ovs_port(), datapath)
        # PERMIT tcp input from gateway and elk to heralding
        self.permit_tcp_host1_host2(parser, t.gw1.get_ip_addr(), t.heralding.get_ip_addr(), t.heralding.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.heralding.get_ip_addr(), t.heralding.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.dmz_heralding.get_ip_addr(), t.dmz_heralding.get_ovs_port(), datapath)

        # PERMIT tcp input to heralding port 25
        self.permit_tcp_dstIP_dstPORT(parser, t.heralding.get_ip_addr(), t.heralding.get_ovs_port(), 25, datapath)

        # PERMIT tcp input from service to honeyfarm
        self.permit_tcp_host1_host2(parser, t.service.get_ip_addr(), t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.service.get_ip_addr(), t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), datapath)
        # PERMIT tcp input from gateway and elk to heralding
        self.permit_tcp_host1_host2(parser, t.gw1.get_ip_addr(), t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.gw1.get_ip_addr(), t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), datapath)

        # PERMIT tcp input to honeyfarm
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), 2022, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), 3022, datapath)
        # PERMIT tcp input to honeyfarm
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), 2022, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), 3022, datapath)  

        # DROP arp input to ti_host1
        self.drop_tcp_dstIP(parser, t.ti_host1.get_ip_addr(), datapath)
        self.permit_tcp_host1_host2(parser, t.gw1.get_ip_addr(), t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), datapath)

        # PERMIT tcp input to ti_host1 port 22
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), 22, datapath)
        # PERMIT tcp input to ti_host1 port 22
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), 8080, datapath)

        # PERMIT tcp input to ti_host1 port 23
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host1.get_ip_addr(), t.ti_host1.get_ovs_port(), 23, datapath)

        
        # DROP arp input to ti_host2
        self.drop_tcp_dstIP(parser, t.ti_host2.get_ip_addr(), datapath)
        self.permit_tcp_host1_host2(parser, t.gw1.get_ip_addr(), t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if1.get_ip_addr(), t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), datapath)

        # PERMIT tcp input to ti_host2 port 22
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), 22, datapath)
        # PERMIT tcp input to ti_host2 port 22
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), 8080, datapath)

        # PERMIT tcp input to ti_host2 port 23
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host2.get_ip_addr(), t.ti_host2.get_ovs_port(), 23, datapath)

        self.forward_to_controller(parser, t.heralding.get_ip_addr(),datapath)

        # MTD PROACTIVE PORT SHUFFLING STARTING RULES
        self.redirect_protocol_syn(parser, datapath, self.port)
        self.change_heralding_src_protocol(parser, datapath, self.port)

    def add_default_rules_br1(self, datapath):
        parser = datapath.ofproto_parser

        self.drop_icmp_srcIP_srcPORT_dstIP(parser, t.gw11.get_ip_addr(), 4, '10.1.11.100', datapath)
        self.drop_tcp_srcIP_srcPORT_dstIP(parser, t.gw11.get_ip_addr(), 4, '10.1.11.100', datapath)

        self.drop_icmp_srcIP_srcPORT_dstIP(parser, t.dmz_service.get_ip_addr(), 22, '10.1.11.100', datapath)
        self.drop_tcp_srcIP_srcPORT_dstIP(parser, t.dmz_service.get_ip_addr(), 22, '10.1.11.100', datapath)

        self.drop_icmp_host1_host2(parser, t.host.get_ip_addr(), t.elk_if2.get_ip_addr(), datapath)
        self.drop_tcp_host1_host2(parser, t.host.get_ip_addr(), t.elk_if2.get_ip_addr(), datapath)
        self.drop_icmp_srcIP_srcPORT_dstIP(parser, t.dmz_service.get_ip_addr(), 22, t.elk_if2.get_ip_addr(), datapath)
        self.drop_tcp_srcIP_srcPORT_dstIP(parser, t.dmz_service.get_ip_addr(), 22, t.elk_if2.get_ip_addr(), datapath)

        # PERMIT tcp input from service to heralding
        self.permit_tcp_host1_host2(parser, t.dmz_service.get_ip_addr(), t.dmz_heralding.get_ip_addr(), t.dmz_heralding.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.dmz_service1.get_ip_addr(), t.dmz_heralding.get_ip_addr(), t.dmz_heralding.get_ovs_port(), datapath)
        # PERMIT tcp input from gateway and elk to heralding
        self.permit_tcp_host1_host2(parser, t.gw11.get_ip_addr(), t.dmz_heralding.get_ip_addr(), t.dmz_heralding.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if2.get_ip_addr(), t.dmz_heralding.get_ip_addr(), t.dmz_heralding.get_ovs_port(), datapath)

        # PERMIT tcp input to heralding port 25
        self.permit_tcp_dstIP_dstPORT(parser, t.dmz_heralding.get_ip_addr(), t.dmz_heralding.get_ovs_port(), 25, datapath)

        # PERMIT tcp input from service to honeyfarm
        self.permit_tcp_host1_host2(parser, t.dmz_service.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.dmz_service1.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)
        # PERMIT tcp input from gateway and elk to heralding
        self.permit_tcp_host1_host2(parser, t.gw10.get_ip_addr(), t.dmz_host.get_ip_addr(), t.dmz_host.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.elk_if2.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)

        self.permit_tcp_host1_host2(parser, t.gw12.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.gw10.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)

        #self.permit_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.dmz_service1.get_ip_addr(), t.dmz_service1.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.dmz_service.get_ip_addr(), t.dmz_service.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), datapath)


        self.permit_tcp_dstIP_dstPORT(parser, t.dmz_service.get_ip_addr(), t.dmz_service.get_ovs_port(), 22, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.dmz_service.get_ip_addr(), t.dmz_service.get_ovs_port(), 23, datapath)

        self.permit_tcp_dstIP_dstPORT(parser, t.dmz_service1.get_ip_addr(), t.dmz_service1.get_ovs_port(), 22, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.dmz_service1.get_ip_addr(), t.dmz_service1.get_ovs_port(), 23, datapath)

         # PERMIT tcp input to honeyfarm
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), 2022, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), 3022, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), 22, datapath)
        self.permit_tcp_dstIP_dstPORT(parser, t.ti_host_dmz.get_ip_addr(), t.ti_host_dmz.get_ovs_port(), 23, datapath)


        

        self.forward_to_controller(parser, t.dmz_heralding.get_ip_addr(),datapath)


        #self.drop_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.heralding.get_ip_addr(), datapath)
        #self.drop_icmp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.heralding.get_ip_addr(), datapath)
        #self.drop_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.service.get_ip_addr(), datapath)
        #self.drop_icmp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.service.get_ip_addr(), datapath)    
        #self.drop_tcp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.host.get_ip_addr(), datapath)
        #self.drop_icmp_host1_host2(parser, t.dmz_host.get_ip_addr(), t.host.get_ip_addr(), datapath)             
     


    def send_set_async(self, datapath):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        packet_in_mask = 1 << ofp.OFPR_ACTION | 1 << ofp.OFPR_INVALID_TTL | 1 << ofp.OFPR_NO_MATCH
        port_status_mask = (1 << ofp.OFPPR_ADD
                            | 1 << ofp.OFPPR_DELETE
                            | 1 << ofp.OFPPR_MODIFY)
        flow_removed_mask = (1 << ofp.OFPRR_IDLE_TIMEOUT
                            | 1 << ofp.OFPRR_HARD_TIMEOUT
                            | 1 << ofp.OFPRR_DELETE
                            | 1 << ofp.OFPRR_GROUP_DELETE)

        req = ofp_parser.OFPSetAsync(datapath,
                                    [packet_in_mask, packet_in_mask],
                                    [port_status_mask, port_status_mask],
                                    [flow_removed_mask, flow_removed_mask])
        datapath.send_msg(req)

    # Funzione per installare una regola nello switch in modo che ogni pacchetto con ip_dst indicato venga inoltrato al controller
    def forward_to_controller(self,parser, ip_dst,datapath):
        
        ofproto = datapath.ofproto
        out_port= ofproto.OFPP_CONTROLLER

        match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=ip_dst)
        actions = [parser.OFPActionOutput(out_port,ofproto.OFPCML_NO_BUFFER)]

        self.add_flow(datapath, 100, match, actions, 0)    

    def permit_eth_dstMAC(self, parser, eth_dst, ovs_port_dest, datapath):
        actions = [parser.OFPActionOutput(ovs_port_dest)]
        match = parser.OFPMatch(eth_dst=eth_dst)
        self.add_flow(datapath, 200, match, actions, 0)

    def drop_arp_srcIP_srcMAC(self, parser, arp_spa, arp_sha, datapath, op_code):
        '''drop_arp'''
        actions = []
        match = parser.OFPMatch(
            eth_type=0x0806, arp_op=op_code, arp_spa=arp_spa, arp_sha=arp_sha)
        self.add_flow(datapath, 100, match, actions, 0)

    def drop_icmp_srcIP_srcMAC_dstIP(self, parser, ipv4_src, eth_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, eth_src=eth_src, ipv4_dst=ipv4_dst,
            ip_proto=1)
        self.add_flow(datapath, 100, match, actions, 0)    
    
    def drop_icmp_srcIP_srcPORT_dstIP(self, parser, ipv4_src, port_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, in_port=port_src, ipv4_dst=ipv4_dst,
            ip_proto=1)     
        self.add_flow(datapath, 100, match, actions, 0)     

    def drop_tcp_srcIP_srcMAC_dstIP(self, parser, ipv4_src, eth_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, eth_src=eth_src, ipv4_dst=ipv4_dst,
            ip_proto=6)
        self.add_flow(datapath, 100, match, actions, 0)   

    def drop_tcp_srcIP_srcPORT_dstIP(self, parser, ipv4_src, port_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, in_port=port_src, ipv4_dst=ipv4_dst,
            ip_proto=6)     
        self.add_flow(datapath, 100, match, actions, 0)   
    
    def drop_tcp_dstIP(self, parser, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=ipv4_dst, ip_proto=6)
        self.add_flow(datapath, 100, match, actions, 0)

    def permit_tcp_host1_host2(self, parser, ipv4_src, ipv4_dst, ovs_port_dest, datapath):
        actions = [parser.OFPActionOutput(ovs_port_dest)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_src, ipv4_dst=ipv4_dst, ip_proto=6)  
        self.add_flow(datapath, 300, match, actions, 0) 

    def permit_tcp_dstIP_dstPORT(self, parser, ipv4_dst, ovs_port_dest, port_dest, datapath):
        actions = [parser.OFPActionOutput(ovs_port_dest)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_dst=ipv4_dst, tcp_dst=port_dest, ip_proto=6)  
        self.add_flow(datapath, 200, match, actions, 0) 
    
    def drop_tcp_dstIP_dstPORT(self, parser, ipv4_dst, port_dest, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_dst=ipv4_dst, tcp_dst=port_dest, ip_proto=6)
        self.add_flow(datapath, 200, match, actions, 0)
    
    def drop_icmp_host1_host2(self, parser, ipv4_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_src, ipv4_dst=ipv4_dst, ip_proto=1)
        self.add_flow(datapath, 300, match, actions, 0)       

    def drop_tcp_host1_host2(self, parser, ipv4_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_src, ipv4_dst=ipv4_dst, ip_proto=6)
        self.add_flow(datapath, 300, match, actions, 0)  

    # PROACTIVE MTD PORT HOPPING
    def redirect_protocol_syn(self, parser, datapath, port):  
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), port, datapath)
        
        actions = [parser.OFPActionSetField(eth_dst=t.heralding.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding.get_ip_addr()),
                   parser.OFPActionOutput(t.heralding.get_ovs_port())]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=t.service.get_ip_addr(), ip_proto=6, tcp_dst=port)
        self.add_flow_with_hard(datapath, 1000, match, actions, 4)

    def change_heralding_src_protocol(self, parser, datapath, port):
        ofproto = datapath.ofproto
        actions = [parser.OFPActionSetField(eth_src=t.service.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(ofproto.OFPP_NORMAL)]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding.get_ip_addr(), 
                                eth_src=t.heralding.get_MAC_addr(), ip_proto=6, tcp_src=port)
        self.add_flow_with_hard(datapath, 1000, match, actions, 5)


    def redirect_traffic (self, dpid,src_ip,tcp_port,source,gw,subnet,br_dpid):
        port_index = map.index_port_mapping.get(tcp_port,None)
  
        decoy_index = u.find_free_honeypot_by_service(man.sb, man.sm, port_index)


        if decoy_index is None and tcp_port != "23":
            print("Creazione nuovo honeypot heralding")
            host = t.ti_host1
            self.create_new_honeypot(host)
            decoy_index = u.find_free_honeypot_by_service(man.sb, man.sm, port_index)
        elif decoy_index is None and tcp_port == "23": 
            print("Creazione nuovo host cowrie")
            self.create_new_host_cowrie()
            decoy_index = u.find_free_honeypot_by_service(man.sb, man.sm, port_index)
            if(decoy_index) is None:
                print("Non è stato possibile creare un nuovo honeypot")
                return
        decoy = f.index_to_decoy_mapping.get (decoy_index,None)
        print("L'honeypot libero per il servizio ", tcp_port, "è :", decoy.get_name())

        destination_port = man.ports[decoy_index][port_index]
        man.sb[decoy_index][port_index] = 1 
        
        print("Redirection dell'utente: ",src_ip, "del service:", source.get_ip_addr(), "All'honeypot: ", decoy.get_ip_addr(), "da porta: ", tcp_port, "to: ", destination_port)
        t.host_redirected.append(src_ip)
        self.redirect_to(br_dpid,src_ip,tcp_port,source,decoy,gw,destination_port)
        self.change_decoy_src(br_dpid, src_ip,subnet,decoy,tcp_port,gw,source,destination_port)

    def redirect_traffic_dmz (self, dpid,src_ip,tcp_port,source,gw,subnet,br_dpid):
        port_index = dmz_map.index_port_mapping.get(tcp_port,None)
  
        decoy_index = u.find_free_honeypot_by_service(man_dmz.sb, man_dmz.sm, port_index)
        print("DMZ")


        if decoy_index is None and tcp_port != "23":
            print("Creazione nuovo honeypot heralding in dmz")
            host = t.ti_host_dmz
            self.create_new_honeypot(host)
            decoy_index = u.find_free_honeypot_by_service(man_dmz.sb, man_dmz.sm, port_index)
        elif decoy_index is None and tcp_port == "23": 
            print("Creazione nuovo host cowrie")
            #TO DO
            #self.create_new_host_cowrie()
            #decoy_index = u.find_free_honeypot_by_service(man.sb, man.sm, port_index)

            if(decoy_index) is None:
                print("Non è stato possibile creare un nuovo honeypot")
                return
        decoy = f.index_to_decoy_mapping_dmz.get (decoy_index,None)
        print("L'honeypot libero per il servizio ", tcp_port, "è :", decoy.get_name())

        destination_port = man_dmz.ports[decoy_index][port_index]
        man_dmz.sb[decoy_index][port_index] = 1 
        
        print("Redirection dell'utente: ",src_ip, "del service:", source.get_ip_addr(), "All'honeypot: ", decoy.get_ip_addr(), "da porta: ", tcp_port, "to: ", destination_port)
        t.host_redirected.append(src_ip)
        self.redirect_to(br_dpid,src_ip,tcp_port,source,decoy,gw,destination_port)
        self.change_decoy_src(br_dpid, src_ip,subnet,decoy,tcp_port,gw,source,destination_port)
    
    def create_new_honeypot(self,host):
        index = max(man.index_honeypot.values()) + 1
        #IL NOME SCELTO SARA DEL TIPO "heralding5"
        name ="heralding"+str(index)
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

    def create_new_honeypot_dmz(self,host):
        index = max(man_dmz.index_honeypot.values()) + 1
        #IL NOME SCELTO SARA DEL TIPO "heralding5"
        name ="heralding"+str(index)
        new_ssh_port= f.find_free_port(man_dmz.ports_host1,4000)
        man.ports_host1.append(new_ssh_port)
        new_ftp_port= f.find_free_port(man_dmz.ports_host1,4000)
        man.ports_host1.append(new_ftp_port)
        new_socks_port= f.find_free_port(man_dmz.ports_host1,4000)
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

    def create_new_host_cowrie(self):
        index = max(man.index_host.values()) + 2
        
        #IL NOME SCELTO SARA DEL TIPO "ti_host3"
        name ="ti_host"+str(index)

        print(name)


        s_hp = [1, 1, 0, 0]
        ports_hp = [22, 23, 0, 0]
        subnet = "10.1.4.0/24"
        
        mac = t.find_free_mac_address()
        ip_address = t.find_free_ip_address(subnet)
        host = f.add_new_host(name,subnet,mac,ip_address)
        #UNA VOLTA CREATO L'HOST AGGIUNGO UN HONEYPOT COWRIE A QUELL HOST

        index_honeypot = max(man.index_honeypot.values()) + 1
        #IL NOME SCELTO SARA DEL TIPO "heralding5"
        name_honeypot ="cowrie"+str(index_honeypot)
        # Crea un nuovo oggetto Honeypot
        new_honeypot = Honeypot(name_honeypot, host.get_ip_addr(), host.get_MAC_addr(), host.get_ovs_port(), host.get_netmask())
        # Lo aggiunge alla lista di tutti gli honeypot attivi
        t.honeypots_list.append(new_honeypot)

        # Aggiorna dizionario decoy_mapping aggiungendo una nuova entry con chiave il nome dell'honeypot e valore l'ultimo honeypot nella lista
        map.decoy_mapping[new_honeypot.get_name()] = t.honeypots_list[-1]


        # Aggiorna dizionario index_mapping aggiungendo una nuova entry con chiave il valore massimo delle chiavi +1 e valore l'ultimo honeypot nella lista
        new_key = max(f.index_to_decoy_mapping.keys()) + 1
        f.index_to_decoy_mapping[new_key] = t.honeypots_list[-1]

        man.add_new_honeypot_ti_management(new_honeypot,host,s_hp,ports_hp)

        print("Nuovo host creato:", t.hosts_list[-1].get_name(), "con ip: ", t.hosts_list[-1].get_ip_addr())
        print("Nuovo Honeypot creato:", t.honeypots_list[-1].get_name(), "con ip: ", t.honeypots_list[-1].get_ip_addr())

        print("Matrice H", man.h)
        print("Matrice SM", man.sm)
        print("Matrice ports", man.ports)
        print("Matrice sdh", man.sdh)
        print("Matrice busy", man.sb)
    

    def redirect_to(self, br_dpid, src_ip, tcp_port, source, destination, gw,destination_port):
        datapath = self.switches.get(br_dpid)
        parser = datapath.ofproto_parser
        self.permit_tcp_host1_host2(parser, src_ip, source.get_ip_addr(), source.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, source.get_ip_addr(), destination.get_ip_addr(), destination.get_ovs_port(), datapath)
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

    def change_decoy_src(self, br_dpid, src_ip, subnet, decoy, tcp_port,gw,destination,destination_port):
        datapath = self.switches.get(br_dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=destination.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=destination.get_MAC_addr()),
                   parser.OFPActionSetField(tcp_src=int(tcp_port)),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=decoy.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src= gw.get_MAC_addr(), ip_proto=6, tcp_src=int(destination_port))                
        self.add_flow(datapath, 1000, match, actions, 1)


    