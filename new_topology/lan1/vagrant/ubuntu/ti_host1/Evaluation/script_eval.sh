#!/bin/bash

# Definisci le directory
DOCKER_DIR="/home/claudio/ubuntu/ti_host1/docker/docker-build-capacity-test"
PYTHON_SCRIPT_DIR="/home/claudio/ubuntu/ti_host1/Evaluation"
PYTHON_SCRIPT="capacity_test_Container.py"

FLASK_DIR="/home/claudio/ubuntu/ti_host1"
FLASK_SERVER="app.py"



repetitions=$1

# Verifica se l'input è un numero
if ! [[ $repetitions =~ ^[0-9]+$ ]]; then
    echo "Errore: Inserisci un numero valido."
    exit 1
fi




# Loop per 10 ripetizioni
for ((i=1; i<$((1+repetitions)); i++))
do
        # Trova il PID del server Flask in esecuzione
    FLASK_PID=$(pgrep -f "python3 $FLASK_SERVER")

    if [ "$i" -ne 1 ]; then
        # Naviga nella directory di Vagrant ed esegui il comando
        (cd "$DOCKER_DIR" && sudo docker compose down -v)
        if [ $? -ne 0 ]; then
            echo "Errore durante l'esecuzione di 'docker compose down -v' alla ripetizione $i"
            exit 1
        fi
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
    (cd "$FLASK_DIR" && nohup python3 "$FLASK_SERVER" &)
    echo "Server Flask riavviato."

    echo "Ripetizione $i"



    
    if [ "$i" -ne 1 ]; then
    sleep 10
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

