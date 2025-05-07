
import random

def gerar_tabuleiro_com_bloqueios_melhorado(n, num_bloqueios=None, seed=None, percentual_max=0.2):
    if seed is not None:
        random.seed(seed)
    total_casas = n * n
    max_bloqueios = int(min(total_casas - n, percentual_max * total_casas))
    if num_bloqueios is None:
        num_bloqueios = int(0.07 * total_casas)
    elif num_bloqueios > max_bloqueios:
        raise ValueError(f"Número de bloqueios ({num_bloqueios}) excede o máximo permitido ({max_bloqueios}) para n={n}.")
    tabuleiro = [['.' for _ in range(n)] for _ in range(n)]
    bloqueios = set()
    while len(bloqueios) < num_bloqueios:
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        if (i, j) not in bloqueios:
            tabuleiro[i][j] = 'X'
            bloqueios.add((i, j))
    return tabuleiro, list(bloqueios)

def imprimir_tabuleiro(tabuleiro, limite=32):
    n = len(tabuleiro)
    for i in range(min(n, limite)):
        linha = " ".join(tabuleiro[i][:limite])
        print(linha)
