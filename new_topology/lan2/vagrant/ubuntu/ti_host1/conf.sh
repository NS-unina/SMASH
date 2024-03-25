#!/bin/sh

sudo ip route add 10.2.3.0/24 via 10.2.4.1 dev enp0s8
sudo ip route add 10.2.5.0/24 via 10.2.4.1 dev enp0s8


