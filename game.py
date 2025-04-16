from drawers import *
from highscore import *
from logica import *
from janela import *
from texturas import *
from configs import *
from OpenGL.GL import *
import glfw
import time
import os
# pip install glfw PyOpenGL Pillow

posicao_jogador = [POSICAO_INICIAL_JOGADOR_X, POSICAO_INICIAL_JOGADOR_Y]
gravidade = GRAVIDADE
velocidade_pulo = VELOCIDADE_PULO
velocidade_obstaculo = VELOCIDADE_OBSTACULO
espaco_entre_obstaculos = ESPACO_ENTRE_OBSTACULOS
vidas = VIDAS_INICIAIS

def inicializar_highscore():
    if not os.path.exists(ARQUIVO_HIGHSCORE):
        with open(ARQUIVO_HIGHSCORE, "w") as arquivo:
            pass

def carregar_recursos():
    # Carrega as texturas e retorna seus IDs em um dicionário
    recursos = {}
    recursos["jogador"] = carregar_textura(CAMINHO_TEX_JOGADOR)
    recursos["fundo"] = carregar_textura(CAMINHO_TEX_FUNDO)
    recursos["cano"] = carregar_textura(CAMINHO_TEX_CANO)
    if None in recursos.values():
        return None
    return recursos

def resetar_estado():
    # Variáveis de estado do jogo
    estado = {
        "posicao_jogador": [POSICAO_INICIAL_JOGADOR_X, ALTURA_JANELA // 2],
        "velocidade_jogador": 0,
        "obstaculos": [],
        "velocidade_obstaculo": VELOCIDADE_OBSTACULO,
        "pontuacao": 0,
        "jogo_iniciado": False,
        "espaco_entre_obstaculos": ESPACO_ENTRE_OBSTACULOS,
        "vidas": VIDAS_INICIAIS,
        "ultimo_tempo": time.time()
    }
    return estado

def desenhar_menu(janela, recursos, estado):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    desenhar_fundo(recursos["fundo"])
    # Exibir o highscore
    if os.path.exists(ARQUIVO_HIGHSCORE):
        pontuacoes = obter_pontuacoes()
        desenhar_texto(LARGURA_JANELA // 2 - 120, ALTURA_JANELA // 2 + 80, "TOP 3 PONTUACOES:")
        if not pontuacoes:
            desenhar_texto(LARGURA_JANELA // 2 - 190, ALTURA_JANELA // 2 + 50, "Nenhuma registrada ainda")
        else:
            for i, (valor_pontuacao, data) in enumerate(pontuacoes, start=1):
                desenhar_texto(LARGURA_JANELA // 2 - 160, ALTURA_JANELA // 2 + (50 - i * 30),
                               f"{i}. {valor_pontuacao} - {data}")

    desenhar_texto(LARGURA_JANELA // 2 - 220, ALTURA_JANELA // 2 - 80, "PRESSIONE ESPACO PARA INICIAR")
    desenhar_texto(10, ALTURA_JANELA - 40, f"Pontuacao: {estado['pontuacao']}")
    desenhar_texto(LARGURA_JANELA - 140, ALTURA_JANELA - 40, f"Vidas: {estado['vidas']}")
    
    glfw.swap_buffers(janela)
    glfw.poll_events()

def menu_inicial(janela, recursos, estado):
    while not estado["jogo_iniciado"] and not glfw.window_should_close(janela):
        desenhar_menu(janela, recursos, estado)
        # Inicia o jogo se a tecla espaço for pressionada
        if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
            estado["jogo_iniciado"] = True
            # Reseta a posição e os obstáculos
            estado["posicao_jogador"] = [POSICAO_INICIAL_JOGADOR_X, ALTURA_JANELA // 2]
            estado["obstaculos"] = []
            estado["ultimo_tempo"] = time.time()

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

def tratar_colisao(janela, recursos, estado):
    estado["vidas"] -= 1
    if estado["vidas"] <= 0:
        estado["jogo_iniciado"] = False
        return
    # Tela de colisão, onde o jogador pode continuar ou sair
    while not glfw.window_should_close(janela):
        glClear(GL_COLOR_BUFFER_BIT)
        desenhar_fundo(recursos["fundo"])
        desenhar_texto(LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2 + 40, "VOCE COLIDIU!")
        desenhar_texto(LARGURA_JANELA // 2 - 140, ALTURA_JANELA // 2, f"Vidas restantes: {estado['vidas']}")
        desenhar_texto(LARGURA_JANELA // 2 - 220, ALTURA_JANELA // 2 - 40, "Pressione ESPACO para continuar")
        desenhar_texto(LARGURA_JANELA // 2 - 160, ALTURA_JANELA // 2 - 70, "Pressione ESC para sair")
        desenhar_texto(10, ALTURA_JANELA - 40, f"Pontuacao: {estado['pontuacao']}")
        glfw.swap_buffers(janela)
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
            estado["posicao_jogador"] = [POSICAO_INICIAL_JOGADOR_X, (ALTURA_JANELA // 2) - 25]
            estado["velocidade_jogador"] = 0
            estado["obstaculos"] = []
            break
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)
            break

def desenhar_jogo(janela, recursos, estado):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    desenhar_fundo(recursos["fundo"])
    desenhar_jogador(recursos["jogador"], estado["posicao_jogador"][0], estado["posicao_jogador"][1])
    for obstaculo in estado["obstaculos"]:
        desenhar_obstaculo_com_textura(obstaculo['x'], obstaculo['y_inferior'],
                                        obstaculo['largura'], obstaculo['altura_inferior'], recursos["cano"])
        desenhar_obstaculo_invertido_com_textura(obstaculo['x'], obstaculo['y_superior'],
                                                 obstaculo['largura'], obstaculo['altura_superior'], recursos["cano"])
    desenhar_texto(10, ALTURA_JANELA - 40, f"Pontuacao: {estado['pontuacao']}")
    desenhar_texto(LARGURA_JANELA - 140, ALTURA_JANELA - 40, f"Vidas: {estado['vidas']}")
    glfw.swap_buffers(janela)
    glfw.poll_events()

def loop_do_jogo(janela, recursos, estado):
    while not glfw.window_should_close(janela) and estado["jogo_iniciado"]:
        atualizar_estado_jogo(janela, estado)
        if verificar_colisao(estado["posicao_jogador"], estado["obstaculos"]):
            tratar_colisao(janela, recursos, estado)
            # Se o jogador perdeu todas as vidas, sai do loop do jogo
            if estado["vidas"] <= 0:
                estado["jogo_iniciado"] = False
                break

        desenhar_jogo(janela, recursos, estado)

def tela_fim_de_jogo(janela, recursos, estado):
    # Salva pontuação se for o caso
    if estado["vidas"] <= 0 and estado["pontuacao"] > 0:
        salvar_pontuacao(estado["pontuacao"])
    while not estado["jogo_iniciado"] and not glfw.window_should_close(janela) and estado["vidas"] <= 0:
        glClear(GL_COLOR_BUFFER_BIT)
        desenhar_fundo(recursos["fundo"])
        desenhar_texto(LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2 + 40, "FIM DE JOGO!")
        desenhar_texto(LARGURA_JANELA // 2 - 120, ALTURA_JANELA // 2, f"PONTUACAO FINAL: {estado['pontuacao']}")
        desenhar_texto(LARGURA_JANELA // 2 - 220, ALTURA_JANELA // 2 - 40, "Pressione ESPACO para reiniciar")
        desenhar_texto(LARGURA_JANELA // 2 - 180, ALTURA_JANELA // 2 - 80, "Pressione ESC para sair")
        glfw.swap_buffers(janela)
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
            estado["jogo_iniciado"] = True
        elif glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

def main():
    # Inicialização geral
    inicializar_highscore()
    janela = inicializar_janela(LARGURA_JANELA, ALTURA_JANELA)
    if not janela:
        return

    recursos = carregar_recursos()
    if recursos is None:
        glfw.terminate()
        return

    while not glfw.window_should_close(janela):
        estado = resetar_estado()
        
        # Tela de Menu Inicial
        menu_inicial(janela, recursos, estado)
        
        # Loop principal do jogo
        loop_do_jogo(janela, recursos, estado)
        
        # Tela de fim de jogo
        tela_fim_de_jogo(janela, recursos, estado)

    glfw.terminate()

if __name__ == "__main__":
    main()
