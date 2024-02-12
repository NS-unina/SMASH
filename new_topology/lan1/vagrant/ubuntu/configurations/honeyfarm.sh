
#!/bin/sh

sudo apt update
sudo useradd honeyfarm
sudo passwd honeyfarm
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

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

sudo apt install net-tools

#auditbeat
#curl -L -O https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-8.7.0-amd64.deb
#sudo dpkg -i auditbeat-8.7.0-amd64.deb

#sudo cp /home/claudio/ubuntu/int_service/auditbeat.yml /etc/auditbeat/auditbeat.yml

#sudo service auditbeat start
#sudo systemctl enable auditbeat


