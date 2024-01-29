#!/bin/bash
source functions.sh


vlans1=("vlan11" "vlan12" "vlan13" "vlan16" "vlan17")
vlans2=("vlan21" "vlan22" "vlan23")

setup_ovs_bridge "br0_lan1" "br1_lan1" "br_lan2" "br_lan3" "br_wan"

create_ovs_bridge "br0_lan1" "3a:4d:a7:05:2a:45"
create_ovs_bridge "br1_lan1" "3a:4d:a7:05:2a:46"
create_ovs_bridge "br_lan2" "3a:4d:a7:05:2a:49"
create_ovs_bridge "br_lan3" "3a:4d:a7:05:2a:47"
create_ovs_bridge "br_wan" "3a:4d:a7:05:2a:48"

# sudo ovs-vsctl set bridge br0 other-config:datapath-id=209326269119040
# sudo ovs-vsctl set bridge br1 other-config:datapath-id=187971798259276

#209544804549707
#33227011233353

create_vlan "vlan11" "br0_lan1" "1" "10.1.3.1/24" "9e:c3:c6:49:0e:e8" "1"
create_vlan "vlan12" "br0_lan1" "2" "10.1.4.1/24" "16:67:1f:3f:86:a7" "5"
create_vlan "vlan13" "br0_lan1" "3" "10.1.5.1/24" "fe:46:67:35:0d:d1" "7"

echo "Connect br0_lan1 to controller 10.1.5.100:6633"
sudo ovs-vsctl set-controller br0_lan1 tcp:10.1.5.100:6633

create_vlan "vlan16" "br1_lan1" "10" "10.1.10.1/24" "8a:ae:02:40:8f:93" "40"
create_vlan "vlan17" "br1_lan1" "11" "10.1.11.1/24" "ea:6a:20:a0:96:11" "41"

echo "Connect br1 to controller 10.1.11.100:6633"
sudo ovs-vsctl set-controller br1_lan1 tcp:10.1.11.100:6633

#LAN2
create_vlan "vlan21" "br_lan2" "20" "10.2.3.1/24" "8a:ae:02:40:8f:93" "50"
create_vlan "vlan22" "br_lan2" "21" "10.2.4.1/24" "ea:6a:20:a0:96:11" "51"
create_vlan "vlan23" "br_lan2" "22" "10.2.5.1/24" "ea:6a:20:a0:96:12" "52"

echo "Connect br_lan2 to controller 10.2.5.100:6633"
sudo ovs-vsctl set-controller br_lan2 tcp:10.2.5.100:6633

create_vlan_forward_rules "${vlans1[@]}"
create_vlan_forward_rules "${vlans2[@]}"

sudo ovs-vsctl -- add-port br0_lan1 patch0 -- set interface patch0 type=patch ofport=45 options:peer=patch1 \
-- add-port br1_lan1 patch1 -- set interface patch1 type=patch ofport=46 options:peer=patch0

sudo iptables -t nat -A POSTROUTING -o patch0 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch1 -j MASQUERADE

