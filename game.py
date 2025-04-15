import glfw
from OpenGL.GL import *
from PIL import Image, ImageFont, ImageDraw
import time
import random
from drawers import *
from highscore import *
#pip install glfw PyOpenGL Pillow

# Configurações da janela
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Variáveis do jogo
player_pos = [100, WINDOW_HEIGHT // 2]
player_speed = 0
gravity = -900
jump_speed = 250
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

    # Adiciona novo obstáculo com altura variável
    if not obstacles or (WINDOW_WIDTH - obstacles[-1]['x']) > gap_between_obstacles:
        obstacle_width = 120  # Reduzi a largura
        gap = 120  # Menor espaço entre canos
        min_height = 50
        max_height = WINDOW_HEIGHT - gap - 50

        height_lower = random.randint(min_height, max_height)
        y_upper = height_lower + gap
        height_upper = WINDOW_HEIGHT - y_upper

        new_obs = {
            'x': WINDOW_WIDTH + 100,
            'y_upper': y_upper,
            'height_upper': height_upper,
            'y_lower': 0,
            'height_lower': height_lower,
            'width': obstacle_width,
            'scored': False
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

    # Garante que o arquivo de highscores exista
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w") as f:
            pass

    window = init_window()
    if not window:
        return

    texture_id = load_texture("assets/mario_mexendo.gif")
    bg_texture_id = load_texture("assets/fundo_super_mario.jpg")
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

            # Exibe highscores se o arquivo existir
            if os.path.exists(HIGHSCORE_FILE):
                highscores = get_highscores()
                draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 80, "TOP 3 SCORES:", font_size=24)

                if not highscores:
                    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, "Nenhum registrado ainda", font_size=20)
                else:
                    for i, (score_value, date) in enumerate(highscores, start=1):
                        draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + (50 - i * 30),
                                  f"{i}. {score_value} - {date}", font_size=20)

            draw_text(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 80, "PRESSIONE ESPACO PARA INICIAR", font_size=24)
            draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}", font_size=24)

            glfw.swap_buffers(window)
            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
                game_started = True
                player_pos = [100, WINDOW_HEIGHT // 2]
                obstacles = []
                last_time = time.time()

        # Loop do jogo em andamento
        while not glfw.window_should_close(window) and game_started:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            update_player(delta_time, window)
            update_obstacles(delta_time)

            if check_collision():
                game_started = False

            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            draw_background(bg_texture_id)
            draw_player(texture_id, player_pos[0], player_pos[1])
            for obs in obstacles:
                draw_obstacle_with_texture(obs['x'], obs['y_lower'], obs['width'], obs['height_lower'], cano_texture_id)
                draw_obstacle_inverted_texture(obs['x'], obs['y_upper'], obs['width'], obs['height_upper'], cano_texture_id)

            glPushMatrix()
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            glColor3f(1.0, 1.0, 1.0)
            draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}", font_size=24)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

            glfw.swap_buffers(window)
            glfw.poll_events()

        # Tela de Game Over
        if score > 0:
            save_highscore(score)

        while not game_started and not glfw.window_should_close(window):
            glClear(GL_COLOR_BUFFER_BIT)
            draw_background(bg_texture_id)

            draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40, "GAME OVER!", font_size=32)
            draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, f"Score final: {score}", font_size=24)
            draw_text(WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT // 2 - 40, "Pressione ESPACO para reiniciar", font_size=20)
            draw_text(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 80, "Pressione ESC para sair", font_size=20)

            glfw.swap_buffers(window)
            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
                game_started = True
            elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(window, True)

    glfw.terminate()



if __name__ == "__main__":
    main()
