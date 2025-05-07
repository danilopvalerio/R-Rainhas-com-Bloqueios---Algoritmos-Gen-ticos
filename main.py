from genetic_n_queens_com_bloqueios import Genetic_N_QUEENS, plot_generations
from bloqueios import gerar_tabuleiro_com_bloqueios_melhorado

def construir_tabuleiro_completo(n, bloqueios, rainhas):
    tabuleiro = [['.' for _ in range(n)] for _ in range(n)]
    for (i, j) in bloqueios:
        tabuleiro[i][j] = 'X'
    for i, j in enumerate(rainhas):
        if tabuleiro[i][j] == 'X':
            tabuleiro[i][j] = '!'  # penalidade visual
        else:
            tabuleiro[i][j] = 'R'
    return tabuleiro

def imprimir_tabuleiro(tabuleiro, limite=32):
    n = len(tabuleiro)
    for i in range(min(n, limite)):
        print(" ".join(tabuleiro[i][:limite]))

def testar_n_rainhas_com_bloqueios(n, seed=42):
    print(f"\n========== Testando para n = {n} ==========")

    # Gerar tabuleiro e bloqueios
    tab, bloqueios_list = gerar_tabuleiro_com_bloqueios_melhorado(n=n, seed=seed)
    bloqueios = set(bloqueios_list)

    # Exibir tabuleiro inicial no console (limitado)
    print("Tabuleiro inicial com bloqueios (X):")
    imprimir_tabuleiro(tab)
    print(f"\nTotal de bloqueios: {len(bloqueios)}")

    # Executar algoritmo genético
    results, best = Genetic_N_QUEENS(
        dimensions=n,
        population_size=500,
        generations=1200,
        mutation_rate=0.1,
        bloqueios=bloqueios
    )

    final_gen = results[-1][0]
    final_fit = results[-1][2][1]
    print(f"\nMelhor resultado encontrado:")
    print(f"Geracao: {final_gen} | Fitness: {final_fit}")

    # Construir tabuleiro final com rainhas e bloqueios
    tabuleiro_final = construir_tabuleiro_completo(n, bloqueios, best)

    print("\nTabuleiro com bloqueios (X) e rainhas (R):")
    imprimir_tabuleiro(tabuleiro_final)

    # Salvar log completo
    log = []
    log.append("Tabuleiro inicial com bloqueios (X):")
    for linha in tab:
        log.append(" ".join(linha))
    
    log.append(f"\nTotal de bloqueios: {len(bloqueios)}")

    log.append("\nTabuleiro final com bloqueios (X) e rainhas (R):")
    for linha in tabuleiro_final:
        log.append(" ".join(linha))

    log.append("\nIteracao | Solucao encontrada | Melhor fitness | Media da populacao")
    for r in results:
        status = "Sim" if r[2][1] == 0 else "Nao"
        log.append(f"{r[0]:>9} | {status:^18} | {r[2][1]:^14} | {r[3]:.2f}")
    
    log.append(f"\nMelhor resultado encontrado:")
    log.append(f"Geracao: {final_gen} | Fitness: {final_fit}")
    log.append(f"Tempo estimado: {int((final_gen+1)*1000/60)} ms")

    with open(f"resultado_n{n}.txt", "w", encoding="utf-8") as f:
        for linha in log:
            f.write(linha + "\n")

    plot_generations(results)

if __name__ == "__main__":
    for n in [8, 16, 32, 128]:
        testar_n_rainhas_com_bloqueios(n)
        
