#!/bin/bash
# Utilizzo delle funzioni
source utils.sh

subnet=$1
mac_tap=$2
vm_name=$3
ip_address=$4
free_port=$5
subnet1="10.1.3.0/24"
subnet2="10.1.4.0/24"

occupied_ips="/home/claudio/Honey-MTD-2/new_topology/lan1/occupied_ips"
occupied_ports="/home/claudio/Honey-MTD-2/new_topology/lan1/occupied_ports"

if [ "$subnet" == "$subnet1" ]; then
    comment="#Subnet 1"
    gateway="10.1.3.1"
    tag="1"
    bridge="br0_lan1"
    routes="[\"10.1.4.0/24\", \"10.1.5.0/24\", \"10.1.10.0/24\", \"10.1.11.0/24\"]"
elif [ "$subnet" == "$subnet2" ]; then
    gateway="10.1.4.1"
    comment="#Subnet 2"
    bridge="br0_lan1"
    tag="2"
    routes="[\"10.1.3.0/24\", \"10.1.5.0/24\", \"10.1.10.0/24\", \"10.1.11.0/24\"]"
else
    echo "Inserisci una subnet valida"
    exit 1
fi

vagrant_file="/home/claudio/Honey-MTD-2/new_topology/lan1/vagrant/ubuntu/Vagrantfile"
tap_name=$(generate_tap_name)
ofport=$(generate_ofport "$bridge")
#mac_tap=$(generate_mac_address)
#vm_name=$(generate_vm_name)
#ip_address=$(find_free_ip3 "$subnet" "$occupied_ips")
#free_port=$(find_free_port "$occupied_ports")
#echo "$ip_address" >> "$occupied_ips"
#echo "$free_port" >> "$occupied_ports"
#TAP create_tap(tap_name, bridge_name, tag, ofport)
create_tap "$tap_name" "$bridge" "$tag" "$ofport"

tap_ofport=$(sudo ovs-vsctl get Interface "$tap_name" ofport)

config_string="    deploy_honeyfarm_runtime(config, \"$vm_name\", \"ubuntu/focal64\", \"2048\",\"ext_cowrie\", 22, $free_port,\"ssh\", \"$tap_name\", \"$mac_tap\", \"$ip_address\", $routes,\"$gateway\")"

sed -i "/# HONEYPOT FARM/a\\
${config_string}" "${vagrant_file}"

cd vagrant/ubuntu

vagrant up "$vm_name" > /dev/null 2>&1

echo "$tap_ofport"


