#!/bin/bash
source functions.sh

echo "Restoring Network ..."

vlans=("vlan1" "vlan2" "vlan3")
taps=("tap1" "tap2" "tap3" "tap4" "tap5")

#TAP create_tap(tap_name, bridge_name, tag, ofport)
create_tap "tap1" "br0" "1" "2"
create_tap "tap2" "br0" "1" "3"
create_tap "tap3" "br0" "2" "4"
create_tap "tap4" "br0" "2" "6"
create_tap "tap5" "br0" "3" "8"

# VLAN setup_vlan_interface(vlan_name, ip_address, mac_address)
setup_vlan_interface "vlan1" "192.168.10.1/24" "9e:c3:c6:49:0e:e8"
setup_vlan_interface "vlan2" "192.168.11.1/24" "16:67:1f:3f:86:a7"
setup_vlan_interface "vlan2" "192.168.12.1/24" "fe:46:67:35:0d:d1"


create_masquerade_rules "${taps[@]}" "${vlans[@]}"
create_vlan_forward_rules "${vlans[@]}"

