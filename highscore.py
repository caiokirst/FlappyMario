import os
import time

ARQUIVO_HIGHSCORE = "assets/highscore.txt"

# Função para ler os três maiores scores do arquivo
def obter_pontuacoes():
    if not os.path.exists(ARQUIVO_HIGHSCORE):
        return []  # Se o arquivo não existir, retorna uma lista vazia

    pontuacoes = []
    with open(ARQUIVO_HIGHSCORE, "r") as f:
        for linha in f:
            pontuacao, data = linha.strip().split(",")
            pontuacoes.append((int(pontuacao), data))

    # Retorna as pontuações ordenadas do maior para o menor
    return sorted(pontuacoes, reverse=True, key=lambda x: x[0])

# Função para salvar uma nova pontuação
def salvar_pontuacao(nova_pontuacao):
    pontuacoes = obter_pontuacoes()
    
    # Obter a data atual
    data_atual = time.strftime("%d/%m/%Y %H:%M")
    
    # Verifica se há menos de 3 registros
    if len(pontuacoes) < 3:
        pontuacoes.append((nova_pontuacao, data_atual))
    else:
        # Se for maior que algum, substitui o menor
        pontuacao_minima = min(pontuacoes, key=lambda x: x[0])
        if nova_pontuacao > pontuacao_minima[0]:
            pontuacoes.remove(pontuacao_minima)
            pontuacoes.append((nova_pontuacao, data_atual))

    # Ordena novamente e mantém apenas as 3 maiores
    pontuacoes = sorted(pontuacoes, reverse=True, key=lambda x: x[0])[:3]

    # Salva as três maiores no arquivo
    with open(ARQUIVO_HIGHSCORE, "w") as f:
        for pontuacao, data in pontuacoes:
            f.write(f"{pontuacao},{data}\n")

# Função para exibir as pontuações antes de iniciar o jogo
def exibir_pontuacoes():
    pontuacoes = obter_pontuacoes()

    print("\n=== PONTUAÇÕES ===")
    if not pontuacoes:
        print("Nenhuma pontuação registrada ainda.")
    else:
        for i, (pontuacao, data) in enumerate(pontuacoes, start=1):
            print(f"{i}. {pontuacao} pontos - {data}")

    print("==================\n")
