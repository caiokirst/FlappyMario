from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np


# Função para carregar uma textura
def load_texture(image_path):
    img = Image.open(image_path)
    img_data = np.array(list(img.getdata()), np.uint8)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id


# Função para gerar a textura com o texto
def render_text_to_texture(text, font_path="arial.ttf", font_size=20):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new("RGBA", (len(text) * font_size, font_size * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=(255, 255, 255, 255))

    img_data = image.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()
    width, height = image.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id, width, height


# Função para desenhar o fundo
def draw_background(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(800, 0)
    glTexCoord2f(1, 1)
    glVertex2f(800, 600)
    glTexCoord2f(0, 1)
    glVertex2f(0, 600)
    glEnd()


# Função para desenhar o jogador
def draw_player(texture_id, x, y):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + 50, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + 50, y + 50)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + 50)
    glEnd()


# Função para desenhar um obstáculo
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
