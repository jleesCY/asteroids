from ship import Ship
import pygame as pg
from pygame.locals import *
import time
from asteroid import Asteroid
import random
import math

TICKS_PER_SECOND = 60
FPS = 60
RUNNING = True
CLOCK = pg.time.Clock()

RATIO = 0.75
WIDTH = 1000
HEIGHT = WIDTH * RATIO
RES = (WIDTH,HEIGHT)
SCREEN = pg.display.set_mode(RES)

LIFE_IMAGE = pg.image.load("assets/ship.svg")
LIFE_IMAGE_HEIGHT = 45
LIFE_IMAGE_WIDTH = LIFE_IMAGE_HEIGHT * 0.6

pg.init()
pg.font.init()

FONT = pg.font.Font("assets/fonts/Hyperspace.ttf", size=50)
SCORE = 0
LIVES = 3

pg.display.set_caption('Asteroids')

ASTEROIDS = []

def main():
    global RUNNING
    global SCORE
    global LIVES

    player = Ship(pg=pg)

    prev_time = time.time()
    dt = 0

    # game loop
    while RUNNING:
        #CLOCK.tick(FPS)
        SCREEN.fill((0,0,0))

        # compute delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        player.update(dt, TICKS_PER_SECOND)

        SCREEN.blit(FONT.render(str(SCORE), False, (255, 255, 255)), (15, 0))

        if len(ASTEROIDS) < 4:
            spawn_asteroid()

        for asteroid in ASTEROIDS:
            asteroid.update(dt, TICKS_PER_SECOND)

            if player.rect.colliderect(asteroid.rect):
                if LIVES == 0:
                    game_over()
                    return
                player.reset()
                LIVES -= 1


            for bullet in player.bullets:
                if bullet.rect.colliderect(asteroid.rect):
                    ASTEROIDS.remove(asteroid)
                    player.bullets.remove(bullet)

                    for new in asteroid.explode():
                        ASTEROIDS.append(new)
                    
                    match asteroid.size:
                        case 1: SCORE += 100
                        case 2: SCORE += 50
                        case 3: SCORE += 20

        for i in range(LIVES):
            texture = pg.transform.smoothscale(LIFE_IMAGE, (LIFE_IMAGE_WIDTH, LIFE_IMAGE_HEIGHT)) 
            SCREEN.blit(texture, (15 + ((LIFE_IMAGE_WIDTH + 4) * i), 60))
        
        pg.display.update()

        p_ready = True
        for event in pg.event.get():

            keys = pg.key.get_pressed()

            if event.type == pg.QUIT:
                RUNNING = False

            if keys[K_o]:
                player.is_accelerating = True
            else:
                player.is_accelerating = False

            if p_ready:
                if keys[K_p]:
                    p_ready = False
                    player.spawn_bullet()
            else:
                if not keys[K_p]:
                    p_ready = True

            if keys[K_q] or keys[K_w]:
                player.is_rotating = True
                if keys[K_w]: 
                    player.rotation_dir = 1
                else: 
                    player.rotation_dir = -1
            else:
                player.is_rotating = False

def game_over():
    global RUNNING
    print("game over")
    RUNNING = False

def spawn_asteroid():
    global ASTEROIDS

    ast = Asteroid(0, 0, 3, 0, pg)
    rand = random.randint(1,4)

    match rand:
        case 1: # left
            ast.x_pos = -ast.large_rect_wh
            ast.y_pos = random.uniform(0, HEIGHT)
        case 2: # right
            ast.x_pos = ast.large_rect_wh + WIDTH
            ast.y_pos = random.uniform(0, HEIGHT)
        case 3: # top
            ast.x_pos = random.uniform(0, WIDTH)
            ast.y_pos = -ast.large_rect_wh
        case 4: # bottom
            ast.x_pos = random.uniform(0, WIDTH)
            ast.y_pos = ast.large_rect_wh + HEIGHT
    
    ast.vector.rotation = random.randint(0,359)
    
    ASTEROIDS.append(ast)

    a = Asteroid(0, 0, 3, 0, pg=pg)
                    
# Call Main
if __name__ == '__main__':
    main()
