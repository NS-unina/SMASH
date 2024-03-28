#!/bin/sh

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller_lan2 \
   external_ids:container_iface=eth1 | grep -q "c21_l"; then
        sudo ./my-ovs-docker del-port br0_lan2 eth1 controller_lan2
fi

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller_lan2 \
   external_ids:container_iface=eth2 | grep -q "c22_l"; then
        sudo ./my-ovs-docker del-port br1_lan2 eth2 controller_lan2
fi

# Remember to change containers name if they change
sudo docker stop controller_lan2
sudo docker start controller_lan2

sudo ./my-ovs-docker add-port br0_lan2 eth1 controller_lan2 c21 70 --ipaddress=10.2.5.100/24
sudo ovs-vsctl -- set port c21_l tag=23
sudo iptables -t nat -A POSTROUTING -o c21_l -j MASQUERADE
sudo ./my-ovs-docker add-port br1_lan2 eth2 controller_lan2 c22 71 --ipaddress=10.2.11.100/24
sudo ovs-vsctl -- set port c22_l tag=27
sudo iptables -t nat -A POSTROUTING -o c22_l -j MASQUERADE

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_host \
   external_ids:container_iface=eth1 | grep -q "h1_l"; then
        sudo ./my-ovs-docker del-port br0_lan2 eth1 int_host
fi


if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_host_lan2 \
   external_ids:container_iface=eth1 | grep -q "h21_l"; then
        sudo ./my-ovs-docker del-port br0_lan2 eth1 int_host_lan2
fi

sudo docker stop int_host_lan2
sudo docker start int_host_lan2

sudo ./my-ovs-docker add-port br0_lan2 eth1 int_host_lan2 h21 39 --ipaddress=10.2.3.10/24 --macaddress=08:00:27:b6:d0:46
sudo ovs-vsctl -- set port h21_l tag=21
sudo iptables -t nat -A POSTROUTING -o h21_l -j MASQUERADE





