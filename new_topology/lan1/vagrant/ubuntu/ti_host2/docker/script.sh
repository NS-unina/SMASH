#!/bin/bash
docker_compose_file="/home/claudio/ubuntu/ti_host2/docker/docker-build/docker-compose.yaml"

name=$1
internal_ip=$2
ssh_port=$3
ftp_port=$4
socks_port=$5

# Configurazione del nuovo container
config="
    $name:
        build: ./images/heralding_imm
        container_name: $name
        cap_add:
        - NET_ADMIN 
        tty: true
        stdin_open: true
        privileged: true
        volumes:
        - ./configurations/heralding:/home
        networks:
          my_network:
            ipv4_address: $internal_ip
        ports:
          - \"$ssh_port:22\"  
          - \"$ftp_port:21\" 
          - \"$socks_port:1080\""       
        


#ed -i "/services:/a\\${new_service_config}" "${docker_compose_file}"

sed -i "/services:/r /dev/stdin" "${docker_compose_file}" <<< "${config}"

sleep 1
cd /home/claudio/ubuntu/ti_host2/docker/docker-build
sudo docker-compose up -d $container_name
sleep 1





