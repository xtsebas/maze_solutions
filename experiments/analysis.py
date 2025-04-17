import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_analytics_from_csv(csv_path='results/maze_results.csv'):
    if not os.path.isfile(csv_path):
        print("CSV no encontrado.")
        return

    df = pd.read_csv(csv_path)

    # 1. Promedio de tiempo por algoritmo
    avg_time = df.groupby('Algoritmo')['Tiempo'].mean()
    avg_time.plot(kind='bar', title='Tiempo promedio por algoritmo')
    plt.ylabel("Tiempo (s)")
    plt.xlabel("Algoritmo")
    plt.tight_layout()
    plt.savefig("results/avg_time_per_algorithm.png")
    plt.clf()

    # 2. Cuántas veces fue primer lugar cada algoritmo
    rank1_count = df[df['Ranking'] == 1]['Algoritmo'].value_counts()
    rank1_count.plot(kind='bar', title='Cantidad de veces en 1er lugar')
    plt.ylabel("Veces en 1er lugar")
    plt.xlabel("Algoritmo")
    plt.tight_layout()
    plt.savefig("results/rank1_per_algorithm.png")
    plt.clf()

    # 3. Promedio de distancia por algoritmo
    avg_path = df.groupby('Algoritmo')['Distancia'].mean()
    avg_path.plot(kind='bar', title='Distancia promedio encontrada')
    plt.ylabel("Pasos")
    plt.xlabel("Algoritmo")
    plt.tight_layout()
    plt.savefig("results/avg_path_per_algorithm.png")
    plt.clf()

    # 4. Promedio de nodos expandidos
    avg_nodes = df.groupby('Algoritmo')['Nodos'].mean()
    avg_nodes.plot(kind='bar', title='Promedio de nodos explorados')
    plt.ylabel("Nodos")
    plt.xlabel("Algoritmo")
    plt.tight_layout()
    plt.savefig("results/avg_nodes_per_algorithm.png")
    plt.clf()

    print("-> Análisis generado y guardado como imágenes .png")
