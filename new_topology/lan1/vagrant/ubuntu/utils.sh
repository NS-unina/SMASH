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

find_free_ip() {
  local subnet=$1

  # Estrai l'indirizzo della rete e il prefisso dalla sottorete
  network=$(echo "$subnet" | cut -d '/' -f 1)
  prefix=$(echo "$subnet" | cut -d '/' -f 2)

  # Calcola il numero massimo di host possibili nella sottorete
  max_hosts=$((2**(32 - prefix) - 2))

  # Trova gli IP attualmente in uso nella sottorete
  used_ips=$(arp-scan --localnet | grep -oP '\(\K[^)]+')

  # Loop per trovare il primo IP libero
  for i in $(seq 1 $max_hosts); do
    test_ip="$network.$i"

    # Controlla se l'IP è libero
    if ! echo "$used_ips" | grep -w "$test_ip" > /dev/null; then
      echo "$test_ip"
      return
    fi
  done

  echo "Nessun indirizzo IP libero trovato nella sottorete $subnet"
}
find_free_ip2() {
  subnet="$1"
  
  # Loop attraverso gli indirizzi IP nella subnet
  for i in {2..254}; do
    ip_address="${subnet%.*}.$i"
    
    # Utilizza ping per verificare se l'indirizzo IP è in uso
    if ! ping -c 1 -w 1 "$ip_address" &> /dev/null; then
      echo "$ip_address"
      return
    fi
  done

  echo "Nessun indirizzo IP libero trovato nella subnet $subnet"
  exit 1
}

