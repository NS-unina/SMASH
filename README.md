# Honey-MTD-2

## Installation
### Prerequirements  
In order to execute the project on your machine
you need to install *Open vSwitch*, *Vagrant*, *Virtualbox*, *Docker* and *Docker Compose*.

The following steps allow project running on a Linux *(Ubuntu 22.04)* machine.

### Setup
In `new_topology` folder: 
1. Execute the script **create_net.sh**.
```  
$ ./create_net.sh
```
2. Execute the script **setup.sh**.
```  
$ ./setup.sh
```
Virtual Machines creation and configuration:

1. In `lan1/vagrant/ubuntu` folder run **vagrant up**.
```  
$ cd new_topology/lan1/vagrant/ubuntu
$ vagrant up
```
VM username = **vagrant**. VM password = **vagrant**.

Server Flask:
1. Install Flask.
```  
$ sudo pip3 install flask
```  
2. In `new_topology/lan1` folder run **python3 app.py**
```  
$ cd new_topology/lan1
$ python3 app.py
```

Containers building and setup:
1. In `docker/docker-build` folder run **docker compose up**.
```  
$ cd new_topology/docker/docker-build
$ docker compose up
```
2. In `docker` folder execute the script **setup_container.sh**.
```  
$ cd new_topology/docker
$ ./setup_container.sh
```
3. In `docker` folder execute the script **auth.sh**.
```  
$ cd new_topology/docker
$ ./auth.sh
```
## Execution
### Start Ryu Controller
1. Open a command line and execute *controller* Container:
```  
$ sudo docker exec -it controller bash
```
2. In *controller* Container, enter in **/home/rest_controller** directory and run the following command:
```  
$ cd /home/rest_controller
$ ryu-manager rest_controller.py
```

### Launch Elastalert
1. Enter in *ELK* Virtual Machine (via VirtualBox GUI) with username and password previously specified.
2. In *ELK* Virtual Machine, enter in **/elastalert** directory and run:
```  
$ cd elastalert
$ python3 -m elastalert.elastalert --verbose
```

## Reset
1. In `/docker/docker-build` run **docker compose down**.
```  
$ cd new_topology/docker/docker-build
$ docker compose down
```
2. In `/vagrant/ubuntu` run **vagrant destroy**.
```  
$ cd new_topology/vagrant/ubuntu
$ vagrant destroy
```
3. In `new_topology` execute the script **reset.sh**.
```  
$ ./reset.sh

