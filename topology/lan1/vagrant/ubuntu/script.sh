# Utilizzo delle funzioni
source utils.sh
tap_name=$(generate_tap_name)
ofport=$(generate_ofport "br0_lan1")
mac_tap=$(generate_mac_address)
vm_name=$(generate_vm_name)
 

#TAP create_tap(tap_name, bridge_name, tag, ofport)
create_tap "$tap_name" "br0_lan1" "2" "$ofport"

config_string="    deploy_honeypot2(config, \"$vm_name\", \"ubuntu/focal64\", \"512\",\"shared\", 22, 3209,\"ssh\", \"$tap_name\", \"$mac_tap\", \"10.1.3.18\", [\"10.1.4.0/24\", \"10.1.5.0/24\", \"10.1.10.0/24\", \"10.1.11.0/24\"],\"10.1.3.1\")"

sed -i "/# INSERISCI NUOVO CODICE PRIMA DI QUESTO COMMENTO/i\\
${config_string}" Vagrantfile

vagrant up "$vm_name"
