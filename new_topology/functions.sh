#!/bin/bash
setup_ovs_bridge() {
    local bridge_names=("$@")

    for bridge_name in "${bridge_names[@]}"; do
        if sudo ovs-vsctl show | grep -q "Bridge $bridge_name"; then
            sudo ovs-vsctl del-br $bridge_name
        fi
    done

    sleep 10

    echo "Start Network setup ..."
    echo "Enable IP forwarding"
    sudo sysctl -w net.ipv4.ip_forward=1
    echo "OVS setup"
}

create_vlan() {
    local vlan_name=$1
    local bridge_name=$2
    local tag=$3
    local ip_address=$4
    local mac_address=$5
    local of_port=$6

    echo "Subnet: $ip_address"

    sudo ovs-vsctl add-port $bridge_name $vlan_name -- set interface $vlan_name type=internal ofport=$of_port
    sudo ovs-vsctl set port $vlan_name tag=$tag
    sudo ifconfig $vlan_name $ip_address up
    sudo ifconfig $vlan_name hw ether $mac_address
    sudo iptables -t nat -A POSTROUTING -o $vlan_name -j MASQUERADE
}

create_ovs_bridge() {
    local bridge_name=$1
    local bridge_hwaddr=$2

    sudo ovs-vsctl add-br $bridge_name
    sudo ovs-vsctl set bridge $bridge_name other_config:hwaddr=$bridge_hwaddr
}


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

setup_vlan_interface() {
    local vlan_name=$1
    local ip_address=$2
    local mac_address=$3

    if ifconfig | grep -q -A2 "$vlan_name:*" | grep -q "inet "; then
        :
    else
        sudo ifconfig $vlan_name $ip_address up
        sudo ifconfig $vlan_name hw ether $mac_address
    fi
}

create_vlan_forward_rules() {
    local vlans=("$@")

    for ((i = 0; i < ${#vlans[@]}; i++)); do
        for ((j = i + 1; j < ${#vlans[@]}; j++)); do
            sudo iptables -A FORWARD -i "${vlans[i]}" -o "${vlans[j]}" -j ACCEPT
            sudo iptables -A FORWARD -i "${vlans[j]}" -o "${vlans[i]}" -j ACCEPT
        done
    done
}

create_masquerade_rules() {
    local tap_interfaces=("$1[@]")
    local vlan_interfaces=("$2[@]")

    for interface in "${tap_interfaces[@]}"; do
        sudo iptables -t nat -A POSTROUTING -o "$interface" -j MASQUERADE
    done

    for interface in "${vlan_interfaces[@]}"; do
        sudo iptables -t nat -A POSTROUTING -o "$interface" -j MASQUERADE
    done
}

delete_bridge() {
    local bridges=("$@")
    
    for bridge_name in "${bridges[@]}"; do
        if sudo ovs-vsctl show | grep -q "Bridge $bridge_name"; then
            sudo ovs-vsctl del-br $bridge_name
        fi
    done
}

delete_interface() {
    local interfaces=("$@")

    for interface_name in "${interfaces[@]}"; do
        if ip a | grep -q "$interface_name:"; then
            sudo ip link delete $interface_name
        fi
    done
}
