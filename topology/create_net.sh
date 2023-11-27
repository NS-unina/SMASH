#!/bin/bash
source functions.sh


vlans=("vlan1" "vlan2" "vlan3" "vlan10" "vlan11")

setup_ovs_bridge "br0" "br1"

create_ovs_bridge "br0" "3a:4d:a7:05:2a:45"
create_ovs_bridge "br1" "3a:4d:a7:05:2a:46"

# sudo ovs-vsctl set bridge br0 other-config:datapath-id=209326269119040
# sudo ovs-vsctl set bridge br1 other-config:datapath-id=187971798259276

#209544804549707
#33227011233353

create_vlan "vlan1" "br0" "1" "192.168.3.1/24" "9e:c3:c6:49:0e:e8" "1"
create_vlan "vlan2" "br0" "2" "192.168.4.1/24" "16:67:1f:3f:86:a7" "5"
create_vlan "vlan3" "br0" "3" "192.168.5.1/24" "fe:46:67:35:0d:d1" "7"

echo "Connect br0 to controller 192.168.5.100:6633"
sudo ovs-vsctl set-controller br0 tcp:192.168.5.100:6633

create_vlan "vlan10" "br1" "10" "192.168.10.1/24" "8a:ae:02:40:8f:93" "40"
create_vlan "vlan11" "br1" "11" "192.168.11.1/24" "ea:6a:20:a0:96:11" "41"

echo "Connect br1 to controller 192.168.11.100:6633"
sudo ovs-vsctl set-controller br1 tcp:192.168.11.100:6633

create_vlan_forward_rules "${vlans[@]}"

sudo ovs-vsctl -- add-port br0 patch0 -- set interface patch0 type=patch ofport=45 options:peer=patch1 \
-- add-port br1 patch1 -- set interface patch1 type=patch ofport=46 options:peer=patch0

sudo iptables -t nat -A POSTROUTING -o patch0 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch1 -j MASQUERADE

