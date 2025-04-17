from configs import *
import os
import time

# --- Funções de Manipulação de Pontuação ---

# Função para inicializar o arquivo de highscore
def criar_arquivo_highscore():
    if not os.path.exists(ARQUIVO_HIGHSCORE):
        with open(ARQUIVO_HIGHSCORE, "w") as arquivo:
            pass

# Função para ler as três maiores pontuações do arquivo
def get_pontuacoes():
    # Verifica se o arquivo de pontuação existe
    if not os.path.exists(ARQUIVO_HIGHSCORE):
        return []  # Se o arquivo não existir, retorna uma lista vazia

    pontuacoes = []
    
    # Lê as pontuações e a data de cada linha do arquivo
    with open(ARQUIVO_HIGHSCORE, "r") as f:
        for linha in f:
            pontuacao, data = linha.strip().split(",")
            pontuacoes.append((int(pontuacao), data))

    # Ordena as pontuações do maior para o menor
    return sorted(pontuacoes, reverse=True, key=lambda x: x[0])

# Função para salvar uma nova pontuação
def salvar_pontuacao(nova_pontuacao):
    # Obtem as pontuações atuais
    pontuacoes = get_pontuacoes()
    
    # Obtém a data atual no formato "dia/mês/ano hora:minuto"
    data_atual = time.strftime("%d/%m/%Y %H:%M")
    
    # Adiciona a nova pontuação, se houver menos de 3 pontuações registradas
    if len(pontuacoes) < 3:
        pontuacoes.append((nova_pontuacao, data_atual))
    else:
        # Substitui a menor pontuação se a nova for maior
        pontuacao_minima = min(pontuacoes, key=lambda x: x[0])
        if nova_pontuacao > pontuacao_minima[0]:
            pontuacoes.remove(pontuacao_minima)
            pontuacoes.append((nova_pontuacao, data_atual))

    # Ordena novamente e mantém apenas as 3 maiores
    pontuacoes = sorted(pontuacoes, reverse=True, key=lambda x: x[0])[:3]

    # Salva as três maiores pontuações no arquivo
    with open(ARQUIVO_HIGHSCORE, "w") as f:
        for pontuacao, data in pontuacoes:
            f.write(f"{pontuacao},{data}\n")
