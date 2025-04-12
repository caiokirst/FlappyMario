from OpenGL.GL import *

# Função para desenhar o HUD
def render_hud(score_texture, score_width, score_height, lives_texture, lives_width, lives_height):
    glColor3f(1, 1, 1)  # Cor do texto (branco)
    draw_text(score_texture, 10, 570, score_width, score_height)  # Score no topo esquerdo
    draw_text(lives_texture, 10, 540, lives_width, lives_height)  # Vidas logo abaixo do score

# Função para desenhar o texto (usando textura)
def draw_text(texture_id, x, y, width, height):
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
