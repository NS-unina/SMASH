#!/bin/sh

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller \
   external_ids:container_iface=eth1 | grep -q "c4_l"; then
        sudo ./my-ovs-docker del-port br0_lan4 eth1 controller
fi


# Remember to change containers name if they change
sudo docker stop controller
sudo docker start controller

sudo ./my-ovs-docker add-port br0_lan4 eth1 controller c4 40 --ipaddress=10.4.3.100/24
sudo ovs-vsctl -- set port c4_l tag=40
sudo iptables -t nat -A POSTROUTING -o c1_l -j MASQUERADE


