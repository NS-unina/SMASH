#!/bin/bash
source functions.sh

echo "Restoring Network ..."

vlans1=("vlan11" "vlan12" "vlan13" "vlan16" "vlan17")
vlans2=("vlan21" "vlan22" "vlan23" "vlan26" "vlan27")
taps1=("tap1" "tap2" "tap3" "tap4" "tap7" "tap5" "tap6" "tap10" "tap12" "tap13" "tap11" "tap18" )
taps2=("tap21" "tap22" "tap23" "tap26")

#TAP create_tap(tap_name, bridge_name, tag, ofport)
create_tap "tap1" "br0_lan1" "1" "2"
create_tap "tap2" "br0_lan1" "1" "3"
create_tap "tap3" "br0_lan1" "1" "4"
create_tap "tap4" "br0_lan1" "2" "6"
create_tap "tap7" "br0_lan1" "2" "13"
create_tap "tap5" "br0_lan1" "3" "8"
create_tap "tap6" "br0_lan1" "3" "9"
create_tap "tap15" "br0_lan1" "2" "25"
create_tap "tap10" "br1_lan1" "10" "2"
create_tap "tap12" "br1_lan1" "10" "20"
create_tap "tap13" "br1_lan1" "10" "21"
create_tap "tap11" "br1_lan1" "11" "13"
create_tap "tap18" "br1_lan1" "12" "18"

#LAN2
create_tap "tap21" "br0_lan2" "21" "31"
create_tap "tap22" "br0_lan2" "21" "32"
create_tap "tap23" "br0_lan2" "22" "33"
create_tap "tap26" "br1_lan2" "26" "36"

# VLAN setup_vlan_interface(vlan_name, ip_address, mac_address)
setup_vlan_interface "vlan11" "10.1.3.1/24" "9e:c3:c6:49:0e:e8"
setup_vlan_interface "vlan12" "10.1.4.1/24" "16:67:1f:3f:86:a7"
setup_vlan_interface "vlan13" "10.1.5.1/24" "fe:46:67:35:0d:d1"
setup_vlan_interface "vlan16" "10.1.10.1/24" "8a:ae:02:40:8f:93"
setup_vlan_interface "vlan17" "10.1.11.1/24" "ea:6a:20:a0:96:11"
setup_vlan_interface "vlan18" "10.1.12.1/24" "ea:6a:20:a0:46:12"

create_masquerade_rules "${taps1[@]}" "${vlans1[@]}"
create_vlan_forward_rules "${vlans1[@]}"

#LAN 2
setup_vlan_interface "vlan21" "10.2.3.1/24" "8a:ae:02:40:8f:96"
setup_vlan_interface "vlan22" "10.2.4.1/24" "ea:6a:20:a0:96:15"
setup_vlan_interface "vlan23" "10.2.5.1/24" "ea:6a:20:a0:96:17"
setup_vlan_interface "vlan26" "10.2.10.1/24" "ea:6a:20:a0:4f:93"
setup_vlan_interface "vlan27" "10.2.11.1/24" "ea:6a:20:a0:26:11"

create_masquerade_rules "${taps2[@]}" "${vlans2[@]}"
create_vlan_forward_rules "${vlans2[@]}"

# if sudo ovs-ofctl show br1 | grep -q "(wlp0s20f3)"; then
#    sudo ovs-vsctl del-port wlp0s20f3
# fi
# sudo ovs-vsctl add-port br1 wlp0s20f3 -- set interface wlp0s20f3 ofport=10
# sudo ifconfig wlp0s20f3 0
# sudo ifconfig br1 192.168.92.106/24 up
# sudo route add default gw 192.168.92.68 br1

# #sudo ifconfig br1 192.168.1.16/24 up
# #sudo route add default gw 192.168.1.1 br1
# sudo iptables -t nat -A POSTROUTING -o br1 -j MASQUERADE
# sudo iptables -t nat -A POSTROUTING -o wlp0s20f3 -j MASQUERADE
# sudo sed -i '1s/^/nameserver 8.8.8.8\n/' /etc/resolv.conf
