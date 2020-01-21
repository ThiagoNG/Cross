import pygame
import os
import time

# Tamanho da tela do jogo
size = width, height = 500, 836

pygame.init()

# Definie a Tela em 500x836
screen = pygame.display.set_mode(size)

pygame.display.set_caption("CrossEnglish")

# Carrega e prepara o teclado
arq_teclado = os.path.join('sprites', 'teclado.jpg')
img_teclado = pygame.image.load(arq_teclado)
img_teclado = img_teclado.convert()

# Carrega e prepara o fundo
arq_fundo = os.path.join('sprites', 'patrulha1.jpg')
img_fundo = pygame.image.load(arq_fundo)
img_fundo = img_fundo.convert()

# Carrega e prepara o quadrado das respostas
arq_squad = os.path.join('sprites','quadrado.png')
img_squad = pygame.image.load(arq_squad)
img_squad = img_squad.convert()

yellow_img_squad = pygame.image.load('ball.bmp')
yellow_img_squad = yellow_img_squad.convert()

# Carrega e prepara o retângulo das perguntas
arq_asq = os.path.join('sprites','perguntas.png')
#arq_asq = os.path.join('sprites','perguntas_first.png')
img_asq = pygame.image.load(arq_asq)
img_asq = img_asq.convert_alpha()

# Carrega e prepara a estrela da pontuação
arq_star = os.path.join('sprites','star1.png')
img_star = pygame.image.load(arq_star)
img_star = img_star.convert_alpha()

# Carrega e prepara o coração das vidas
arq_heart = os.path.join('sprites','heart.png')
img_heart = pygame.image.load(arq_heart)
img_heart = img_heart.convert_alpha()

pos_x = 0
pos_y = 0

# Define as cores que serão usadas no jogo
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,179)
SCORE = (0, 0, 139)

# Define as fontes que serão usadas no jogo
font = pygame.font.SysFont('comicsansms',40, True, False)
font1 = pygame.font.SysFont('Calibri',20, True, False)
#font2 = pygame.font.SysFont('comicsansm',26, True, False)
font2 = pygame.font.SysFont('Calibri',18, True, True)
fontscore = pygame.font.SysFont('comicsansms',25)

# Carrega em um array as coordenadas do teclado
coordinates = [
    (5, 45, 520, 578, "Q"),
    (55, 95, 520, 578, "W"),
    (105,145,520,578,"E"),
    (155,195,520,578,"R"),
    (205,245,520,578,"T"),
    (255,295,520,578,"Y"),
    (305,345,520,578,"U"),
    (355,395,520,578,"I"),
    (405,445,520,578,"O"),
    (455,495,520,578,"P"),
    (30,75,605,660,"A"),
    (80,120,605,660,"S"),
    (130,170,605,660,"D"),
    (180,220,605,660,"F"),
    (230,270,605,660,"G"),
    (280,320,605,660,"H"),
    (330,370,605,660,"J"),
    (380,420,605,660,"K"),
    (430,470,605,660,"L"),
    (80,120,685,745,"Z"),
    (130,170,685,745,"X"),
    (180,220,685,745,"C"),
    (230,270,685,745,"V"),
    (280,320,685,745,"B"),
    (330,370,685,745,"N"),
    (380,420,685,745,"M")
]

# Carrega a imagem do teclado   
screen.blit(img_teclado, (0,500))

# Carrega a imagem do fundo   
screen.blit(img_fundo,(0,0,500,500))

# Carrega a imagem da estrela
screen.blit(img_star, (360,10))

# Carrega a imagem das vidas
screen.blit(img_heart, (10,12))
screen.blit(img_heart, (50,12))
screen.blit(img_heart, (90,12))
screen.blit(img_heart, (130,12))
screen.blit(img_heart, (170,12))

valores_q = ''
valores_a = ''

pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)

class Estado:
    def __init__(self):
        self.horizontal = 220
        self.vertical = 70
        self.texto = ''
        
        self.ntry = 1
     
        self.nanswer = 0
        self.nscore = 0
        self.sound1 = pygame.mixer.Sound("sounds/musica.wav")

        
        pygame.mixer.find_channel(True).play(self.sound1,-1)

    def amarelar(self):
        pending = 6
        vertical = self.vertical
        horizontal = 220
        while pending > 0:
            screen.blit(yellow_img_squad,(horizontal -2,vertical))
            pending = pending - 1
            horizontal = horizontal + 45
     
    def desenha_resposta(self):
        line = 6
        horizontal = 220
        vertical = 70

        while line > 0:
            pending = 6
            while pending > 0:
                screen.blit(img_squad,(horizontal -2,vertical))
                pending = pending - 1
                horizontal = horizontal + 45
            
            horizontal = 220
            line = line - 1
            vertical = vertical + 70

    def proxima_letra(self, letra):
        text = font.render(letra, True, BLACK)
        screen.blit(text, (self.horizontal - 1, self.vertical - 12))
        self.horizontal = self.horizontal + 45
        self.texto = self.texto + letra

    def apague(self):
        if self.texto != '':
            self.horizontal = self.horizontal - 45
            screen.blit(img_squad,(self.horizontal -2,self.vertical))
             
            self.texto = self.texto[:-1]

    def level(self,level):
        
        self.ref_questions = open("questions"+level+".txt","r")
        self.ref_answers = open("answers"+level+".txt","r")
        self.valores_q = self.ref_questions.readlines()
        self.valores_a = self.ref_answers.readlines()
        
        self.desenha_resposta()
        self.desenha_perguntas()
        
    def texts(self,score):
    
        pygame.draw.rect(screen, (0,187,232), [400, 10, 40, 40])

        scoretext = fontscore.render(str(score), 1,(0,0,139))
        screen.blit(scoretext, (400, 10))
        pygame.display.update()
            
        if score == 0:    
            estado.level("1")
        elif score == 60:
            fontfinal = pygame.font.SysFont('comicsansms',50)
                          
            screen.blit(img_fundo,(0,0,500,500))
            scoretext = fontscore.render("Pontuação: "+str(score), 1,(0,0,139))
            screen.blit(scoretext, (300, 10))
            
            self.horizontal = 220
            self.vertical = 70
            self.texto = ''
            self.nanswer = 0
            
            self.sound1.set_volume(0)
            sound5 = pygame.mixer.Sound("sounds/passoufase.wav")
            duration = sound5.get_length()
            pygame.mixer.find_channel(True).play(sound5)
            time.sleep(duration)
            self.sound1.set_volume(1)
            
            self.level("2")
        elif score == 120:
            screen.blit(img_fundo,(0,0,500,500))
            scoretext = fontscore.render("Pontuação: "+str(score), 1,(0,0,139))
            screen.blit(scoretext, (300, 10))
            
            self.horizontal = 220
            self.vertical = 70
            self.texto = ''
            
            self.sound1.set_volume(0)
            sound5 = pygame.mixer.Sound("sounds/passoufase.wav")
            duration = sound5.get_length()
            pygame.mixer.find_channel(True).play(sound5)
            time.sleep(duration)
            self.sound1.set_volume(1)
            
            self.level("3")
            
        pygame.display.update()
    
    def gameover(self):
        screen.blit(img_fundo,(0,0,500,500))
        fontfinal = pygame.font.SysFont('comicsansms',50)

        finaltext = fontfinal.render("QUE PENA",1,(0,0,139))
        screen.blit(finaltext,(120,100))
        
        finaltext1 = fontfinal.render("VOCÊ PERDEU",1,(0,0,139))
        screen.blit(finaltext1,(80,160))

        pygame.display.update()
        self.sound1.set_volume(0)
        sound4 = pygame.mixer.Sound("sounds/over.wav")
        duration = sound4.get_length()
        pygame.mixer.find_channel(True).play(sound4)
        time.sleep(duration)
        self.sound1.set_volume(1)
        
    def desenha_perguntas(self):
        n = 0
        positionxdraw = 60
        positionxques = 70
        
        while n < len(estado.valores_q):    
            screen.blit(img_asq,(5,positionxdraw))
            split = estado.valores_q[n]

            word = split.split()
            
            x = 0
            nPosLine = 0

            if (len(word)) > 0:
                wordfinal = ''
                while x < len(word):
                
                    if len(wordfinal + " " + word[x]) < 23:
                        if (x == len(word)-1):
                            screen.blit(font2.render(wordfinal + " " + word[x],True,WHITE), (7,positionxques))
                        else:
                            wordfinal = wordfinal + " " + word[x]
                    else:
                        
                        screen.blit(font2.render(wordfinal.lstrip(),True,WHITE), (7,positionxques))
                        wordfinal = word[x]
                        positionxques = positionxques + 20
                        nPosLine = nPosLine + 20

                    x = x + 1
            
            positionxques = positionxques - nPosLine
            n = n+1
            positionxdraw = positionxdraw + 70
            positionxques = positionxques + 70

    
    def verificar_resposta(self):
        if self.texto == self.valores_a[self.nanswer][:len(self.valores_a[self.nanswer])-1]:
            self.sound1.set_volume(0)
            sound2 = pygame.mixer.Sound("sounds/star.wav")
            duration = sound2.get_length()
            pygame.mixer.find_channel(True).play(sound2)
            time.sleep(duration)
            self.sound1.set_volume(1)

            self.horizontal = 220
            self.vertical = self.vertical + 70
            self.texto = ''
            self.nanswer = self.nanswer + 1
         
            self.nscore = self.nscore + 10
            self.texts(self.nscore)
        else:
         
            self.sound1.set_volume(0)
            sound3 = pygame.mixer.Sound("sounds/lostlife.wav")
            duration = sound3.get_length()
            pygame.mixer.find_channel(True).play(sound3)
            time.sleep(duration)
            self.sound1.set_volume(1)
            
            if self.ntry == 1:
                pygame.draw.rect(screen, (0,187,232), [170, 10, 40, 40])
            elif self.ntry == 2:
                pygame.draw.rect(screen, (0,187,232), [130, 10, 40, 40])
            elif self.ntry == 3:
                pygame.draw.rect(screen, (0,187,232), [90, 10, 40, 40])
            elif self.ntry == 4:
                pygame.draw.rect(screen, (0,187,232), [50, 10, 40, 40])
            elif self.ntry == 5:
                pygame.draw.rect(screen, (0,187,232), [10, 10, 40, 40])
                self.gameover()
            
            self.ntry = self.ntry + 1
            
            for _ in self.texto:
                self.apague()

estado = Estado()

estado.texts(0)

laco = True
# Loop do jogo até o usuário clicar em sair

while laco:
    for evt in pygame.event.get():
        # Se for pra sair (X no canto ou ESC)
        if evt.type == pygame.QUIT:    
            estado.ref_answers.close()
            estado.ref_questions.close()
            laco = False
            
        if evt.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
  
            # ENTER
            if pos_x > 380 and pos_x < 495 and pos_y > 775 and pos_y < 825:
                estado.verificar_resposta()      
            elif pos_x > 440 and pos_x < 495 and pos_y > 685 and pos_y < 745:
                estado.apague()
            else:
                for (x1, x2, y1, y2, letra) in coordinates:
                    if pos_x > x1 and pos_x < x2 and pos_y > y1 and pos_y < y2:
                        if len(estado.texto) < 6:
                            estado.proxima_letra(letra)
                            
                        break  
    
    pygame.display.update()
    pygame.display.flip()
    
pygame.quit()