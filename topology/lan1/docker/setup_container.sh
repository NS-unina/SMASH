#!/bin/sh

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller \
   external_ids:container_iface=eth1 | grep -q "c1_l"; then
        sudo ./my-ovs-docker del-port br_lan1 eth1 controller
fi

# Remember to change containers name if they change
sudo docker stop controller
sudo docker start controller

sudo ./my-ovs-docker add-port br_lan1 eth1 controller c1 20 --ipaddress=10.1.5.100/24
sudo ovs-vsctl -- set port c1_l tag=3
sudo iptables -t nat -A POSTROUTING -o c1_l -j MASQUERADE

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_host \
   external_ids:container_iface=eth1 | grep -q "h1_l"; then
        sudo ./my-ovs-docker del-port br_lan1 eth1 int_host
fi

sudo docker stop int_host
sudo docker start int_host

sudo ./my-ovs-docker add-port br_lan1 eth1 int_host h1 15 --ipaddress=10.1.3.10/24 --macaddress=08:00:27:b6:d0:66
sudo ovs-vsctl -- set port h1_l tag=1
sudo iptables -t nat -A POSTROUTING -o h1_l -j MASQUERADE



if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_ssh_server \
   external_ids:container_iface=eth1 | grep -q "h3_l"; then
        sudo ./my-ovs-docker del-port br_lan1 eth1 int_ssh_server
fi

sudo docker stop int_ssh_server
sudo docker start int_ssh_server

sudo ./my-ovs-docker add-port br_lan1 eth1 int_ssh_server h3 16 --ipaddress=10.1.3.13/24 --macaddress=08:00:27:b6:d0:69
sudo ovs-vsctl -- set port h3_l tag=1
sudo iptables -t nat -A POSTROUTING -o h3_l -j MASQUERADE

