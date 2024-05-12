#!/bin/sh

ip route add 10.2.4.0/24 via 10.2.3.1 dev eth1
ip route add 10.2.5.0/24 via 10.2.3.1 dev eth1


ip route add 10.1.0.0/16 via 10.2.3.1 dev eth1

