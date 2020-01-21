# -*- coding: utf-8 -*-

"""

Snake do Rafa :)

Código desenvolvido para aprender sobre o funcionamento do PyGame.

Como todo código que se desenvolve enquanto está aprendendo, esse script
ficou muito bisonho e cheio de trechos de código inúteis.

Estou compartilhando porque talvez possa ajudar alguém ou incentivá-los
a estudarem programação.

Um abraço a todos!

"""

import os, sys, getopt

import random

import pygame
from pygame.locals import *

# Bibliotecas de desenho
from pygame.draw import line, circle, polygon

# Essa classe representa o ator "Fundo" do jogo
class Background:
    image = None
    
    def __init__(self):
        screen = pygame.display.get_surface()
        back = pygame.Surface(screen.get_size()).convert()
        back.fill((0, 0, 0))
        self.image = back
    # __init__()
    
    def update(self, dt):
        pass # ainda não faz nada
    # update()
    
    def draw(self, screen):
        screen.blit(self.image, (0, 0))
    # draw()
    
# Background

class Game:
    # Tela
    screen = None
    screen_size = None
    
    # Rodando?
    run = True
    
    # Velocidade do clock
    clock = 64
    
    # Fundo
    background = None
    
    # Última tecla pressionada
    tecla = None
    
    # BlockStep - Tamanho dos blocos e itens
    BS = 15
    
    # Vetores 'x' e 'y', responsáveis por guardar o local que a snake está
    x = [1]
    y = [1]
    
    # Valores máximos da mesa (será convertido em BS depois)
    x_max = 20
    y_max = 20
    
    # Define se já existe um objetivo na tela e onde está
    objNaTela = False
    obj_x = None
    obj_y = None
    
    # Define a direção da snake
    direcao = None
    
    # Define se a snake deve crescer
    crescer = False
    
    # Cores
    cor = {
           'verde': (0, 255, 0),
           'azul': (0, 0, 255),
           'vermelho': (255, 0, 0),
           'amarelo': (255,255,0),
           'cinza': (100, 100, 100)
           }
    
    # Pausa e fim de jogo
    pause = False
    gameover = False
    
    # Fonte para escrever na tela
    fonte = None
    
    # Mostrar fps na tela
    mostra_fps = True
    
    def __init__(self, size, fullscreen):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption e desabilitamos o mouse dentro desta.
        """
        actors = {}
        pygame.init()
        flags = DOUBLEBUF

        pygame.font.init()
        self.fonte = pygame.font.SysFont(None, 20)   

        if fullscreen:
            flags |= FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()
        
        pygame.mouse.set_visible(0)
        
        pygame.display.set_caption('Snake do Rafa :)');
    # init
    
    def handle_events(self):
        """
        Trata o evento e toma a ação necessária
        """
        
        for event in pygame.event.get():
            t = event.type
            if t in (KEYDOWN, KEYUP):
                self.tecla = k = event.key
                
            if t == QUIT:
                self.run = False
                
            elif t == KEYDOWN:
                if k == K_ESCAPE:
                    self.run = False
                elif k == K_RETURN:
                    self.pause = False if self.pause else True
                    
    # handle_events()
    
    def actors_update(self, dt):
        self.background.update(dt)
    # actors_update()
    
    def actors_draw(self):
        self.background.draw(self.screen)
        
        # Desenha a snake (semelhante ao 'for' do C)
        for i in range(len(self.x)):
            circle(self.screen,
                   self.cor['vermelho'] if i == 0 else self.cor['verde'], # Se for a primeira, vermelho. Senão, verde.
                   (self.x[i] * self.BS, self.y[i] * self.BS), # Posiciona na tela
                   self.BS / 2) # O raio do círculo é a metade do tamanho do bloco
    # actors_draw()
    
    def desenhaMesa(self):
        # Redução da margem para a snake não encostar na borda
        margem = 5
        
        # Pode ser melhorado com o uso do 'lines'
        
        # Cima
        pygame.draw.line(self.screen,
                         self.cor['cinza'],
                         [0, 0],
                         [self.screen_size[0],0],
                         self.BS - margem)
        
        # Esquerda
        pygame.draw.line(self.screen,
                         self.cor['cinza'],
                         [0, 0],
                         [0, self.screen_size[1]],
                         self.BS - margem)
        
        # Direita
        pygame.draw.line(self.screen,
                         self.cor['cinza'],
                         [self.screen_size[0] - margem, 0],
                         [self.screen_size[0] - margem, self.screen_size[1]],
                         self.BS)
        
        # Baixo 
        pygame.draw.line(self.screen,
                         self.cor['cinza'],
                         [0, self.screen_size[1] - margem / 2],
                         [self.screen_size[0], self.screen_size[1] - margem / 2],
                         self.BS - margem)

    def escreveFps(self, fps):
        label = self.fonte.render("FPS: %1.2f" % fps, 1, self.cor['amarelo'])
        self.screen.blit(label, (0, 0))
    # escreveFps()
    
    def movimentar(self):
        # Grava a última posição antes do movimento do corpo, caso necessite crescer
        ultimo_x = self.x[-1]
        ultimo_y = self.y[-1]
        
        # Verifica se existe corpo e, então, movimenta
        # Movimenta de trás pra frente para evitar sobreescrever posições
        if (len(self.x) > 1 and self.tecla):
            for i in reversed(range(1, len(self.x))):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
                
        # Crescer? 
        if (self.crescer):
            self.x.append(ultimo_x)
            self.y.append(ultimo_y)
            self.crescer = False

        # Realiza a movimentação
        if self.direcao == "up":
                self.y[0] -= 1
        elif self.direcao == "right":
                self.x[0] += 1
        elif self.direcao == "down":
                self.y[0] += 1
        elif self.direcao == "left":
                self.x[0] -= 1
        
        # Teste de colisão
        if self.x[0] == self.obj_x and self.y[0] == self.obj_y:
            self.crescer = True
            self.objNaTela = False

    # movimentar()
    
    def posicionaObj(self):
        if (not self.objNaTela):
            # Testa se o objetivo não será colocado dentro da snake
            dentro = True
            
            while dentro:
                dentro = False
                
                # +1 e -1 para nunca posicionar nas bordas
                self.obj_x = random.randint(1 + 1, self.x_max - 1)
                self.obj_y = random.randint(1 + 1, self.y_max - 1)
                
                for i in range(len(self.x)):
                    if self.obj_x == self.x[i] and self.obj_y == self.y[i]:
                        dentro = True
            # while
            
            self.objNaTela = True
        
        circle(self.screen,
               self.cor['azul'], # O objetivo é azul
               (self.obj_x * self.BS, self.obj_y * self.BS), # Posiciona na tela
               self.BS / 2) # O raio do círculo é a metade do tamanho do bloco
    
    def defineDirecao(self):
                # Realiza a movimentação
        if self.tecla == K_UP:
            if (self.direcao != "down"):
                self.direcao = "up"
        elif self.tecla == K_RIGHT:
            if (self.direcao != "left"):
                self.direcao = "right"
        elif self.tecla == K_DOWN:
            if (self.direcao != "up"):
                self.direcao = "down"
        elif self.tecla == K_LEFT:
            if (self.direcao != "right"):
                self.direcao = "left"
    
    def detectarColisao(self):
        morreu = False
        
        # Separei pra ficar mais fácil de visualizar
        if self.x[0] == 0 or self.y[0] == 0:
            morreu = True
            
        elif self.x[0] == self.screen_size[0] / self.BS or self.y[0] == self.screen_size[1] / self.BS:
            morreu = True
            
        else:
            # Testa se a cabeça da snake colidiu com alguma parte do corpo
            for i in range(1, len(self.x)):
                if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                    morreu = True
                    break
        
        if morreu:
            fonte = pygame.font.SysFont("Arial", 80)
            label = fonte.render("Fim de jogo :(" , 1, self.cor['cinza'])
            self.screen.blit(label, (75, 170))
            self.gameover = True
    
    def loop(self):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background()
        
        # Inicializamos o relógio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock = pygame.time.Clock()
        #dt = 16
        dt = self.clock
        
        # Assim iniciamos o loop principal do programa
        while self.run:
            clock.tick(1000/dt)
            
            # Manuseia eventos de input
            self.handle_events()
            
            if not self.pause and not self.gameover:
                # Atualiza elementos
                self.actors_update(dt)
                
                # Desenhe para o back buffer
                self.actors_draw()
                
                # Desenha a mesa
                self.desenhaMesa()
                                
                if (self.mostra_fps):
                    self.escreveFps(clock.get_fps())
            
                # Altera a direção, se necessário
                self.defineDirecao()
            
                # Movimenta a snake
                self.movimentar()
                
                self.detectarColisao()
            
                # Posiciona o objetivo
                self.posicionaObj()
            
                # Ao fim do desenho temos que trocar o front buffer e o back buffer
                pygame.display.flip()
            
            elif self.pause:
                fonte = pygame.font.SysFont("Arial", 80)
                label = fonte.render("Jogo pausado" , 1, self.cor['verde'])
                self.screen.blit(label, (75, 170))
                
                pygame.display.flip()
                
                pygame.display.flip()
            
            
        # while self.run
    # loop()
# Game

def usage():
    prog = sys.argv[0]
    
# usage()

def parse_opts(argv):
    """
    Pega as informações da linha de comando e retorna
    """
    # Analise a linha de comando usando 'getopt'
    try:
        opts, args = getopt.gnu_getopt(argv[1:],
                                        "hfr:",
                                        ["help",
                                         "fullscreen",
                                         "resolution="])
                                         
    except getopt.GetoptError:
        # Imprime as informações e sai
        usage()
        sys.exit(2)
        
    options = {
        "fullscreen": False,
        "resolution": (650, 480),
        }
        
    for o, a in opts:
        if o in ("-f", "--fullscreen"):
            options["fullscreen"] = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-r", "--resolution"):
            a = a.lower()
            r = a.split("x")
            if len(r) == 2:
                options["resolution"] = r
                continue

            r = a.split(",")
            if len(r) == 2:
                options["resolution"] = r
                continue

            r = a.split(":")
            if len(r) == 2:
                options["resolution"] = r
                continue

    # for o, a in opts
    r = options["resolution"]
    options["resolution"] = [ int(r[0]), int(r[1])]
    return options
# parse_opts()

def main(argv):
    """
    Primeiro vamos verificar se estamos no diretório certo para conseguir
    encontrar as imagens e outros recursos. Depois inicializar o pygame
    com as opções passadas pela linha de comando
    """
    fullpath = os.path.abspath(argv[0])
    diretorio = os.path.dirname(fullpath)
    os.chdir(diretorio)
    
    options = parse_opts(argv)
    game = Game(options["resolution"], options["fullscreen"])
    game.loop()
# main()

# Chama o main se estiver executando o script (não entendi exatamente...)
if __name__ == '__main__':
    main(sys.argv)