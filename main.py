import sys
import csv
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Constantes utilizadas:
K = 10
MAX_ITERATIONS = 100

def read_input_file(file_path):
    """Função utilizada para ler o arquivo csv de entrada e retornar as arestas obtidas."""
    edges = []
    try:
        with open(file_path, 'r', newline='') as f:
            print(f"Lendo o arquivo de entrada {file_path}...")
            data = csv.reader(f)

            for row in data:
                # Converte os valores da linha para int:
                for i in range(len(row)):
                    row[i] = int(row[i])
                edges.append(row) # cria uma lista com os valores da linha e adiciona na lista de arestas

    except FileNotFoundError as error:
        print(f"O arquivo {file_path} não existe!: {error}")
        sys.exit(1)

    return edges

def add_nodes_label(G, labels):
    for node in G.nodes:
        G.nodes[node]['label'] = random.choice(labels)
        print(f"Nó: {node}, Rótulo: {G.nodes[node]['label']}")

def calculate_mode_with_random_draw(neighbors_labels):
    if not neighbors_labels:
        return None
    
    # Conta a frequência de cada rótulo
    counter = Counter(neighbors_labels)
    max_freq = max(counter.values())
    
    # Lista dos rótulos com frequência máxima
    most_frequent = [label for label, freq in counter.items() if freq == max_freq]
    
    # Em caso de empate, escolhe aleatoriamente
    return random.choice(most_frequent)

def label_propagation(G=nx.Graph()):
    N = G.number_of_nodes()
    labels = np.arange(K)
    print(f"Rótulos: {labels}")
    add_nodes_label(G, labels)
    iteration = 0
    changed = True
    nodes_to_visit = np.array(G.nodes)
    print(nodes_to_visit)
    while iteration < MAX_ITERATIONS and changed:
        changed = False

        random.shuffle(nodes_to_visit) # aleatorizando a lista de nós visitados
        print(f"Ordem que os nós serão visitados: {nodes_to_visit}")

        for node in nodes_to_visit:
            neighbors = list(G.neighbors(node))
            print(f"Nó: {node}, Vizinhos: {neighbors}")

            if neighbors:
                neighbors_labels = []
                for neighbor in neighbors:
                    neighbors_labels.append(G.nodes[neighbor]['label'])
                
                # Calcula o novo rótulo
                novo_rotulo = calculate_mode_with_random_draw(neighbors_labels)
                
                # Verifica se houve mudança e atualiza
                if novo_rotulo != G.nodes[node]['label']:
                    G.nodes[node]['label'] = novo_rotulo
                    changed = True
                    print(f"Nó {node} mudou para rótulo: {novo_rotulo}")
        iteration += 1
    dict_rotulos = {node: G.nodes[node]['label'] for node in G.nodes}
    visualizar_comunidades(G, dict_rotulos, titulo=f"Comunidades detectadas após {iteration} iterações")

def create_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    return G

def identificar_comunidades(dict_rotulos):
    #Agrupa os vértices por comunidade baseado nos rótulos.
    comunidades = {}
    for vertice, rotulo in dict_rotulos.items():
        if rotulo not in comunidades:
            comunidades[rotulo] = []
        comunidades[rotulo].append(vertice)
    return comunidades

def visualizar_comunidades(grafo, dict_rotulos, titulo="Comunidades Detectadas"):
    #Visualiza o grafo com as comunidades coloridas.
    rotulos_lista = [dict_rotulos.get(i, i) for i in range(grafo.number_of_nodes())]
    comunidades = identificar_comunidades(dict_rotulos)
    num_comunidades = len(comunidades)
    
    # Gera cores distintas para cada comunidade
    cores = plt.cm.tab10(np.linspace(0, 1, num_comunidades))
    cor_por_comunidade = {}
    for idx, (rotulo, _) in enumerate(comunidades.items()):
        cor_por_comunidade[rotulo] = cores[idx]
    
    # Cores para cada vértice
    cores_vertices = [cor_por_comunidade[rotulo] for rotulo in rotulos_lista]
    pos = nx.spring_layout(grafo, seed=42)
    plt.figure(figsize=(12, 8))
    
    # Desenha o grafo
    nx.draw(grafo, pos, node_color=cores_vertices, with_labels=True, node_size=500, font_size=10, font_weight='bold', edge_color='gray', alpha=0.7)
    
    # Adiciona legenda
    legend_elements = []
    for rotulo, vertices in comunidades.items():
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cor_por_comunidade[rotulo], markersize=10, label=f'Comunidade {rotulo}'))
    
    # Posiciona a legenda fora do gráfico
    plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5))
    plt.title(titulo)
    plt.subplots_adjust(right=0.8)
    plt.show()

def run():
    # Verifica se os argumentos foram passados corretamente:
    if len(sys.argv) < 2:
        print("Argumentos insuficientes!")
        print("Formato correto: python main.py <caminho_para_o_arquivo_de_entrada.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    edges = read_input_file(file_path)
    print(edges)
    G = create_graph(edges)
    print(f"Nós: {G.nodes}")
    print(f"Arestas: {G.edges}")
    label_propagation(G)

if __name__ == "__main__":
    run()