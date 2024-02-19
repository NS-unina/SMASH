#!/usr/bin/env bash

set -efux

sudo hostnamectl set-hostname 'cowrie'

sudo apt update && \
sudo apt-get install -y git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv

# Aggiungi la chiave GPG di Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Aggiungi il repository Docker al tuo sistema
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Aggiorna l'elenco dei pacchetti con i repository Docker
sudo apt update

# Installa Docker
sudo apt install -y docker-ce

# Aggiungi l'utente al gruppo docker per poter eseguire comandi Docker senza sudo
sudo usermod -aG docker $USER

# Scarica l'ultima versione di Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Applica i permessi eseguibili a Docker Compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt-get install net-tools

sudo sed -i 's/#Port 22/Port 40001/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd

sudo apt install -y apache2  # Installa Apache
sudo apt install -y python3-pip  # Installa pip per Python
sudo pip3 install flask  # Installa Flask per Python

# shellcheck disable=SC2155
#export pass=$(echo mypasswd | openssl passwd -6 -stdin)
#sudo useradd -m -p $pass -s /bin/bash administrator

sudo adduser --disabled-password cowrie1
sudo passwd -d cowrie1
sudo adduser cowrie1 sudo

sudo su - cowrie1<<EOF
git clone https://github.com/cowrie/cowrie
cd cowrie
virtualenv --python=python3 cowrie-env
. cowrie-env/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
pip install pymongo

sudo cp /home/claudio/ubuntu/ext_cowrie/conf.sh /home/cowrie1
sudo cp /home/claudio/ubuntu/ext_cowrie/start.sh /home/vagrant

sudo cp /home/claudio/ubuntu/ext_cowrie/cowrie.cfg /home/cowrie1/cowrie/etc
sudo touch /etc/authbind/byport/22
sudo chown cowrie1:cowrie1 /etc/authbind/byport/22
sudo chmod 770 /etc/authbind/byport/22

sudo touch /etc/authbind/byport/23
sudo chown cowrie1:cowrie1 /etc/authbind/byport/23
sudo chmod 770 /etc/authbind/byport/23

sudo cp /home/cowrie1/cowrie/etc/userdb.example /home/cowrie1/cowrie/etc/userdb.txt

cd ..

#filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.7.0-amd64.deb
sudo dpkg -i filebeat-8.7.0-amd64.deb
#metricbeat
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-8.7.0-amd64.deb
sudo dpkg -i metricbeat-8.7.0-amd64.deb
#auditbeat
curl -L -O https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-8.7.0-amd64.deb
sudo dpkg -i auditbeat-8.7.0-amd64.deb

chmod +x home/claudio/ubuntu/host2/your_script.sh

sudo cp /home/claudio/ubuntu/ext_cowrie/filebeat.yml /etc/filebeat/filebeat.yml
sudo systemctl start filebeat
sudo systemctl enable filebeat

sudo cp /home/claudio/ubuntu/ext_cowrie/metricbeat.yml /etc/metricbeat/metricbeat.yml
sudo service metricbeat start
sudo systemctl enable metricbeat

sudo cp /home/claudio/ubuntu/ext_cowrie/auditbeat.yml /etc/auditbeat/auditbeat.yml
sudo service auditbeat start
sudo systemctl enable auditbeat
EOF


