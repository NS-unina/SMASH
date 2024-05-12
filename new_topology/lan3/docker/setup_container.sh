#!/bin/sh

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller_lan3 \
   external_ids:container_iface=eth1 | grep -q "c31_l"; then
        sudo ./my-ovs-docker del-port br0_lan3 eth1 controller_lan3
fi

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller_lan3 \
   external_ids:container_iface=eth2 | grep -q "c32_l"; then
        sudo ./my-ovs-docker del-port br1_lan3 eth2 controller_lan3
fi

# Remember to change containers name if they change
sudo docker stop controller_lan3
sudo docker start controller_lan3

sudo ./my-ovs-docker add-port br0_lan3 eth1 controller_lan2 c31 80 --ipaddress=10.3.5.100/24
sudo ovs-vsctl -- set port c31_l tag=33
sudo iptables -t nat -A POSTROUTING -o c31_l -j MASQUERADE
sudo ./my-ovs-docker add-port br1_lan3 eth2 controller_lan3 c23 81 --ipaddress=10.3.11.100/24
sudo ovs-vsctl -- set port c23_l tag=37
sudo iptables -t nat -A POSTROUTING -o c32_l -j MASQUERADE

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_host_lan3 \
   external_ids:container_iface=eth1 | grep -q "h31_l"; then
        sudo ./my-ovs-docker del-port br0_lan3 eth1 int_host_lan3
fi

sudo docker stop int_host_lan2
sudo docker start int_host_lan2

sudo ./my-ovs-docker add-port br0_lan3 eth1 int_host_lan3 h31 49 --ipaddress=10.2.3.10/24 --macaddress=08:00:27:b6:d0:49
sudo ovs-vsctl -- set port h31_l tag=31
sudo iptables -t nat -A POSTROUTING -o h31_l -j MASQUERADE





