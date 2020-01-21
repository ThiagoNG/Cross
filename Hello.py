import sys
import pygame

# Verificando erros de inicializacao
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Ops, {0} o Pygame iniciou com algum problema..." . format(check_errors[1]))
    sys.exit(-1)
    
size = width, height = 1100, 880
speed = [5, 5]
black = 100, 100, 255
gray = 100, 100, 100

screen = pygame.display.set_mode(size)
 
ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()
  
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
  
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
  
        screen.fill(gray)
        screen.blit(ball, ballrect)
        pygame.display.flip()