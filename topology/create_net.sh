#!/bin/bash
source functions.sh


vlans1=("vlan11" "vlan12" "vlan13" "vlan15" "vlan16")
vlans2=("vlan21" "vlan22" "vlan23")
vlans3=("vlan31" "vlan32" "vlan33")


setup_ovs_bridge "br0_lan1" "br1_lan1" "br_lan2" "br_lan3" "br_wan"

create_ovs_bridge "br0_lan1" "3a:4d:a7:05:2a:45"
create_ovs_bridge "br1_lan1" "3a:4d:a7:05:2a:46"
create_ovs_bridge "br_lan2" "3a:4d:a7:05:2a:49"
create_ovs_bridge "br_lan3" "3a:4d:a7:05:2a:47"
create_ovs_bridge "br_wan" "3a:4d:a7:05:2a:48"

# sudo ovs-vsctl set bridge br_lan1 other-config:datapath-id=209326269119040
# sudo ovs-vsctl set bridge br_lan2 other-config:datapath-id=187971798259276

#209544804549707
#33227011233353

create_vlan "vlan11" "br0_lan1" "1" "10.1.3.1/24" "9e:c3:c6:49:0e:e8" "1"
create_vlan "vlan12" "br0_lan1" "2" "10.1.4.1/24" "16:67:1f:3f:86:a7" "5"
create_vlan "vlan13" "br0_lan1" "3" "10.1.5.1/24" "fe:46:67:35:0d:d1" "7"

echo "Connect br0_lan1 to controller 10.1.5.100:6633"
sudo ovs-vsctl set-controller br0_lan1 tcp:10.1.5.100:6633

create_vlan "vlan15" "br1_lan1" "5" "10.1.10.1/24" "8a:ae:02:40:8f:83" "10"
create_vlan "vlan16" "br1_lan1" "6" "10.1.11.1/24" "ea:6a:20:a0:96:10" "11"

echo "Connect br1_lan1 to controller 10.1.11.100:6633"
sudo ovs-vsctl set-controller br1_lan1 tcp:10.1.11.100:6633


create_vlan "vlan21" "br_lan2" "10" "10.2.3.1/24" "8a:ae:02:40:8f:93" "40"
create_vlan "vlan22" "br_lan2" "11" "10.2.4.1/24" "ea:6a:20:a0:96:11" "41"
create_vlan "vlan23" "br_lan2" "11" "10.2.5.1/24" "ea:6a:20:a0:96:12" "42"

echo "Connect br_lan2 to controller 10.2.5.100:6633"
sudo ovs-vsctl set-controller br_lan2 tcp:10.2.5.100:6633

create_vlan "vlan31" "br_lan3" "20" "10.3.3.1/24" "8a:ae:02:40:8f:94" "50"
create_vlan "vlan32" "br_lan3" "21" "10.3.4.1/24" "ea:6a:20:a0:96:14" "51"
create_vlan "vlan33" "br_lan3" "22" "10.3.5.1/24" "ea:6a:20:a0:96:17" "52"

echo "Connect br_lan3 to controller 10.3.5.100:6633"
sudo ovs-vsctl set-controller br_lan3 tcp:10.3.5.100:6633

create_vlan_forward_rules "${vlans1[@]}"
create_vlan_forward_rules "${vlans2[@]}"
create_vlan_forward_rules "${vlans3[@]}"

# patch wan lan1
sudo ovs-vsctl -- add-port br0_lan1 patch0 -- set interface patch0 type=patch ofport=45 options:peer=patch1 \
-- add-port br_wan patch1 -- set interface patch1 type=patch ofport=46 options:peer=patch0

sudo ovs-vsctl -- add-port br0_lan1 patch10 -- set interface patch10 type=patch ofport=55 options:peer=patch11 \
-- add-port br1_lan1 patch11 -- set interface patch11 type=patch ofport=56 options:peer=patch10

sudo ovs-vsctl -- add-port br1_lan1 patch12 -- set interface patch12 type=patch ofport=57 options:peer=patch13 \
-- add-port br0_lan1 patch13 -- set interface patch13 type=patch ofport=58 options:peer=patch12

sudo ovs-vsctl -- add-port br1_lan1 patch2 -- set interface patch2 type=patch ofport=47 options:peer=patch3 \
-- add-port br_wan patch3 -- set interface patch3 type=patch ofport=48 options:peer=patch2

sudo ovs-vsctl -- add-port br_lan2 patch4 -- set interface patch4 type=patch ofport=49 options:peer=patch5 \
-- add-port br_wan patch5 -- set interface patch5 type=patch ofport=50 options:peer=patch4


sudo ovs-vsctl -- add-port br_lan3 patch6 -- set interface patch6 type=patch ofport=51 options:peer=patch7 \
-- add-port br_wan patch7 -- set interface patch7 type=patch ofport=52 options:peer=patch6

sudo iptables -t nat -A POSTROUTING -o patch0 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch1 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch2 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch3 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch4 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch5 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch6 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch7 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch10 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch11 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch12 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch13 -j MASQUERADE

