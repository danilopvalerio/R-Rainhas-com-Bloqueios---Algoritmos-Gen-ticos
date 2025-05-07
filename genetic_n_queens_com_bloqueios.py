import random
from collections import defaultdict
import matplotlib.pyplot as plt
import time

# Função que avalia a qualidade de um indivíduo da população (cromossomo).
# Penaliza colisões nas diagonais e presença de uma rainha em posição bloqueada.
#OBS: O código não penaliza explicitamente conflitos de rainhas na mesma linha, pois cada cromossomo já garante que
# cada rainha está em uma linha única. O cromossomo é uma permutação das colunas, ou seja, cada índice da lista
# representa uma linha e o valor naquele índice representa a coluna onde a rainha está posicionada. Assim, 
# por construção, não há possibilidade de duas rainhas estarem na mesma linha ou na mesma coluna pela forma que o código foi construído.
# Dessa forma, a verificação ocorre por diagonais e posições bloqueadas.
def fitness(chromosome: list, bloqueios: set):
    diag1 = defaultdict(int)  # Armazena a contagem de rainhas na mesma diagonal /
    diag2 = defaultdict(int)  # Armazena a contagem de rainhas na mesma diagonal \
    penalty = 0  # Penalidade acumulada por posições bloqueadas

    # Itera sobre cada linha (row) e coluna (col) definida pelo cromossomo
    # Iteração sobre o cromossomo
    for row, col in enumerate(chromosome):
        if (row, col) in bloqueios:
            penalty += 1000  # Penalidade severa se rainha estiver em posição bloqueada
        diag1[row - col] += 1
        diag2[row + col] += 1

    # Conta colisões em cada diagonal
    collisions = 0
    for count in diag1.values():
        # Essa fórmula serve para calcular o número de pares de rainhas que estão se atacando na mesma diagonal.
        collisions += count * (count - 1) // 2 
    for count in diag2.values():
        collisions += count * (count - 1) // 2

    return collisions + penalty  # Soma total de conflitos e penalidades

    # Explicação com exemplo:
    # Se o chromosome for = [0, 2, 3, 1]
    # E os bloqueios forem = {(0, 0), (3, 1)}
    # Para as posições (0, 0) e (3, 1) estão no conjunto de bloqueios, então adicionamos 2000 de penalidade (1000 de cada)
    # Colisões entre rainhas = 1 (conforme calculado)
    # Logo, collisions + penalty = 2001

# Cruzamento do tipo PMX (Partially Mapped Crossover)
# Garante que os filhos sejam permutações válidas
def pmx_crossover(parent1, parent2):
    size = len(parent1)
    cx1, cx2 = sorted(random.sample(range(size), 2))  # Seleciona dois pontos de corte
    child = [-1] * size
    child[cx1:cx2+1] = parent1[cx1:cx2+1]  # Copia segmento de um dos pais

    # Mapeia elementos para corrigir conflitos fora da faixa de cruzamento
    mapping = {parent1[i]: parent2[i] for i in range(cx1, cx2+1)}
    for i in range(size):
        if child[i] == -1:  # Preenche posições não definidas
            current = parent2[i]
            while current in child[cx1:cx2+1]:  # Resolve conflitos via mapeamento
                current = mapping.get(current, current)
            child[i] = current
    return child

# Aplica mutação por troca entre duas posições do cromossomo
def mutation(chromosome: list, mutation_prob: float = 0.1):
    if random.random() < mutation_prob:
        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

# Gera a população inicial como permutações válidas de 0 a n-1
def Generate_population(chromosome_size: int, population_size: int):
    return [random.sample(range(chromosome_size), chromosome_size) for _ in range(population_size)]

# Seleção por torneio: escolhe o melhor entre 'k' aleatórios
def tournament_selection(population, bloqueios, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        contenders = random.sample(population, tournament_size)
        selected.append(min(contenders, key=lambda x: fitness(x, bloqueios)))
    return selected

# Plota a evolução do fitness ao longo das gerações
def plot_generations(results):
    geration = []
    bests_alltime = []
    bests_generation = []

    for result in results:
        geration.append(result[0])
        bests_generation.append(result[1][1])
        bests_alltime.append(result[2][1])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(geration, bests_generation)
    ax1.set_xlabel('Geração')
    ax1.set_ylabel('Melhor fitness')
    ax1.set_title('Melhor fitness por geração')
    ax1.grid(True)

    ax2.plot(geration, bests_alltime)
    ax2.set_xlabel('Geração')
    ax2.set_ylabel('Melhor fitness')
    ax2.set_title('Melhor fitness de todas as gerações')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

# Função principal do algoritmo genético
def Genetic_N_QUEENS(dimensions=8, population_size=500, generations=1000, mutation_rate=0.1, elitism_size=2, bloqueios=set()):
    population = Generate_population(dimensions, population_size)  # População inicial
    best_chromosome = min(population, key=lambda x: fitness(x, bloqueios)).copy()  # Inicializa melhor solução
    results = []
    start_time = time.time()

    for generation in range(generations):
        selected_parents = tournament_selection(population, bloqueios)  # Seleciona indivíduos para cruzamento
        offspring = []

        # Cruzamento em pares
        for i in range(0, len(selected_parents), 2):
            if i + 1 >= len(selected_parents):
                parents = [selected_parents[i], random.choice(selected_parents)]  # Garante par válido
            else:
                parents = selected_parents[i:i + 2]
            child1 = pmx_crossover(parents[0], parents[1])
            child2 = pmx_crossover(parents[1], parents[0])
            offspring.extend([child1, child2])

        # Aplica mutação nos filhos e mantém o melhor da geração anterior
        offspring = [mutation(child, mutation_rate) for child in offspring[:population_size]]
        combined = offspring + [best_chromosome.copy()]
        population = sorted(combined, key=lambda x: fitness(x, bloqueios))[:population_size]

        current_best = min(population, key=lambda x: fitness(x, bloqueios))
        if fitness(current_best, bloqueios) < fitness(best_chromosome, bloqueios):
            best_chromosome = current_best.copy()  # Atualiza melhor solução

        avg_fitness = sum(fitness(ind, bloqueios) for ind in population) / len(population)
        results.append([
            generation,
            [current_best, fitness(current_best, bloqueios)],
            [best_chromosome, fitness(best_chromosome, bloqueios)],
            avg_fitness
        ])

        # Para execução se encontrar solução perfeita
        if fitness(best_chromosome, bloqueios) == 0:
            break

    end_time = time.time()
    exec_time_ms = int((end_time - start_time) * 1000)

    print(f"\nMelhor resultado encontrado:")
    print(f"Geração: {results[-1][0]} | Fitness: {results[-1][2][1]}")
    print(f"Tempo de execução: {exec_time_ms} ms")
    return results, best_chromosome
