import pygame
from random import randint

pygame.init()


# Eixos
x = 1280
y = 720
speed = 10
pontos = 3

# Nave
nave_x = 200
nave_y = 300
speed_nave = 5


# Alien
alien_x = 1350
alien_y = 360
speed_alien = 7

# Bala
bala_x = 210
bala_y = 315
speed_bala = 0
tiro = False

# Definições
tela = pygame.display.set_mode((x, y))
pygame.display.set_caption("Game")

# Funções
def respawn():
    x= 1350
    y = randint(1, 640)
    return [x, y]

def respawn_bala():
    tiro = False
    bala_resp_x = nave_x + 10
    bala_resp_y = nave_y + 15
    speed_bala = 0
    return [tiro, bala_resp_x, bala_resp_y, speed_bala]

def colisoes():
    global pontos, speed, speed_alien, speed_bala, speed_nave
    if nave_rect.colliderect(alien_rect):
        pontos -= int(randint(1, 3) / 2)
        speed += 0.3
        speed_alien += 0.3
        speed_bala += 0.3
        speed_nave += 0.3
        return True
    elif alien_rect.x <= 60:
        pontos -= int(randint(1, 3) / 2)
        speed -= 0.2
        speed_alien -= 0.2
        speed_bala -= 0.2
        speed_nave -= 0.2
        return True
    elif bala_rect.colliderect(alien_rect):
        pontos += int(randint(1, 3) / 2)
        speed += 0.3
        speed_alien += 0.3
        speed_bala += 0.3
        speed_nave += 0.3
        return True
    else:
        return False

# Imagens
bg = pygame.image.load("images/Fundo.jpg").convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

alien = pygame.image.load("images/alien.png").convert_alpha()
alien = pygame.transform.scale(alien, (50, 50))

nave = pygame.image.load("images/nave.png").convert_alpha()
nave = pygame.transform.scale(nave, (50, 50))

bala = pygame.image.load("images/bala.png").convert_alpha()
bala = pygame.transform.scale(bala, (25, 25))
bala = pygame.transform.rotate(bala, -90)


# Player Rects

nave_rect = nave.get_rect()
alien_rect = alien.get_rect()
bala_rect = bala.get_rect()

# Sistema
fonte = pygame.font.SysFont("fonts/PixelGameFont.ttf", 50)
fonte2 = pygame.font.SysFont("fonts/PixelGameFont.ttf", 20)
const = 1280
run = True
relogio = pygame.time.Clock()

while run:

    relogio.tick(60)

    fps = relogio.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            tiro = True
            speed_bala = speed

    tecla = pygame.key.get_pressed()

    if tecla[pygame.K_w] and nave_y > 1:
        nave_y -= speed_nave
        if not tiro:
            bala_y -= speed_nave
    
    if tecla[pygame.K_s] and nave_y < 665:
        nave_y += speed_nave
        if not tiro:
            bala_y += speed_nave

    if tecla[pygame.K_q]:
        tiro = True
        speed_bala = speed

    # Respawn  alien
    if alien_x <= 50 or colisoes():
        alien_x = respawn()[0]
        alien_y = respawn()[1]
    if bala_x >= 1300 or colisoes():
        tiro, bala_x, bala_y, speed_bala = respawn_bala()
    
    if pontos <= 0:
        run = False

    # Rects Posições
    nave_rect.x = nave_x
    nave_rect.y = nave_y

    alien_rect.x = alien_x
    alien_rect.y = alien_y

    bala_rect.x = bala_x
    bala_rect.y = bala_y

    

    
    rel_x = x % bg.get_rect().width
    tela.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < const:
        tela.blit(bg, (rel_x, 0))
    
    tela.blit(alien, (alien_x, alien_y))
    tela.blit(bala, (bala_x, bala_y))
    tela.blit(nave, (nave_x, nave_y))
    
    # movimento da tela
    x -= speed
    alien_x -= speed_alien
    bala_x += speed_bala

    score = fonte.render(f"Pontos: {int(pontos)}", True, (0, 0, 0))
    fps_t = fonte2.render(f"FPS - {int(fps)}", True, (0, 0, 0))
    tela.blit(score, (50, 50))
    tela.blit(fps_t, (10, 10))

    pygame.display.update()
