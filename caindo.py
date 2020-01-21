# coding:utf-8
# caminhando.py

import pygame
import os
from pygame.locals import *

# Inicia o pygame
pygame.init()

# Tela de 640x480
tela = pygame.display.set_mode((640,480))
pygame.display.set_caption("Jogo do Boneco Caminhando")

# Prepara o fundo para ser utilizado
fundo = pygame.Surface((640,480))
fundo = fundo.convert()
fundo.fill((0,0,0))

# Carrega e prepara o fundo
arq_fundo = os.path.join('sprites','fundo.png')
img_fundo = pygame.image.load(arq_fundo)
img_fundo = img_fundo.convert()

# Carrega e prepara o chão
arq_chao = os.path.join('sprites', 'chao.png')
img_chao = pygame.image.load(arq_chao)
img_chao = img_chao.convert()

# Carrega o sprite do boneco
arq_boneco = os.path.join('sprites', 'boneco.png')
boneco = pygame.image.load(arq_boneco)
#boneco = boneco.convert()

# Prepara o clock para ser usado
clock = pygame.time.Clock()

# X inicial do personagem
pers_x = 10

# Movimento sendo executado (0 = parado)
mov = 0

# Ação da animação
acao = 0

# Para qual lado o personagem está indo
indo_para = "direita"

# Se o personagem está correndo
correndo = False

# Máximo FPS do jogo
fps = 80

# Contagem de frames da animação
contagem_frames = 0

# Loop do jogo
while True:
    # Verifica os eventos do teclado
    for evt in pygame.event.get():
        # Se for pra sair (X no canto ou ESC)
        if evt.type == QUIT or (evt.type == KEYDOWN and evt.key == K_ESCAPE):
            exit()

        if evt.type == KEYDOWN:
            # Direita
            if evt.key == K_RIGHT:
                mov = +1
            # Esquerda
            elif evt.key == K_LEFT:
                mov = -1
            # Shift
            if evt.key == K_LSHIFT:
                correndo = True
        # Se soltar a tecla
        if evt.type == KEYUP:
            if evt.key != K_LSHIFT:
                mov = 0
            # Se tiver soltado o SHIFT...
            else:
                correndo = False

    # Tempo para animar o personagem
    tempo = clock.tick(fps) / 10.0

    # Se não houver movimentação
    if mov == 0:
        acao = 0
    # Se houver movimentação
    else:
        if contagem_frames > fps / 7:
            contagem_frames = 0
            # 3 estados e animação 0,1,2
            if acao > 2:
                acao = 0
            # Se não for o último estado, avança
            else:
                acao += 1
        else:
            contagem_frames += 1

    # Desenha o fundo
    tela.blit(img_fundo, (0,0))
    tela.blit(img_fundo, (416,0))
    tela.blit(img_fundo, (0,416))
    tela.blit(img_fundo, (416,416))

    # Desenha o chão
    tela.blit(img_chao, (0, 390))
    tela.blit(img_chao, (416, 390))

    # Adiciona o movimento
    if not correndo:
        pers_x += mov * tempo
    else:
        pers_x += mov * tempo * 3

    # Recorta a animação atual do boneco
    personagem = boneco.subsurface(Rect(64*acao,0,64,64))

    # Para esquerda ou para direita?
    if mov < 0:
        indo_para = "esquerda"
    elif mov > 0:
        indo_para = "direita"

    if indo_para == "esquerda":
        personagem = pygame.transform.flip(personagem, True, False)

    # Imprime o personagem na tela
    tela.blit(personagem,(pers_x,370))

    pygame.display.flip()