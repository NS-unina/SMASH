#!/bin/sh

ip route add 10.1.11.0/24 via 10.1.4.1 dev enp0s8
ip route add 10.1.4.0/24 via 10.1.5.1 dev enp0s8
ip route add 10.1.10.0/24 via 10.1.11.1 dev enp0s9
