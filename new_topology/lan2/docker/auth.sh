#!/bin/bash

sudo docker exec int_host_lan2 /home/conf.sh
sudo docker exec controller_lan2 /home/conf.sh
sudo docker exec int_ssh_server_lan2 /home/conf.sh
