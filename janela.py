from OpenGL.GL import *
import glfw


def inicializar_janela(LARGURA_JANELA, ALTURA_JANELA, titulo="Flappy Mario"):
    if not glfw.init():
        return None
    
    janela = glfw.create_window(LARGURA_JANELA, ALTURA_JANELA, titulo, None, None)
    if not janela:
        glfw.terminate()
        return None
    
    glfw.make_context_current(janela)

    # Configura o modo de projeção ortográfica
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, LARGURA_JANELA, 0, ALTURA_JANELA, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Configuração de cores e texturas
    glClearColor(0.5, 0.7, 0.9, 1.0)  # Cor de fundo da janela
    glEnable(GL_TEXTURE_2D)  # Ativa o uso de texturas
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)  # Modo de mistura de texturas
    glEnable(GL_BLEND)  # Ativa o blend para permitir transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Função de mistura para a transparência

    return janela
