#!/bin/sh

sudo ip route add 10.1.3.0/24 via 10.1.4.1 dev enp0s8
sudo ip route add 10.1.5.0/24 via 10.1.4.1 dev enp0s8
sudo ip route add 10.1.10.0/24 via 10.1.4.1 dev enp0s8
sudo ip route add 10.1.11.0/24 via 10.1.4.1 dev enp0s8
