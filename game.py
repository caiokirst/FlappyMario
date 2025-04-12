import glfw
from OpenGL.GL import *
from PIL import Image
import time
import numpy as np
import random
from textures import load_texture, render_text_to_texture, draw_background, draw_player, draw_obstacle_with_texture
from hud import render_hud

# Inicialização da janela
def init_window():
    if not glfw.init():
        print("Erro ao inicializar o GLFW!")
        return None

    window = glfw.create_window(800, 600, "Jogo Super Mario", None, None)
    if not window:
        print("Erro ao criar a janela!")
        glfw.terminate()
        return None

    glfw.make_context_current(window)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo (preto)
    glEnable(GL_TEXTURE_2D)
    glViewport(0, 0, 800, 600)
    return window

# Função principal do jogo
def main():
    last_time = time.time()
    score = 0
    lives = 3

    window = init_window()
    if not window:
        return

    # Carregar texturas
    player_texture = load_texture("assets/super_mario.png")
    bg_texture = load_texture("assets/fundo_super_mario.jpg")
    obstacle_texture = load_texture("assets/cano_verde.png")

    # Gerar as texturas para o texto
    score_texture, score_width, score_height = render_text_to_texture(f"Score: {score}")
    lives_texture, lives_width, lives_height = render_text_to_texture(f"Vidas: {lives}")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        # Atualizações do jogador e obstáculos (aqui você pode implementar a lógica do jogo)
        # Exemplo de movimento do jogador
        player_x = 200
        player_y = 300

        # Desenho do fundo, personagem e obstáculos
        draw_background(bg_texture)
        draw_player(player_texture, player_x, player_y)

        # Desenhar HUD (Score e Vidas)
        render_hud(score_texture, score_width, score_height, lives_texture, lives_width, lives_height)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
