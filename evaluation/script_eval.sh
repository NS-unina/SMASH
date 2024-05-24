#!/bin/bash

# Definisci le directory
VAGRANT_DIR="/home/claudio/Honey-MTD-2/new_topology/lan1/vagrant/ubuntu"
PYTHON_SCRIPT_DIR="/home/claudio/Honey-MTD-2/evaluation/VM-as-a-Service"
PYTHON_SCRIPT="capacity_test_VM.py"

TOPO_DIR="/home/claudio/Honey-MTD-2/new_topology"
FLASK_DIR="/home/claudio/Honey-MTD-2/new_topology/lan1"
SCRIPT_1="reset.sh"
SCRIPT_2="create_net.sh"
SCRIPT_3="setup.sh"
FLASK_SERVER="app.py"



repetitions=$1

# Verifica se l'input è un numero
if ! [[ $repetitions =~ ^[0-9]+$ ]]; then
    echo "Errore: Inserisci un numero valido."
    exit 1
fi

(cd "$TOPO_DIR" && ./reset.sh && ./create_net.sh && ./setup.sh)

sleep 5
gnome-terminal -- bash -c "cd \"$FLASK_DIR\" && python3 \"$FLASK_SERVER\""

sleep 5

# Loop per 10 ripetizioni
for ((i=1; i<=$repetitions; i++))
do
    echo "Ripetizione $i"

    # Naviga nella directory di Vagrant ed esegui il comando
    (cd "$VAGRANT_DIR" && vagrant destroy -f)
    if [ $? -ne 0 ]; then
        echo "Errore durante l'esecuzione di 'vagrant destroy -f' alla ripetizione $i"
        exit 1
    fi

    # Naviga nella directory dello script Python ed eseguilo
    (cd "$PYTHON_SCRIPT_DIR" && python3 "$PYTHON_SCRIPT" "$i")
    if [ $? -ne 0 ]; then
        echo "Errore durante l'esecuzione dello script Python alla ripetizione $i"
        exit 1
    fi

    echo "Ripetizione $i completata"
done

echo "Tutte le ripetizioni sono state completate"

