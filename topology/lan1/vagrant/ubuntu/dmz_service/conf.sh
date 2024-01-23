#!/bin/sh

sudo ip route add 10.1.4.0/24 via 10.1.3.1 dev eth1
sudo ip route add 10.1.5.0/24 via 10.1.3.1 dev eth1
sudo ip route add 10.1.10.0/24 via 10.1.3.1 dev eth1
sudo ip route add 10.1.11.0/24 via 10.1.3.1 dev eth1
