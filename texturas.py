from OpenGL.GL import *
from PIL import Image

# Função para carregar uma textura de uma imagem
def carregar_textura(caminho):
    try:
        # Tenta abrir a imagem a partir do caminho fornecido
        imagem = Image.open(caminho)
    except IOError:
        # Caso ocorra um erro ao carregar a imagem, imprime uma mensagem e retorna None
        print("Erro ao carregar a imagem:", caminho)
        return None

    # Inverte a imagem verticalmente para compatibilidade com OpenGL
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    # Converte a imagem para o formato RGBA e obtém os dados da imagem
    dados_img = imagem.convert("RGBA").tobytes()
    
    # Obtém as dimensões da imagem
    largura, altura = imagem.size

    # Gera uma nova textura
    id_textura = glGenTextures(1)
    
    # Ativa a textura para binding
    glBindTexture(GL_TEXTURE_2D, id_textura)
    
    # Carrega a imagem na textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados_img)
    
    # Define o filtro de minificação e magnificação da textura
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return id_textura

# Função para carregar todos os frames de um GIF
def carregar_frames_gif(CAMINHO_TEX_JOGADOR):
    # Abre o GIF especificado pelo caminho
    gif = Image.open(CAMINHO_TEX_JOGADOR)
    
    frames = []
    try:
        # Tenta carregar todos os frames do GIF
        while True:
            frame = gif.copy().convert("RGBA")  # Converte o frame para o formato RGBA
            frames.append(frame)  # Adiciona o frame à lista
            gif.seek(gif.tell() + 1)  # Avança para o próximo frame
    except EOFError:
        # Finaliza a captura quando não houver mais frames
        pass
    
    return frames
