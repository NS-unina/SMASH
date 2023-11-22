#!/bin/bash
source functions.sh


vlans=("vlan1" "vlan2" "vlan3")

setup_ovs_bridge "br0" "br1"
create_ovs_bridge "br0" "3a:4d:a7:05:2a:45"

#CREATE VLAN create_vlan(vlan_name,bridge_name,tag,ip,mac,of_port)
create_vlan "vlan1" "br0" "1" "192.168.10.1/24" "9e:c3:c6:49:0e:e8" "1"
create_vlan "vlan2" "br0" "2" "192.168.11.1/24" "16:67:1f:3f:86:a7" "5"
create_vlan "vlan3" "br0" "3" "192.168.12.1/24" "fe:46:67:35:0d:d1" "7"

#CONNECT BR TO CONTROLLER
echo "Connect br0 to controller 192.168.12.100:6633"
sudo ovs-vsctl set-controller br0 tcp:192.168.12.100:6633

create_vlan_forward_rules "${vlans[@]}"

