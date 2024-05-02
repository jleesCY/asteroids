from ship import Ship
import pygame as pg
from pygame.locals import *
import time
from asteroid import Asteroid

TICKS_PER_SECOND = 60
FPS = 60
RUNNING = True
CLOCK = pg.time.Clock()

RATIO = 0.75
WIDTH = 1000
HEIGHT = WIDTH * RATIO
RES = (WIDTH,HEIGHT)
SCREEN = pg.display.set_mode(RES)

ASTEROIDS = []

def main():
    global RUNNING

    player = Ship(pg=pg)

    pg.init()

    prev_time = time.time()
    dt = 0

    ASTEROIDS.append(Asteroid(100, 100, 3, 45, pg))

    # game loop
    while RUNNING:
        CLOCK.tick(FPS)
        SCREEN.fill((0,0,0))

        # compute delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        player.update(dt, TICKS_PER_SECOND)

        for asteroid in ASTEROIDS:
            asteroid.update(dt, TICKS_PER_SECOND)
            for bullet in player.bullets:
                if bullet.rect.colliderect(asteroid.rect):
                    ASTEROIDS.remove(asteroid)
                    player.bullets.remove(bullet)

                    for new in asteroid.explode():
                        ASTEROIDS.append(new)
        
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
                    
# Call Main
if __name__ == '__main__':
    main()