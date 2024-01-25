#!/bin/bash

# Funzione per generare un nome univoco per il tap
generate_tap_name() {
  echo "tap_$(uuidgen)" | cut -c1-15
}

generate_vm_name() {
  echo "int_heralding_$(uuidgen)" | cut -c1-20
}

# Funzione per generare un numero di porta OpenFlow unico
generate_ofport() {
  local bridge_name=$1
  local ofport=$(sudo ovs-ofctl show $bridge_name | awk '/addr:/ {print $2}' | cut -d'(' -f1 | tr -cd '0-9')
  ((ofport++))
  echo "$ofport"
}
# Funzione per generare un MAC address univoco
generate_mac_address() {
  echo "080027$(dd if=/dev/urandom bs=1 count=3 2>/dev/null | od -An -t x1 | tr -d ' \n' | sed 's/../&/g')"
}
# Funzione per creare un tap
create_tap() {
  local tap_name=$1
  local bridge_name=$2
  local tag=$3
  local ofport=$4

  if sudo ovs-vsctl show | grep -w -q "Port $tap_name"; then
    sudo ovs-vsctl del-port $tap_name
  fi

  if ip a | grep -q "$tap_name:." | grep -q "state UP"; then
    :
  elif ip a | grep "$tap_name:" | grep -q "state DOWN"; then
    sudo ip link set $tap_name up
    sudo ovs-vsctl add-port $bridge_name $tap_name tag=$tag -- set interface $tap_name ofport=$ofport
  else
    sudo ip tuntap add name $tap_name mode tap
    sudo ip link set $tap_name up
    sudo ovs-vsctl add-port $bridge_name $tap_name tag=$tag -- set interface $tap_name ofport=$ofport
  fi
}
