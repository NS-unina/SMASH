import argparse
import pandas as pd
import os

def main(directory, column_name):
    # Lista per contenere tutti i DataFrame
    dfs = []

    # Legge tutti i file CSV nella directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            print(f"File letto: {filename}, Colonne: {df.columns.tolist()}")
            dfs.append(df)

    # Controlla se ci sono DataFrame nella lista
    if not dfs:
        print("Nessun file CSV trovato nella directory specificata.")
        return

    # Concatena tutti i DataFrame in uno solo
    all_data = pd.concat(dfs)

    # Verifica se la colonna richiesta esiste
    if column_name not in all_data.columns:
        print(f"La colonna '{column_name}' non esiste nei file CSV.")
        return

    # Calcola la media e la deviazione standard della colonna specificata per ogni VM_Number
    grouped_data = all_data.groupby('VM_Number').agg({column_name: ['mean', 'std']}).reset_index()

    # Rinominare le colonne
    grouped_data.columns = ['VM_Number', f'{column_name}_Mean', f'{column_name}_StdDev']

    # Arrotonda la media e la deviazione standard a due cifre dopo la virgola
    grouped_data = grouped_data.round({f'{column_name}_Mean': 2, f'{column_name}_StdDev': 2})

    # Percorso del file di output nella stessa directory di input
    output_filepath = os.path.join(directory, f'{column_name}_statistics.csv')

    # Salva il risultato in un nuovo file CSV
    grouped_data.to_csv(output_filepath, index=False)
    print(f"Risultati salvati in: {output_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calcola la media e la deviazione standard di una colonna specifica dai file CSV.')
    parser.add_argument('directory', type=str, help='Path alla directory contenente i file CSV.')
    parser.add_argument('column_name', type=str, help='Nome della colonna su cui calcolare le statistiche.')

    args = parser.parse_args()
    main(args.directory, args.column_name)
