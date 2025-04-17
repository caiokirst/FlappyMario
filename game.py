from configs import *
from texturas import *
from janela import *
from logica import *
from drawers import *
from highscore import *
# pip install glfw PyOpenGL Pillow

# Variáveis globais
posicao_jogador = [POSICAO_INICIAL_JOGADOR_X, POSICAO_INICIAL_JOGADOR_Y]
gravidade = GRAVIDADE
velocidade_pulo = VELOCIDADE_PULO
velocidade_obstaculo = VELOCIDADE_OBSTACULO
espaco_entre_obstaculos = ESPACO_ENTRE_OBSTACULOS
vidas = VIDAS_INICIAIS

# Função principal
def main():
    criar_arquivo_highscore()
    janela = inicializar_janela(LARGURA_JANELA, ALTURA_JANELA)
    if not janela:
        return

    recursos = carregar_recursos()
    if recursos is None:
        glfw.terminate()
        return

    while not glfw.window_should_close(janela):
        estado = resetar_estado()
        
        desenhar_menu_inicial(janela, recursos, estado)
        
        loop_do_jogo(janela, recursos, estado)
        
        desenhar_tela_fim(janela, recursos, estado)

    glfw.terminate()

if __name__ == "__main__":
    main()
