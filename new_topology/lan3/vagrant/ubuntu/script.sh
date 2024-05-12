# Utilizzo delle funzioni
source utils.sh

subnet=$1
subnet1="10.2.3.0/24"
subnet2="10.2.4.0/24"

occupied_ips="/home/claudio/Honey-MTD-2/new_topology/lan1/occupied_ips"
occupied_ports="/home/claudio/Honey-MTD-2/new_topology/lan1/occupied_ports"

if [ "$subnet" == "$subnet1" ]; then
    comment="#Subnet 1"
    gateway="10.2.3.1"
    tag="1"
    bridge="br0_lan1"
    routes="[\"10.2.4.0/24\", \"10.2.5.0/24\", \"10.2.10.0/24\", \"10.2.11.0/24\"]"
elif [ "$subnet" == "$subnet2" ]; then
    gateway="10.2.4.1"
    comment="#Subnet 2"
    bridge="br0_lan1"
    tag="2"
    routes="[\"10.2.3.0/24\", \"10.2.5.0/24\", \"10.2.10.0/24\", \"10.2.11.0/24\"]"
else
    echo "Inserisci una subnet valida"
    exit 1
fi

python_file="/home/claudio/Honey-MTD-2/topology/lan1/docker/docker-build/configurations/controller/rest_controller/topology.py"
tap_name=$(generate_tap_name)
ofport=$(generate_ofport "$bridge")
mac_tap=$(generate_mac_address)
vm_name=$(generate_vm_name)
ip_address=$(find_free_ip3 "$subnet" "$occupied_ips")
free_port=$(find_free_port "$occupied_ports")
echo "Indirizzo IP libero trovato: $ip_address"
echo "Numero di porta libero trovato: $free_port"
echo "$ip_address" >> "$occupied_ips"
echo "$free_port" >> "$occupied_ports"
#TAP create_tap(tap_name, bridge_name, tag, ofport)
create_tap "$tap_name" "$bridge" "$tag" "$ofport"

tap_ofport=$(sudo ovs-vsctl get Interface "$tap_name" ofport)

config_string="    deploy_honeypot2(config, \"$vm_name\", \"ubuntu/focal64\", \"512\",\"shared\", 22, \"$free_port\",\"ssh\", \"$tap_name\", \"$mac_tap\", \"$ip_address\", $routes,\"$gateway\")"

topology_string="$vm_name\ = Honeypot(\"$vm_name\", \"$ip_address\", \"$mac_tap\", \"$tap_ofport\", '255.255.255.0')"
echo $topology_string

sed -i "/# HONEYPOT FARM/a\\
${config_string}" Vagrantfile

sed -i "/${comment}/a ${topology_string}" "${python_file}"





vagrant up "$vm_name"


