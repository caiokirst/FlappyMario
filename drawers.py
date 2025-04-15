from game import *

# Desenho do fundo
def draw_background(tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(WINDOW_WIDTH, 0)
    glTexCoord2f(1, 1); glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
    glTexCoord2f(0, 1); glVertex2f(0, WINDOW_HEIGHT)
    glEnd()

# Desenho do jogador
def draw_player(tex_id, x, y, width=50, height=50):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x+width, y)
    glTexCoord2f(1, 1); glVertex2f(x+width, y+height)
    glTexCoord2f(0, 1); glVertex2f(x, y+height)
    glEnd()

# Desenho dos obstáculos debaixo
def draw_obstacle_with_texture(x, y, width, height, tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x+width, y)
    glTexCoord2f(1, 1); glVertex2f(x+width, y+height)
    glTexCoord2f(0, 1); glVertex2f(x, y+height)
    glEnd()

# Desenho dos obstáculos invertidos
def draw_obstacle_inverted_texture(x, y, width, height, tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x+width, y)
    glTexCoord2f(1, 0); glVertex2f(x+width, y+height)
    glTexCoord2f(0, 0); glVertex2f(x, y+height)
    glEnd()

# Função para desenhar texto usando Pillow e glDrawPixels
def draw_text(x, y, text, font_size=32):
    # Criação da imagem com o texto
    font = ImageFont.truetype("assets/SuperMario256.ttf", font_size)
    bbox = font.getbbox(text)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=(255, 255, 255, 255))
    text_data = image.transpose(Image.FLIP_TOP_BOTTOM).tobytes()

    # Desabilita texturização para garantir cores verdadeiras
    glDisable(GL_TEXTURE_2D)
    # Usa glWindowPos2i para definir a posição do texto em coordenadas da janela
    glWindowPos2i(x, y)
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glEnable(GL_TEXTURE_2D)