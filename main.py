from ship import Ship
from asteroid import Asteroid
from projectile import Projectile
from ufo import UFO
from vector import Vector
import pygame as pg
from pygame.locals import *
import time

TICKS_PER_SECOND = 60
FPS = 60
RUNNING = True
CLOCK = pg.time.Clock()

RATIO = 0.75
WIDTH = 1000
HEIGHT = WIDTH * RATIO
RES = (WIDTH,HEIGHT)
SCREEN = pg.display.set_mode(RES)

def main():
    global RUNNING

    player = Ship(pg=pg)

    pg.init()

    prev_time = time.time()
    dt = 0

    # game loop
    while RUNNING:
        CLOCK.tick(FPS)
        SCREEN.fill((0,0,0))

        # compute delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        player.update(dt, TICKS_PER_SECOND)
        pg.display.update()

        for event in pg.event.get():

            keys = pg.key.get_pressed()

            if event.type == pg.QUIT:
                RUNNING = False

            if keys[K_o]:
                player.is_accelerating = True
            else:
                player.is_accelerating = False

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