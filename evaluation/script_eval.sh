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




# Loop per 10 ripetizioni
for ((i=8; i<$((8+repetitions)); i++))
do
    (cd "$TOPO_DIR" && ./reset.sh && ./create_net.sh && ./setup.sh)
        # Trova il PID del server Flask in esecuzione
    FLASK_PID=$(pgrep -f "python3 $FLASK_SERVER")

        # Naviga nella directory di Vagrant ed esegui il comando
    (cd "$VAGRANT_DIR" && vagrant destroy -f)
    if [ $? -ne 0 ]; then
        echo "Errore durante l'esecuzione di 'vagrant destroy -f' alla ripetizione $i"
        exit 1
    fi

    if [ -n "$FLASK_PID" ]; then
        echo "Trovato server Flask in esecuzione con PID: $FLASK_PID"
        echo "Terminazione del server Flask..."
        kill "$FLASK_PID"

        # Aspetta che il processo venga terminato
        while kill -0 "$FLASK_PID" 2>/dev/null; do
            sleep 1
        done

        echo "Server Flask terminato."
    else
        echo "Nessun server Flask in esecuzione trovato."
    fi

    # Riavvia il server Flask in una nuova shell
    echo "Riavvio del server Flask..."
    gnome-terminal -- bash -c "cd \"$FLASK_DIR\" && python3 \"$FLASK_SERVER\""
    echo "Server Flask riavviato."



    echo $((5+repetitions))
    echo "Ripetizione $i"



    
    if [ "$i" -ne 8 ]; then
    sleep 180
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

