# Configurações da Janela
LARGURA_JANELA = 800
ALTURA_JANELA = 600

# Configurações do Jogador
ALTURA_MARIO = ALTURA_JANELA * 0.1
LARGURA_MARIO = LARGURA_JANELA * 0.075
POSICAO_INICIAL_JOGADOR_X = 100
POSICAO_INICIAL_JOGADOR_Y = ALTURA_JANELA // 2
GRAVIDADE = -(ALTURA_JANELA * 1.5)
VELOCIDADE_PULO = ALTURA_JANELA / 2.25

# Configurações dos Obstáculos
VELOCIDADE_OBSTACULO = 200
ESPACO_ENTRE_OBSTACULOS = ALTURA_JANELA
GAP_INICIAL = ALTURA_JANELA * 0.2
LARGURA_OBSTACULO = LARGURA_JANELA * 0.2
ALTURA_OBSTACULO = ALTURA_JANELA * 0.2

# Vidas do Jogador
VIDAS_INICIAIS = 3
VIDAS_MAX = 5

# Caminhos das Texturas
CAMINHO_TEX_JOGADOR = "assets/mario_mexendo.gif"
CAMINHO_TEX_FUNDO = "assets/fundo_super_mario.png"
CAMINHO_TEX_CANO = "assets/cano_verde.png"
CAMINHO_TEX_CORACAO = "assets/coracao.png"

# Spawn de corações
TEMPO_ENTRE_CORACOES = 10   # em segundos
TAMANHO_CORACAO      = 40   # em pixels

# Margem do topo e do chão para spawn de corações
MARGEM_SPAWN_CORACAO = 100

# Configurações do Highscore
ARQUIVO_HIGHSCORE = "assets/highscore.txt"

# Configurações do Texto
TAMANHO_FONTE = 24
COR_TEXTO = (255, 255, 255, 255)
FUNDO = False
COR_FUNDO = (0, 0, 0, 30)
PADDING = 8
SOMBRA = True
COR_SOMBRA = (0, 0, 0, 150)
CONTORNO = True
COR_CONTORNO = (0, 0, 0, 255)
ESPESSURA_CONTORNO = 2
FUNDO_ARREDONDADO = True
RAIO_BORDA = 10
