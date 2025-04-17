from OpenGL.GL import *
from PIL import Image

def carregar_textura(caminho):
    try:
        imagem = Image.open(caminho)
    except IOError:
        print("Erro ao carregar a imagem:", caminho)
        return None

    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
    dados_img = imagem.convert("RGBA").tobytes()
    largura, altura = imagem.size

    id_textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, dados_img)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return id_textura

def carregar_frames_gif(CAMINHO_TEX_JOGADOR):
    gif = Image.open(CAMINHO_TEX_JOGADOR)
    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGBA")
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames