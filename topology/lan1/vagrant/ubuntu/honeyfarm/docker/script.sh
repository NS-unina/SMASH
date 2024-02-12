# Utilizzo delle funzioni
source utils.sh

subnet=$1
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

python_file="/home/claudio/Honey-MTD-2/topology/lan1/docker/docker-build/configurations/controller/rest_controller/topology.py"
docker_compose_file="/home/claudio/Honey-MTD-2/new_topology/lan1/docker/docker-build/docker-compose.yaml"

interface_name=$(generate_interface_name)
ofport=$(generate_ofport "$bridge")
mac_container=$(generate_mac_address_container)
container_name=$(generate_container_name)
ip_address=$(find_free_ip3 "$subnet" "$occupied_ips")
free_port=$(find_free_port "$occupied_ports")
echo "Indirizzo IP libero trovato: $ip_address"
echo "Numero di porta libero trovato: $free_port"
echo "$ip_address" >> "$occupied_ips"
echo "$free_port" >> "$occupied_ports"

# Configurazione del nuovo container
new_service_config="    $container_name:
        build: ./images/heralding_imm
        container_name: $container_name
        cap_add:
        - NET_ADMIN 
        tty: true
        stdin_open: true
        privileged: true
        volumes:
        - ./configurations/heralding:/home"


#ed -i "/services:/a\\${new_service_config}" "${docker_compose_file}"

sed -i "/services:/r /dev/stdin" "${docker_compose_file}" <<< "${new_service_config}"

sleep 1
cd docker-build
sudo docker-compose up -d $container_name
sleep 1


cd ..
#SETUP CONTAINER
interface="${interface_name}_l"
sudo docker stop $container_name
sudo docker start $container_name
sudo ./my-ovs-docker add-port $bridge eth1 $container_name $interface_name $ofport --ipaddress=$ip_address/24 --macaddress=$mac_container
sudo ovs-vsctl -- set port $interface tag=$tag
sudo iptables -t nat -A POSTROUTING -o $interface -j MASQUERADE

sleep 1
#echo $interface
interface_ofport=$(sudo ovs-vsctl get Interface $interface ofport)
interface_ofport_int=$((interface_ofport))
topology_string="$container_name\ = Honeypot(\"$container_name\", \"$ip_address\", \"$mac_container\", $interface_ofport_int, '255.255.255.0')"

sed -i "/${comment}/a ${topology_string}" "${python_file}"






