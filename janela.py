import glfw
from OpenGL.GL import *

def inicializar_janela(LARGURA_JANELA, ALTURA_JANELA, titulo="Flappy Mario"):
    if not glfw.init():
        return None
    janela = glfw.create_window(LARGURA_JANELA, ALTURA_JANELA, titulo, None, None)
    if not janela:
        glfw.terminate()
        return None
    glfw.make_context_current(janela)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, LARGURA_JANELA, 0, ALTURA_JANELA, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0.5, 0.7, 0.9, 1.0)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    return janela
