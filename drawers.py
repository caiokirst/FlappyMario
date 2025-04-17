from game import *
from configs import *
from PIL import Image, ImageDraw, ImageFont


# --- Funções de Desenho 2D ---

# Desenha o fundo com textura
def desenhar_fundo(tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(LARGURA_JANELA, 0)
    glTexCoord2f(1, 1); glVertex2f(LARGURA_JANELA, ALTURA_JANELA)
    glTexCoord2f(0, 1); glVertex2f(0, ALTURA_JANELA)
    glEnd()

# Desenha o jogador com textura
def desenhar_jogador(tex_id, x, y):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + LARGURA_MARIO, y)
    glTexCoord2f(1, 1); glVertex2f(x + LARGURA_MARIO, y + ALTURA_MARIO)
    glTexCoord2f(0, 1); glVertex2f(x, y + ALTURA_MARIO)
    glEnd()

# Desenha um obstáculo normal com textura
def desenhar_obstaculo_com_textura(x, y, largura, altura, tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + largura, y)
    glTexCoord2f(1, 1); glVertex2f(x + largura, y + altura)
    glTexCoord2f(0, 1); glVertex2f(x, y + altura)
    glEnd()

# Desenha um obstáculo invertido com textura
def desenhar_obstaculo_invertido_com_textura(x, y, largura, altura, tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glTexCoord2f(1, 1); glVertex2f(x + largura, y)
    glTexCoord2f(1, 0); glVertex2f(x + largura, y + altura)
    glTexCoord2f(0, 0); glVertex2f(x, y + altura)
    glEnd()

# --- Funções de Desenho de Texto ---

# Função para desenhar texto com configurações personalizáveis usando Pillow
def desenhar_texto(x, y, texto, tamanho_fonte=TAMANHO_FONTE, cor_texto=COR_TEXTO,
                   fundo=FUNDO, cor_fundo=COR_FUNDO, padding=PADDING, sombra=SOMBRA, cor_sombra=COR_SOMBRA,
                   contorno=CONTORNO, cor_contorno=COR_CONTORNO, espessura_contorno=ESPESSURA_CONTORNO,
                   fundo_arredondado=FUNDO_ARREDONDADO, raio_borda=RAIO_BORDA):

    # Criar a fonte
    fonte = ImageFont.truetype("assets/SuperMario256.ttf", tamanho_fonte)
    
    # Calcular o tamanho do texto
    bbox = fonte.getbbox(texto)
    largura_texto = bbox[2] - bbox[0]
    altura_texto = bbox[3] - bbox[1]

    # Tamanho total do fundo
    largura_total = largura_texto + 2 * padding
    altura_total = altura_texto + 2 * padding

    # Criar a imagem de fundo
    imagem = Image.new("RGBA", (largura_total, altura_total), (0, 0, 0, 0))
    desenhar = ImageDraw.Draw(imagem)

    # Desenhar o fundo (com ou sem bordas arredondadas)
    if fundo:
        if fundo_arredondado:
            desenhar.rounded_rectangle([0, 0, largura_total, altura_total], radius=raio_borda, fill=cor_fundo)
        else:
            desenhar.rectangle([0, 0, largura_total, altura_total], fill=cor_fundo)

    # Desenhar a sombra do texto
    if sombra:
        sombra_offset = 2
        desenhar.text((padding + sombra_offset, padding + sombra_offset), texto, font=fonte, fill=cor_sombra)

    # Desenhar o contorno do texto
    if contorno:
        for dx in range(-espessura_contorno, espessura_contorno + 1):
            for dy in range(-espessura_contorno, espessura_contorno + 1):
                if dx != 0 or dy != 0:
                    desenhar.text((padding + dx, padding + dy), texto, font=fonte, fill=cor_contorno)

    # Desenhar o texto principal
    desenhar.text((padding, padding), texto, font=fonte, fill=cor_texto)

    # Converter a imagem para bytes e desenhar no OpenGL
    dados_texto = imagem.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
    glDisable(GL_TEXTURE_2D)
    glWindowPos2i(x, y)
    glDrawPixels(largura_total, altura_total, GL_RGBA, GL_UNSIGNED_BYTE, dados_texto)
    glEnable(GL_TEXTURE_2D)
