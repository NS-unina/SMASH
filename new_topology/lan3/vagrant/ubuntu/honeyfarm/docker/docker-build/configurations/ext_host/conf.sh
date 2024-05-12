#!/bin/sh

ip route add 10.2.11.0/24 via 10.2.10.2 dev eth1
ip route add 10.2.3.0/24 via 10.2.10.2 dev eth1
ip route add 10.2.4.0/24 via 10.2.10.2 dev eth1
ip route add 10.2.5.0/24 via 10.2.10.2 dev eth1

ip route add 10.2.0.0/16 via 10.2.10.2 dev eth1
