from PIL import Image, ImageDraw, ImageFont
from configs import *
from OpenGL.GL import *
from highscore import *
import os
import glfw
import time

from texturas import carregar_textura_transparente


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

def desenhar_coracao(tex_id, x, y):
    size = TAMANHO_CORACAO
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x,       y)
    glTexCoord2f(1, 0); glVertex2f(x+size,  y)
    glTexCoord2f(1, 1); glVertex2f(x+size,  y+size)
    glTexCoord2f(0, 1); glVertex2f(x,       y+size)
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

# --- Funções de Tela do Jogo ---

# Função para desenhar o menu inicial
def desenhar_menu(janela, recursos, estado):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    desenhar_fundo(recursos["fundo"])

    # Exibe o highscore
    if os.path.exists(ARQUIVO_HIGHSCORE):
        pontuacoes = get_pontuacoes()
        desenhar_texto(LARGURA_JANELA // 2 - 120, ALTURA_JANELA // 2 + 80, "TOP 3 PONTUACOES:")
        if not pontuacoes:
            desenhar_texto(LARGURA_JANELA // 2 - 190, ALTURA_JANELA // 2 + 50, "Nenhuma registrada ainda")
        else:
            for i, (valor_pontuacao, data) in enumerate(pontuacoes, start=1):
                desenhar_texto(LARGURA_JANELA // 2 - 160, ALTURA_JANELA // 2 + (50 - i * 30),
                               f"{i}. {valor_pontuacao} - {data}")

    desenhar_texto(LARGURA_JANELA // 2 - 220, ALTURA_JANELA // 2 - 80, "PRESSIONE ESPACO PARA INICIAR")
    desenhar_texto(10, ALTURA_JANELA - 40, f"Pontuacao: {estado['pontuacao']}")
    desenhar_texto(LARGURA_JANELA - 140, ALTURA_JANELA - 40, f"Vidas: {estado['vidas']}")
    
    glfw.swap_buffers(janela)
    glfw.poll_events()

# Função para mostrar o menu inicial até que o jogo seja iniciado
def desenhar_menu_inicial(janela, recursos, estado):
    while not estado["jogo_iniciado"] and not glfw.window_should_close(janela):
        desenhar_menu(janela, recursos, estado)
        if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
            estado["jogo_iniciado"] = True
            estado["posicao_jogador"] = [POSICAO_INICIAL_JOGADOR_X, ALTURA_JANELA // 2]
            estado["obstaculos"] = []
            estado["ultimo_tempo"] = time.time()

# Função para desenhar o estado do jogo (jogador, obstáculos, pontuação, etc.)
def desenhar_jogo(janela, recursos, estado):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    desenhar_fundo(recursos["fundo"])

    # Piscando quando invencível
    if estado["invencivel"]:
        tempo_decorrido = time.time() - estado["tempo_invencivel"]
        if tempo_decorrido > 2:  # Tempo de invencibilidade em segundos
            estado["invencivel"] = False
            alpha = 1.0
        else:
            alpha = 0.3 if int(tempo_decorrido * 10) % 2 == 0 else 1.0
    else:
        alpha = 1.0

    # Recarregar a textura com a transparência adequada
    recursos["jogador"] = carregar_textura_transparente(CAMINHO_TEX_JOGADOR, alpha)

    # Desenha o jogador (com transparência se invencível)
    desenhar_jogador(recursos["jogador"], estado["posicao_jogador"][0], estado["posicao_jogador"][1])

    for obstaculo in estado["obstaculos"]:
        desenhar_obstaculo_com_textura(obstaculo['x'], obstaculo['y_inferior'],
                                       obstaculo['largura'], obstaculo['altura_inferior'], recursos["cano"])
        desenhar_obstaculo_invertido_com_textura(obstaculo['x'], obstaculo['y_superior'],
                                                 obstaculo['largura'], obstaculo['altura_superior'], recursos["cano"])

    for cor in estado["coracoes"]:
        desenhar_coracao(recursos["coracao"], cor["x"], cor["y"])

    desenhar_texto(10, ALTURA_JANELA - 40, f"Pontuacao: {estado['pontuacao']}")
    desenhar_texto(LARGURA_JANELA - 140, ALTURA_JANELA - 40, f"Vidas: {estado['vidas']}")

    glfw.swap_buffers(janela)
    glfw.poll_events()


# Função para mostrar a tela de fim de jogo e salvar a pontuação, se necessário
def desenhar_tela_fim(janela, recursos, estado):
    if estado["vidas"] <= 0 and estado["pontuacao"] > 0:
        salvar_pontuacao(estado["pontuacao"])
    
    while not estado["jogo_iniciado"] and not glfw.window_should_close(janela) and estado["vidas"] <= 0:
        glClear(GL_COLOR_BUFFER_BIT)
        desenhar_fundo(recursos["fundo"])
        desenhar_texto(LARGURA_JANELA // 2 - 100, ALTURA_JANELA // 2 + 40, "FIM DE JOGO!")
        desenhar_texto(LARGURA_JANELA // 2 - 120, ALTURA_JANELA // 2, f"PONTUACAO FINAL: {estado['pontuacao']}")
        desenhar_texto(LARGURA_JANELA // 2 - 220, ALTURA_JANELA // 2 - 40, "Pressione ESPACO para reiniciar")
        desenhar_texto(LARGURA_JANELA // 2 - 180, ALTURA_JANELA // 2 - 80, "Pressione ESC para sair")
        
        glfw.swap_buffers(janela)
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
            estado["jogo_iniciado"] = True
        elif glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)
