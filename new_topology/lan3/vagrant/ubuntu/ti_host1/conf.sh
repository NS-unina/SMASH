#!/bin/sh

sudo ip route add 10.3.3.0/24 via 10.3.4.1 dev enp0s8
sudo ip route add 10.3.5.0/24 via 10.3.4.1 dev enp0s8


