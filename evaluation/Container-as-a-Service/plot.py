import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def main(file_path):
    # Leggi i dati dal file CSV
    df = pd.read_csv(file_path)

    # Prendi i nomi delle colonne per le etichette
    x_label = df.columns[0]
    y_label = df.columns[1]

    # Crea il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_label], df[y_label], marker='o', linestyle='-', color='b', label=y_label)

    # Calcola la deviazione standard
    std_dev = df[f'{y_label}_StdDev'][0]

    # Aggiunge titolo e etichette, incluso deviazione standard
    plt.title(f'{y_label} per {x_label} (Deviazione standard: {std_dev:.2f})')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Aggiunge una griglia
    plt.grid(True)

    # Aggiunge una legenda
    plt.legend()

    # Ottieni la cartella del file CSV
    output_folder = os.path.dirname(file_path)

    # Salva il grafico come immagine nella stessa cartella del file CSV
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + '_plot.png'
    output_filepath = os.path.join(output_folder, output_filename)
    plt.savefig(output_filepath)

    # Mostra il grafico
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot CPU Usage from CSV file.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file containing CPU usage data.')

    args = parser.parse_args()
    main(args.file_path)
