import glfw
from OpenGL.GL import *
from PIL import Image, ImageFont, ImageDraw
import time
import random
from drawers import *

# Configurações da janela
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Variáveis do jogo
player_pos = [100, WINDOW_HEIGHT // 2]
player_speed = 0
gravity = -600
jump_speed = 300
last_time = 0
obstacles = []
obstacle_speed = 200
score = 0
game_started = False
gap_between_obstacles = 400

# IDs de textura
texture_id = None
bg_texture_id = None
cano_texture_id = None

# Carregamento de textura
def load_texture(path):
    try:
        image = Image.open(path)
    except IOError:
        print("Erro ao carregar a imagem:", path)
        return None

    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    width, height = image.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

# Inicialização da janela com configuração 2D
def init_window():
    if not glfw.init():
        return None
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Flappy Mario", None, None)
    if not window:
        glfw.terminate()
        return None
    glfw.make_context_current(window)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0.5, 0.7, 0.9, 1.0)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    return window

# Atualiza o jogador
def update_player(delta_time, window):
    global player_pos, player_speed
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        player_speed = jump_speed
    player_speed += gravity * delta_time
    player_pos[1] += player_speed * delta_time
    if player_pos[1] < 0:
        player_pos[1] = 0
        player_speed = 0
    if player_pos[1] > WINDOW_HEIGHT - 50:
        player_pos[1] = WINDOW_HEIGHT - 50
        player_speed = 0

# Atualiza os obstáculos e controla a pontuação
def update_obstacles(delta_time):
    global obstacles, score, obstacle_speed, gap_between_obstacles

    # Move obstáculos
    for obs in obstacles:
        obs['x'] -= obstacle_speed * delta_time

    # Remove obstáculos fora da tela
    obstacles[:] = [obs for obs in obstacles if obs['x'] + obs['width'] > 0]

    # Adiciona novo obstáculo se necessário
    if not obstacles or (WINDOW_WIDTH - obstacles[-1]['x']) > gap_between_obstacles:
        obstacle_width = 160
        gap = 200
        min_top = 100
        max_top = WINDOW_HEIGHT - gap - 100
        top_y = random.randint(min_top, max_top)
        new_obs = {
            'x': WINDOW_WIDTH + 100,
            'y_upper': top_y + gap,
            'height_upper': WINDOW_HEIGHT - (top_y + gap),
            'y_lower': 0,
            'height_lower': top_y,
            'width': obstacle_width,
            'scored': False  # flag para controle de pontuação
        }
        obstacles.append(new_obs)

    # Verifica se o jogador passou por algum obstáculo
    for obs in obstacles:
        if not obs['scored'] and player_pos[0] > obs['x'] + obs['width']:
            obs['scored'] = True
            score += 1
            obstacle_speed = min(400, 200 + score * 4)
            gap_between_obstacles = max(200, 400 - score * 8)

# Checa colisões com os obstáculos
def check_collision():
    player_rect = (player_pos[0] + 10, player_pos[1] + 10, 30, 30)  # margem de 10 px
    for obs in obstacles:
        lower = (obs['x'], obs['y_lower'], obs['width'], obs['height_lower'])
        upper = (obs['x'], obs['y_upper'], obs['width'], obs['height_upper'])
        if (player_rect[0] < lower[0] + lower[2] and player_rect[0] + player_rect[2] > lower[0] and
            player_rect[1] < lower[1] + lower[3] and player_rect[1] + player_rect[3] > lower[1]) or \
           (player_rect[0] < upper[0] + upper[2] and player_rect[0] + player_rect[2] > upper[0] and
            player_rect[1] < upper[1] + upper[3] and player_rect[1] + player_rect[3] > upper[1]):
            return True
    return False

# Função principal
def main():
    global last_time, texture_id, bg_texture_id, cano_texture_id
    global player_pos, player_speed, obstacles, obstacle_speed, score, game_started, gap_between_obstacles

    window = init_window()
    if not window:
        return

    texture_id = load_texture("assets/mario_mexendo.gif")
    bg_texture_id = load_texture("assets/fundo_alternativo.png")
    cano_texture_id = load_texture("assets/cano_verde.png")

    if texture_id is None or bg_texture_id is None or cano_texture_id is None:
        glfw.terminate()
        return

    while not glfw.window_should_close(window):
        # Reinicia as variáveis para cada partida
        player_pos = [100, WINDOW_HEIGHT // 2]
        player_speed = 0
        obstacles = []
        obstacle_speed = 200
        score = 0
        gap_between_obstacles = 400
        game_started = False

        last_time = time.time()

        # Tela de introdução
        while not game_started and not glfw.window_should_close(window):
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            draw_background(bg_texture_id)
            # Exibe mensagem e score (mesmo que 0)
            draw_text(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2, "PRESSIONE ESPACO PARA INICIAR", font_size=24)
            draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}", font_size=24)
            glfw.swap_buffers(window)
            glfw.poll_events()
            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
                game_started = True
                player_pos = [100, WINDOW_HEIGHT // 2]
                obstacles = []
                last_time = time.time()

        # Loop do jogo em andamento
        while not glfw.window_should_close(window) and not check_collision():
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            update_player(delta_time, window)
            update_obstacles(delta_time)

            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            draw_background(bg_texture_id)
            # Desenha o jogador
            draw_player(texture_id, player_pos[0], player_pos[1])
            # Desenha os obstáculos
            for obs in obstacles:
                draw_obstacle_with_texture(obs['x'], obs['y_lower'], obs['width'], obs['height_lower'], cano_texture_id)
                draw_obstacle_inverted_texture(obs['x'], obs['y_upper'], obs['width'], obs['height_upper'], cano_texture_id)

            # Isola o desenho do score utilizando push/pop e utilizando glWindowPos2i
            glPushMatrix()
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            glColor3f(1.0, 1.0, 1.0)  # Garante cor branca
            draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}", font_size=24)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

            glfw.swap_buffers(window)
            glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
