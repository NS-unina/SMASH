#!/bin/sh

ip route add 10.2.3.0/24 via 10.2.5.1 dev enp0s8
ip route add 10.2.4.0/24 via 10.2.5.1 dev enp0s8
ip route add 10.2.10.0/24 via 10.2.11.1 dev enp0s9
