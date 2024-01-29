#!/bin/sh
echo $1
var=$(echo $1 | python3 /home/vagrant/take_ip.py)
echo $var

echo "REDIRECT TO COWRIE SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$var\", \"Dpid\": \"85884017520972\"}" \
   http://10.1.5.100:8080/rest_controller/push_int_server_out

