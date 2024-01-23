#!/bin/sh
echo $1
echo "REDIRECT TO COWRIE SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"22\", \"Decoy\": \"heralding1\", \"Source\": \"service\"}" \
   http://10.1.5.100:8080/rest_controller/redirect_traffic

echo "REDIRECT TO HERALDING FTP"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"21\", \"Decoy\": \"heralding1\", \"Source\": \"service\"}"\
   http://10.1.5.100:8080/rest_controller/redirect_traffic

echo "REDIRECT TO COWRIE SMTP TELNET"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\", \"Tcp_port\": \"23\", \"Decoy\": \"cowrie\", \"Source\": \"service\"}"\
   http://10.1.5.100:8080/rest_controller/redirect_traffic

echo "REDIRECT TO COWRIE HTTP PORT HOPPING"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\"}" \
   http://10.1.5.100:8080/rest_controller/http_port_hopping

