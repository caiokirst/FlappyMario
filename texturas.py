from OpenGL.GL import *
from PIL import Image
from configs import *

# Função para carregar uma textura de imagem para uso no OpenGL
def carregar_textura(caminho):
    try:
        # Tenta abrir a imagem com o caminho fornecido
        imagem = Image.open(caminho)
    except IOError:
        # Se ocorrer erro, exibe mensagem e retorna None
        print("Erro ao carregar a imagem:", caminho)
        return None

    # Inverte a imagem verticalmente (necessário para o OpenGL)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    # Converte a imagem para RGBA e extrai os dados em bytes
    dados_img = imagem.convert("RGBA").tobytes()
    largura, altura = imagem.size  # Obtém dimensões

    # Gera uma nova textura no OpenGL
    id_textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_textura)  # Ativa a textura

    # Envia os dados da imagem para o OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados_img)

    # Define filtros de textura (suavização)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return id_textura  # Retorna o ID da textura criada

# Função para carregar todos os frames de um GIF
def carregar_frames_gif(CAMINHO_TEX_JOGADOR):
    gif = Image.open(CAMINHO_TEX_JOGADOR)  # Abre o arquivo GIF
    frames = []

    try:
        # Tenta extrair todos os frames do GIF
        while True:
            frame = gif.copy().convert("RGBA")  # Converte o frame para RGBA
            frames.append(frame)  # Adiciona o frame à lista
            gif.seek(gif.tell() + 1)  # Vai para o próximo frame
    except EOFError:
        # Quando não houver mais frames, encerra o loop
        pass

    return frames  # Retorna todos os frames carregados

def aplicar_imagem_transparente(imagem, alpha):
    imagem = imagem.convert("RGBA")  # Converte a imagem para o formato RGBA
    datas = imagem.getdata()

    nova_imagem = []
    for item in datas:
        # Alterando o valor alpha
        nova_imagem.append((item[0], item[1], item[2], int(item[3] * alpha)))

    imagem.putdata(nova_imagem)
    return imagem


def carregar_textura_transparente(caminho_imagem, alpha=1.0):
    # Carrega a imagem usando Pillow
    imagem = Image.open(caminho_imagem)

    # Aplica a transparência
    imagem_transparente = aplicar_imagem_transparente(imagem, alpha)

    # Converte a imagem em uma textura OpenGL
    largura, altura = imagem_transparente.size
    imagem_transparente = imagem_transparente.tobytes("raw", "RGBA", 0, -1)

    # Gerar uma textura OpenGL
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, imagem_transparente)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id


# Função para carregar todas as texturas necessárias para o jogo
def carregar_recursos():
    recursos = {
        "jogador": carregar_textura(CAMINHO_TEX_JOGADOR),
        "fundo": carregar_textura(CAMINHO_TEX_FUNDO),
        "cano": carregar_textura(CAMINHO_TEX_CANO)
    }

    # Verifica se alguma textura falhou ao carregar
    if None in recursos.values():
        return None  # Retorna None se algum recurso estiver faltando

    return recursos  # Retorna o dicionário com todos os recursos
