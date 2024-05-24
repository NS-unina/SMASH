import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main(file_path):
    # Leggi i dati dal file CSV
    df = pd.read_csv(file_path)

    # Prendi i nomi delle colonne per le etichette
    x_label = df.columns[0]
    y_label = df.columns[1]

    # Crea il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_label], df[y_label], marker='o', linestyle='-', color='b', label=y_label)

    # Aggiunge titolo e etichette
    plt.title(f'{y_label} per {x_label}')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Aggiunge una griglia
    plt.grid(True)

    # Aggiunge una legenda
    plt.legend()

    # Mostra il grafico
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot CPU Usage from CSV file.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file containing CPU usage data.')

    args = parser.parse_args()
    main(args.file_path)
