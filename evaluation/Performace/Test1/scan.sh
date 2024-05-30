#!/bin/bash

# Specifica la subnet
subnet="10.1.3."

repetition_number=$1

# Intervallo di IP (ad esempio, da 1 a 30 per la tua subnet)
start_ip=11
end_ip=14

# Porta range
ports="1-100"

# Timing template
timing="-T4"

# Altre opzioni per velocizzare la scansione
options="-Pn --max-retries 2 "

# Contatori per i risultati
hosts_up=0
hosts_down=0

# Directory per salvare i risultati
output_dir="nmap_results"
output_dir2="1_server"
mkdir -p "$output_dir"
mkdir -p "$output_dir2"


# Crea un array di IP nella subnet
ips=()
for i in $(seq $start_ip $end_ip); do
    ips+=("${subnet}${i}")
done

# Randomizza l'ordine degli IP
shuffled_ips=($(shuf -e "${ips[@]}"]))

# Loop attraverso ciascun IP randomizzato
for ip in "${shuffled_ips[@]}"; do
    echo "Scanning $ip"
    
    # File di output per questo IP
    output_file="${output_dir2}/${repetition_number}.txt"
    output_report="${output_dir2}/report_${repetition_number}.txt"
    
    # Esegui la scansione Nmap e salva l'output nel file
    nmap $timing $options -p $ports $ip -oN "$output_file"
    
    # Controlla se l'host è up o down
    if grep -q "Host is up" "$output_file"; then
        echo "$ip is up"
        hosts_up=$((hosts_up + 1))
    else
        echo "$ip is down"
        hosts_down=$((hosts_down + 1))
    fi
done

# Stampa i risultati finali
echo "Scan complete." >> "$output_report"
echo "Hosts up: $hosts_up" >> "$output_report"
echo "Hosts down: $hosts_down" >> "$output_report"
