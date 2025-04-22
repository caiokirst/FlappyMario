from configs import *
import random
import glfw
import time
from drawers import desenhar_jogo

# --- Funções de Atualização do Estado e Jogo ---

def atualizar_jogador(delta_time, janela, pos_jogador, velocidade_jogador, gravidade, velocidade_pulo, altura_janela):
    if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
        velocidade_jogador = velocidade_pulo

    velocidade_jogador += gravidade * delta_time
    pos_jogador[1] += velocidade_jogador * delta_time

    if pos_jogador[1] < 0:
        pos_jogador[1] = 0
        velocidade_jogador = 0

    if pos_jogador[1] > altura_janela - 50:
        pos_jogador[1] = altura_janela - 50
        velocidade_jogador = 0

    return pos_jogador, velocidade_jogador

def atualizar_obstaculos(delta_time, obstaculos, velocidade_obstaculo, gap_entre_obstaculos,
                          largura_janela, altura_janela, pos_jogador, pontuacao):
    for obs in obstaculos:
        obs['x'] -= velocidade_obstaculo * delta_time

    obstaculos = [obs for obs in obstaculos if obs['x'] + obs['largura'] > 0]

    if not obstaculos or (largura_janela - obstaculos[-1]['x']) > gap_entre_obstaculos:
        largura_obstaculo = 120
        gap = int(GAP_INICIAL)
        altura_minima = 50
        altura_maxima = altura_janela - gap - 50
        altura_inferior = random.randint(altura_minima, altura_maxima)
        y_superior = altura_inferior + gap
        altura_superior = altura_janela - y_superior

        novo_obs = {
            'x': largura_janela + 100,
            'y_superior': y_superior,
            'altura_superior': altura_superior,
            'y_inferior': 0,
            'altura_inferior': altura_inferior,
            'largura': largura_obstaculo,
            'pontuado': False
        }
        obstaculos.append(novo_obs)

    for obs in obstaculos:
        if not obs['pontuado'] and pos_jogador[0] > obs['x'] + obs['largura']:
            obs['pontuado'] = True
            pontuacao += 1
            velocidade_obstaculo = min(400, 200 + pontuacao * 4)
            gap_entre_obstaculos = min(ESPACO_ENTRE_OBSTACULOS, ESPACO_ENTRE_OBSTACULOS / 1.5 + pontuacao * 4)

    return obstaculos, pontuacao, velocidade_obstaculo, gap_entre_obstaculos

def verificar_colisao(pos_jogador, obstaculos):
    retangulo_jogador = (pos_jogador[0] + 5, pos_jogador[1] + 5, 30, 30)

    for obs in obstaculos:
        inferior = (obs['x'], obs['y_inferior'], obs['largura'], obs['altura_inferior'])
        superior = (obs['x'], obs['y_superior'], obs['largura'], obs['altura_superior'])

        if (retangulo_jogador[0] < inferior[0] + inferior[2] and retangulo_jogador[0] + retangulo_jogador[2] > inferior[0] and
            retangulo_jogador[1] < inferior[1] + inferior[3] and retangulo_jogador[1] + retangulo_jogador[3] > inferior[1]) or \
           (retangulo_jogador[0] < superior[0] + superior[2] and retangulo_jogador[0] + retangulo_jogador[2] > superior[0] and
            retangulo_jogador[1] < superior[1] + superior[3] and retangulo_jogador[1] + retangulo_jogador[3] > superior[1]):
            return True

    return False

def tratar_colisao(janela, recursos, estado):
    estado["vidas"] -= 1

    if estado["vidas"] <= 0:
        estado["jogo_iniciado"] = False
        return

    estado["posicao_jogador"] = [POSICAO_INICIAL_JOGADOR_X, (ALTURA_JANELA // 2) - 25]
    estado["velocidade_jogador"] = 0

    # Removido: NÃO limpar os obstáculos
    # estado["obstaculos"] = []

    estado["invencivel"] = True
    estado["tempo_invencivel"] = time.time()

def atualizar_coracoes(delta_tempo, estado):
    """Spawn, move e detecta colisões com corações."""
    agora = time.time()
    # Spawn periódico
    if agora - estado["ultimo_spawn_coracao"] > TEMPO_ENTRE_CORACOES:
        y_min = MARGEM_SPAWN_CORACAO
        y_max = ALTURA_JANELA - TAMANHO_CORACAO - MARGEM_SPAWN_CORACAO
        y = random.randint(y_min, y_max)
        estado["coracoes"].append({ "x": LARGURA_JANELA + TAMANHO_CORACAO, "y": y })
        estado["ultimo_spawn_coracao"] = agora

    # Move e remove corações fora da tela
    for cor in estado["coracoes"]:
        cor["x"] -= estado["velocidade_obstaculo"] * delta_tempo
    estado["coracoes"] = [
        c for c in estado["coracoes"]
        if c["x"] + TAMANHO_CORACAO > 0
    ]

    # Colisão jogador ↔ coração
    rx, ry = estado["posicao_jogador"]
    r_w, r_h = 30, 30  # mesma hitbox que obstacles
    for cor in estado["coracoes"][:]:
        cx, cy = cor["x"], cor["y"]
        if (rx < cx + TAMANHO_CORACAO and rx + r_w > cx and
            ry < cy + TAMANHO_CORACAO and ry + r_h > cy):
            estado["coracoes"].remove(cor)
            if estado["vidas"] < VIDAS_MAX:
                estado["vidas"] += 1

    return estado

def atualizar_estado_jogo(janela, estado):
    tempo_atual = time.time()
    delta_tempo = tempo_atual - estado["ultimo_tempo"]
    estado["ultimo_tempo"] = tempo_atual

    estado["posicao_jogador"], estado["velocidade_jogador"] = atualizar_jogador(
        delta_tempo, janela, estado["posicao_jogador"], estado["velocidade_jogador"],
        GRAVIDADE, VELOCIDADE_PULO, ALTURA_JANELA
    )

    estado["obstaculos"], estado["pontuacao"], estado["velocidade_obstaculo"], estado["espaco_entre_obstaculos"] = atualizar_obstaculos(
        delta_tempo, estado["obstaculos"], estado["velocidade_obstaculo"], estado["espaco_entre_obstaculos"],
        LARGURA_JANELA, ALTURA_JANELA, estado["posicao_jogador"], estado["pontuacao"]
    )

    estado = atualizar_coracoes(delta_tempo, estado)
    return estado

def resetar_estado():
    estado = {
        "posicao_jogador": [POSICAO_INICIAL_JOGADOR_X, ALTURA_JANELA // 2],
        "velocidade_jogador": 0,
        "obstaculos": [],
        "velocidade_obstaculo": VELOCIDADE_OBSTACULO,
        "pontuacao": 0,
        "jogo_iniciado": False,
        "espaco_entre_obstaculos": ESPACO_ENTRE_OBSTACULOS,
        "vidas": VIDAS_INICIAIS,
        "ultimo_tempo": time.time(),
        "invencivel": False,
        "tempo_invencivel": 0,
        "coracoes": [],
        "ultimo_spawn_coracao": time.time(),
    }
    return estado

def loop_do_jogo(janela, recursos, estado):
    while not glfw.window_should_close(janela) and estado["jogo_iniciado"]:
        estado = atualizar_estado_jogo(janela, estado)

        # Atualiza tempo de invencibilidade
        if estado["invencivel"]:
            tempo_decorrido = time.time() - estado["tempo_invencivel"]
            if tempo_decorrido > 2:
                estado["invencivel"] = False

        desenhar_jogo(janela, recursos, estado)

        # Só verifica colisão se não estiver invencível
        if not estado["invencivel"] and verificar_colisao(estado["posicao_jogador"], estado["obstaculos"]):
            tratar_colisao(janela, recursos, estado)

            if estado["vidas"] <= 0:
                estado["jogo_iniciado"] = False
                break
