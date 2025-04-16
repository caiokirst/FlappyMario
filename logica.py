import random
import glfw

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
        gap = 120
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
            gap_entre_obstaculos = max(300, 400 - pontuacao * 8)

    return obstaculos, pontuacao, velocidade_obstaculo, gap_entre_obstaculos

def verificar_colisao(pos_jogador, obstaculos):
    retangulo_jogador = (pos_jogador[0] + 5, pos_jogador[1] + 5, 30, 30)
    for obs in obstaculos:
        inferior = (obs['x'], obs['y_inferior'], obs['largura'], obs['altura_inferior'])
        superior = (obs['x'], obs['y_superior'], obs['largura'], obs['altura_superior'])
        if (retangulo_jogador[0] < inferior[0] + inferior[2] and retangulo_jogador[0] + retangulo_jogador[2] > inferior[0] and
            retangulo_jogador[1] < inferior[1] + inferior[3] and retangulo_jogador[1] + retangulo_jogador[3] > inferior[1]) or (retangulo_jogador[0] < superior[0] + superior[2] and retangulo_jogador[0] + retangulo_jogador[2] > superior[0] and
            retangulo_jogador[1] < superior[1] + superior[3] and retangulo_jogador[1] + retangulo_jogador[3] > superior[1]):
            return True
    return False
