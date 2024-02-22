#!/bin/sh
echo $1
echo "REDIRECT SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"22\", \"Source\": \"service\"}" \
   http://10.1.5.100:8080/rest_controller/redirect_traffic

echo "REDIRECT FTP"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"21\", \"Source\": \"service\"}"\
   http://10.1.5.100:8080/rest_controller/redirect_traffic

echo "REDIRECT SMTP TELNET"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"23\", \"Source\": \"service\"}"\
   http://10.1.5.100:8080/rest_controller/redirect_traffic

echo "REDIRECT HTTP PORT HOPPING"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Source\": \"service\"}" \
   http://10.1.5.100:8080/rest_controller/http_port_hopping

