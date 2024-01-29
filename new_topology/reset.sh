#!/bin/bash
source functions.sh

bridges=("br0_lan1" "br1_lan1" "br_lan2" "br_lan3"  "br_wan")
taps=("tap1" "tap2" "tap3" "tap4" "tap7" "tap5" "tap6" "tap10" "tap12" "tap13" "tap11")
interfaces=("c1_l" "c2_l" "h1_l" "h2_l" "s1_l" "h3_l")

delete_bridge "${bridges[@]}"

delete_interface "${taps[@]}"

delete_interface "${interface[@]}"


sudo netplan apply

# if ifconfig | grep -q -A2 "wlp0s20f3:*" | grep -q "inet "; then
#    echo "wlp0s20f3 still exists"
# else
#    sudo ifconfig wlp0s20f3 10.1.92.106/24 up
#    sudo route add default gw 10.1.92.68 wlp0s20f3
# fi
# sleep 5
