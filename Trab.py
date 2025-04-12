import glfw
from OpenGL.GL import *
from PIL import Image, ImageFont, ImageDraw
import time
import random

# Configurações da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Variáveis do jogo
player_pos = [100, WINDOW_HEIGHT // 2]
player_speed = 0
gravity = -600
jump_speed = 300
last_time = 0
obstacles = []
obstacle_speed = 200  # velocidade inicial
score = 0
game_started = False
gap_between_obstacles = 400  # começa com espaçamento maior

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

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

def draw_text(x, y, text, font_size=32):
    font = ImageFont.truetype("assets/SuperMario256.ttf", font_size)
    bbox = font.getbbox(text)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=(255, 255, 255, 255))

    text_data = image.transpose(Image.FLIP_TOP_BOTTOM).tobytes()

    glRasterPos2f(x, y)
    glColor3f(1.0, 1.0, 1.0)  # Define a cor branca antes de desenhar
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# Inicialização da janela
def init_window():
    if not glfw.init():
        return None
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Flappy Mario", None, None)
    if not window:
        glfw.terminate()
        return None
    glfw.make_context_current(window)

    # Configuração de projeção para modo ortográfico (2D)
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

# Desenho do fundo e personagens
def draw_background(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(WINDOW_WIDTH, 0)
    glTexCoord2f(1, 1)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
    glTexCoord2f(0, 1)
    glVertex2f(0, WINDOW_HEIGHT)
    glEnd()

def draw_player(texture_id, x, y, width=50, height=50):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + height)
    glEnd()

def draw_obstacle_with_texture(x, y, width, height, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + height)
    glEnd()

def draw_obstacle_inverted_texture(x, y, width, height, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(x, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0)
    glVertex2f(x, y + height)
    glEnd()

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

def update_obstacles(delta_time):
    global obstacles, score, obstacle_speed, gap_between_obstacles

    for obs in obstacles:
        obs['x'] -= obstacle_speed * delta_time

    obstacles[:] = [obs for obs in obstacles if obs['x'] + obs['width'] > 0]

    if not obstacles or (WINDOW_WIDTH - obstacles[-1]['x']) > gap_between_obstacles:
        obstacle_width = 100
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
            'width': obstacle_width
        }

        obstacles.append(new_obs)
        score += 1

        # Aumenta velocidade até 400
        obstacle_speed = min(400, 200 + score * 2)

        # Diminui espaçamento gradualmente até 200
        gap_between_obstacles = max(200, 400 - score * 4)

def check_collision():
    player_rect = (player_pos[0] + 10, player_pos[1] + 10, 30, 30)  # margem de 10 px
    for obs in obstacles:
        lower = (obs['x'], obs['y_lower'], obs['width'], obs['height_lower'])
        upper = (obs['x'], obs['y_upper'], obs['width'], obs['height_upper'])
        if rect_collision(player_rect, lower) or rect_collision(player_rect, upper):
            return True
    return False

def rect_collision(r1, r2):
    x1, y1, w1, h1 = r1
    x2, y2, w2, h2 = r2
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

# Principal
def main():
    global last_time, texture_id, bg_texture_id, cano_texture_id
    global player_pos, player_speed, obstacles, obstacle_speed, score, game_started, gap_between_obstacles

    window = init_window()
    if not window:
        return

    texture_id = load_texture("assets/super_mario.png")
    bg_texture_id = load_texture("assets/fundo_super_mario.jpg")
    cano_texture_id = load_texture("assets/cano_verde.png")

    if texture_id is None or bg_texture_id is None or cano_texture_id is None:
        glfw.terminate()
        return

    while not glfw.window_should_close(window):
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

            # Exibe a mensagem para pressionar espaço para iniciar
            draw_text(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2, "PRESSIONE ESPACO PARA INICIAR", font_size=24)

            # Exibe o score no canto superior esquerdo (mesmo que o jogo não tenha começado)
            draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}", font_size=24)

            glfw.swap_buffers(window)
            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
                game_started = True
                player_pos = [100, WINDOW_HEIGHT // 2]
                obstacles = []

        # Começo do jogo
        last_time = time.time()
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

            # Exibe o score no canto superior esquerdo
            draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}", font_size=24)

            glfw.swap_buffers(window)
            glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
