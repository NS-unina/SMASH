#!/bin/sh

ip route add 10.1.0.0/16 via 10.4.3.1 dev eth1
ip route add 10.2.0.0/16 via 10.4.3.1 dev eth1
ip route add 10.3.0.0/16 via 10.4.3.1 dev eth1
