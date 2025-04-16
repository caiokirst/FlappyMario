from game import *
from PIL import Image, ImageDraw, ImageFont

# Desenho do fundo
def desenhar_fundo(tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(LARGURA_JANELA, 0)
    glTexCoord2f(1, 1); glVertex2f(LARGURA_JANELA, ALTURA_JANELA)
    glTexCoord2f(0, 1); glVertex2f(0, ALTURA_JANELA)
    glEnd()

# Desenho do jogador
def desenhar_jogador(tex_id, x, y, largura=50, altura=50):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x+largura, y)
    glTexCoord2f(1, 1); glVertex2f(x+largura, y+altura)
    glTexCoord2f(0, 1); glVertex2f(x, y+altura)
    glEnd()

# Desenho dos obstáculos debaixo
def desenhar_obstaculo_com_textura(x, y, largura, altura, tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x+largura, y)
    glTexCoord2f(1, 1); glVertex2f(x+largura, y+altura)
    glTexCoord2f(0, 1); glVertex2f(x, y+altura)
    glEnd()

# Desenho dos obstáculos invertidos
def desenhar_obstaculo_invertido_com_textura(x, y, largura, altura, tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x+largura, y)
    glTexCoord2f(1, 0); glVertex2f(x+largura, y+altura)
    glTexCoord2f(0, 0); glVertex2f(x, y+altura)
    glEnd()

# Função para desenhar texto usando Pillow e glDrawPixels
def desenhar_texto(x, y, texto, tamanho_fonte=24):
    # Criação da imagem com o texto
    fonte = ImageFont.truetype("assets/SuperMario256.ttf", tamanho_fonte)
    bbox = fonte.getbbox(texto)
    largura, altura = bbox[2] - bbox[0], bbox[3] - bbox[1]
    imagem = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    desenhar = ImageDraw.Draw(imagem)
    desenhar.text((0, 0), texto, font=fonte, fill=(255, 255, 255, 255))
    dados_texto = imagem.transpose(Image.FLIP_TOP_BOTTOM).tobytes()

    # Desabilita texturização para garantir cores verdadeiras
    glDisable(GL_TEXTURE_2D)
    # Usa glWindowPos2i para definir a posição do texto em coordenadas da janela
    glWindowPos2i(x, y)
    glDrawPixels(largura, altura, GL_RGBA, GL_UNSIGNED_BYTE, dados_texto)
    glEnable(GL_TEXTURE_2D)
