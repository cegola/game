import pygame, sys, random
from pygame.locals import *

# game variables
FPS = 110
ANCHOVENTANA = 700
ALTOVENTANA = 500
COLORTEXTO = (193, 13, 23)
TAMAÑOFUENTE = 12
TASAMOVIMIENTOJUGADOR = 5
TASAENEMIGAS = 100
VELOCIDADMINENEMIGA = 1
VELOCIDADMAXENEMIGA = 3

shelving_y_pos = 0
nombreJuego = 'YAYAS ATACK'
x = 350
y = 350
speed = 5
puntMax = 0
nombreTop = ''


def draw_shelving():
    screen.blit(shelving_surface, (0, shelving_y_pos))
    screen.blit(shelving_surface, (0, shelving_y_pos - 705))
    screen.blit(shelving_surface, (600, shelving_y_pos))
    screen.blit(shelving_surface, (600, shelving_y_pos - 705))


def dibujarTexto(texto, font, superficie, x, y):
    objetotexto = font.render(texto, 1, COLORTEXTO)
    rectangulotexto = objetotexto.get_rect(center=(x, y))
    # rectangulotexto.topleft = (x, y)
    superficie.blit(objetotexto, rectangulotexto)


def esperarTecla():
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                finalizar()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:  # Quita al presionar ESCAPE
                    finalizar()
                return

def colision(rect, enemies):
    for i in enemies:
        if rect.colliderect(i['rect']):
            return True
    return False


def finalizar():
    pygame.quit()
    sys.exit()


# definimos pygame, ventana y reloj
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA))
pygame.display.set_caption(str(nombreJuego))

# ocultamos el ratón
pygame.mouse.set_visible(False)

# establece los fonts
font = pygame.font.Font('resources/04B_30__.TTF', 24)

# establecemos las imagenes
bg_surface = pygame.image.load('img/background1.png').convert()
shelving_surface = pygame.image.load('img/shelving.png').convert()

yaya = pygame.image.load('img/player.png')
rectYaya = yaya.get_rect()

enemies_img = ['img/enemigo1.png', 'img/enemigo2.png','img/enemigo3.png']
maxEnemies = len(enemies_img)-1


# dibujamos el texto inicial
dibujarTexto(str(nombreJuego), font, screen, (ANCHOVENTANA / 2), (ALTOVENTANA / 2) - 50)
dibujarTexto('Presione una tecla', font, screen, (ANCHOVENTANA / 2), (ALTOVENTANA / 2))
dibujarTexto('para iniciar el juego', font, screen, (ANCHOVENTANA / 2), (ALTOVENTANA / 2) + 50)
pygame.display.update()
esperarTecla()

while True:
    # comienzo del juego
    ptos = 0
    screen.blit(bg_surface, (0, 0))
    rectYaya.topleft = (x, y)
    enemies = []
    contEnemy = 0
    moverIzquierda = moverDerecha = False

    while True:
        ptos += 1
        # recoger eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finalizar()
            # sabemos que tecla esta presionada
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moverDerecha = False
                    moverIzquierda = True
                    # x -= speed
                if event.key == K_RIGHT or event.key == ord('z'):
                    moverIzquierda = False
                    moverDerecha = True
                    # x += speed
                if event.key == K_ESCAPE:
                    finalizar()
            # sabemos que la tecla se suelta
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == ord('a'):
                    moverIzquierda = False
                if event.key == K_RIGHT or event.key == ord('z'):
                    moverDerecha = False
                if event.key == K_ESCAPE:
                    finalizar()

        # mover jugador
        if moverIzquierda and rectYaya.left > 90:
            rectYaya.move_ip(-1 * TASAMOVIMIENTOJUGADOR, 0)
        if moverDerecha and rectYaya.right < (ANCHOVENTANA - 90):
            rectYaya.move_ip(TASAMOVIMIENTOJUGADOR, 0)

        contEnemy += 1
        if contEnemy == TASAENEMIGAS:
            contEnemy=0
            pos = random.randint(0, maxEnemies)
            newEnemy = {'rect': pygame.Rect(random.randint(90, ANCHOVENTANA-180) ,-90,90,90), 'speed':random.randint(VELOCIDADMINENEMIGA, VELOCIDADMAXENEMIGA), 'surface': pygame.image.load(enemies_img[pos])}

            enemies.append(newEnemy)


        # mueve los enemigos hacia abajo
        for i in enemies:
            i['rect'].move_ip(0, i['speed'])

        # eliminamos los enemigos por debajo de la pantalla
        for i in enemies:
            if i['rect'].top > ALTOVENTANA:
                enemies.remove(i)


        screen.blit(bg_surface, (0, 0))
        screen.blit(yaya, rectYaya)

        # dibuja las estanterias
        shelving_y_pos += 1
        draw_shelving()
        # si la estanteria acaba (final de la pantalla) la posicion y vuelve a 0
        if shelving_y_pos >= 700:
            shelving_y_pos = 0
        
        #dibujamos los puntos
        dibujarTexto('Puntos: %s' % (ptos), font, screen, 350, 10)
        dibujarTexto('Records: %s' % (puntMax), font, screen, 350, 40)

        #dibuja los enemigos
        for i in enemies:
            screen.blit(i['surface'], i['rect'])

        # vemos si hay choque
        if colision(rectYaya, enemies):
            if ptos > puntMax:
                puntMax=ptos
            break

        pygame.display.update()
        clock.tick(FPS)

    #acabar juego
    dibujarTexto('Maxima puntuacion: '+str(puntMax) , font, screen, (ANCHOVENTANA / 2), (ALTOVENTANA / 2) - 50)
    dibujarTexto('Game over', font, screen, (ANCHOVENTANA / 2), (ALTOVENTANA / 2))
    dibujarTexto('Presione para repetir', font, screen, (ANCHOVENTANA / 2), (ALTOVENTANA / 2) + 50)
    pygame.display.update()
    esperarTecla()
