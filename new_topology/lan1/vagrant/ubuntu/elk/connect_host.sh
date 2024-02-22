#!/bin/sh
echo $1
var=$(echo $1 | python3 /home/vagrant/take_ip.py)
echo $var

#echo "REDIRECT TO COWRIE SSH"
#curl -X POST \
#   -H 'Content-Type: application/json' \
#   -d "{\"Source_IP\": \"$var\", \"Dpid\": \"85884017520972\"}" \
#   http://10.1.5.100:8080/rest_controller/push_int_server_out

#PUSH INT SERVER OUT È UN REDIRECT TRAFFIC SSH DA SSH_SERVICE (10.1.3.13)
echo "REDIRECT INTERNAL SSH SERVER TO DECOY"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"22\", \"Source\": \"ssh_service\"}"\
   http://10.1.5.100:8080/rest_controller/redirect_traffic


