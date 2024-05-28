import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def main(file_path, prefix):
    # Leggi i dati dal file CSV
    df = pd.read_csv(file_path)

    if prefix == "ResponseTime":
        df = df.iloc[1:]

    # Prendi i nomi delle colonne per le etichette
    x_label = df.columns[0]
    y_label = df.columns[1]

    # Crea il grafico principale per i dati
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_label], df[y_label], marker='o', linestyle='-', color='b', label=y_label)

    # Aggiunge titolo e etichette
    plt.title(f'{y_label} per Numero di Container')
    plt.xlabel('Numero di Container')
    plt.ylabel(y_label)

    # Aggiunge una griglia
    plt.grid(True)

    # Aggiunge una legenda
    plt.legend()

    # Ottieni la cartella del file CSV
    output_folder = os.path.dirname(file_path)

    # Salva il grafico dei dati come immagine nella stessa cartella del file CSV
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + '_data_plot.png'
    output_filepath = os.path.join(output_folder, output_filename)
    plt.savefig(output_filepath)

    # Creazione di un secondo grafico per la deviazione standard
    std_dev_col = f'{prefix}_StdDev'
    std_dev = df[std_dev_col]

    plt.figure(figsize=(10, 6))
    plt.bar(df[x_label], std_dev, color='orange', label=f'{prefix} Deviazione standard')
    plt.title(f'{prefix} Deviazione standard')
    plt.xlabel('Numero di Container')
    plt.ylabel('Deviazione standard')
    plt.xticks(df[x_label])
    plt.legend()

    # Salva il grafico della deviazione standard come immagine nella stessa cartella del file CSV
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + '_std_dev_plot.png'
    output_filepath = os.path.join(output_folder, output_filename)
    plt.savefig(output_filepath)

    # Mostra entrambi i grafici
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot CPU Usage from CSV file.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file containing CPU usage data.')
    parser.add_argument('prefix', type=str, help='Prefix to identify columns for standard deviation calculation.')

    args = parser.parse_args()
    main(args.file_path, args.prefix)
