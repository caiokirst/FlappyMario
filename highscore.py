import os
import time

HIGHSCORE_FILE = "assets/highscore.txt"

# Função para ler os três maiores scores do arquivo
def get_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []  # Se o arquivo não existir, retorna uma lista vazia

    highscores = []
    with open(HIGHSCORE_FILE, "r") as f:
        for line in f:
            score, date = line.strip().split(",")
            highscores.append((int(score), date))

    # Retorna os scores ordenados do maior para o menor
    return sorted(highscores, reverse=True, key=lambda x: x[0])

# Função para salvar um novo highscore
def save_highscore(new_score):
    highscores = get_highscores()
    
    # Obter a data atual
    current_date = time.strftime("%d/%m/%Y %H:%M")
    
    # Verifica se há menos de 3 registros
    if len(highscores) < 3:
        highscores.append((new_score, current_date))
    else:
        # Se for maior que algum, substitui o menor
        min_score = min(highscores, key=lambda x: x[0])
        if new_score > min_score[0]:
            highscores.remove(min_score)
            highscores.append((new_score, current_date))

    # Ordena novamente e mantém apenas os 3 maiores
    highscores = sorted(highscores, reverse=True, key=lambda x: x[0])[:3]

    # Salva os três maiores no arquivo
    with open(HIGHSCORE_FILE, "w") as f:
        for score, date in highscores:
            f.write(f"{score},{date}\n")

# Função para exibir os highscores antes de iniciar o jogo
def display_highscores():
    highscores = get_highscores()

    print("\n=== HIGHSCORES ===")
    if not highscores:
        print("Nenhum highscore registrado ainda.")
    else:
        for i, (score, date) in enumerate(highscores, start=1):
            print(f"{i}. {score} pontos - {date}")

    print("==================\n")
