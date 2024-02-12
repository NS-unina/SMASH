#!/bin/bash

# Funzione per generare un nome univoco per il tap
generate_interface_name() {
  echo "t$(uuidgen)" | cut -c1-5
}

generate_container_name() {
  echo "heralding_$(uuidgen)" | cut -c1-16
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
generate_mac_address_container() {
  echo "08:00:27:$(dd if=/dev/urandom bs=1 count=3 2>/dev/null | od -An -t x1 | tr -d ' \n' | sed 's/../&:/g;s/:$//')"
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

find_free_ip3() {
    local subnet="$1"
    local occupied_file="$2"
    local ip_list=()

    # Carica gli indirizzi IP occupati dal file
    if [ -e "$occupied_file" ]; then
        readarray -t ip_list < "$occupied_file"
    fi

    # Cerca un indirizzo IP libero
    for i in {2..254}; do
        local ip="${subnet%.*}.${i}"
        if [[ ! " ${ip_list[@]} " =~ " ${ip} " ]]; then
            echo "$ip"
            return
        fi
    done
}

find_free_port() {
    local occupied_file="$1"
    local port_list=()

    # Carica i numeri di porta occupati dal file
    if [ -e "$occupied_file" ]; then
        readarray -t port_list < "$occupied_file"
    fi

    # Cerca un numero di porta libero
    for port in {3200..4000}; do
        if [[ ! " ${port_list[@]} " =~ " ${port} " ]]; then
            echo "$port"
            return
        fi
    done
}
