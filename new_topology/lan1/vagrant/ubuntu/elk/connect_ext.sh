#!/bin/sh
echo $1
echo "REDIRECT TO HERALDING DMZ SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"101737510984148\"}" \
   http://10.1.11.100:8080/rest_controller/redirect_ssh_dmz
   
echo "REDIRECT TO HERALDING DMZ SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"101737510984148\", \"Tcp_port\": \"22\", \"Source\": \"dmz_service\", \"Gateway\": \"gw10\", \"Subnet\": \"subnet4\", \"br\": \"br1\"}"\
   http://10.1.5.100:8080/rest_controller/redirect_traffic

