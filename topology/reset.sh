#!/bin/bash
source functions.sh

bridges=("br0" "br1")
taps=("tap1" "tap2" "tap3" "tap4" "tap5")
interfaces=("c1_l" "c2_l" "h1_l" "h2_l" "s1_l" "h3_l")

delete_bridge "${bridges[@]}"

delete_interface "${taps[@]}"

delete_interface "${interface[@]}"

sudo netplan apply

