from vector import Vector
import math
import pygame

class Ship:

    pg = None
    texture = None
    rect = None

    x_pos = 0
    y_pos = 0

    # movement
    rotation_dir = -1   # -1 is left, 1, is right
    is_rotating = False
    control_vector = None
    movement_vector = None
    curr_rotation_speed = 0
    is_accelerating = False

    # fine-tune ----------
    max_speed = 8
    control_max_speed = 2
    rotation_speed = 300
    deceleration = 3
    vector_change_padding = 5
    mass = 10
    # --------------------

    vector_len = 7


    def __init__(self, pg: pygame):
        self.pg = pg
        self.control_vector = Vector(0,0)
        self.movement_vector = Vector(0,0)
        self.control_vector.rotate(270)
        self.texture = pg.image.load("assets/ship.png")
        self.rect = None # pg rect
        self.x_pos = 500
        self.y_pos = 500

    def draw_vects(self):
        self.pg.draw.line(
            self.pg.display.get_surface(),
            (0,255,0),
            (self.x_pos, self.y_pos),
            (self.x_pos + self.movement_vector.x() * self.vector_len, self.y_pos + self.movement_vector.y() * self.vector_len),
            width=5
        )
        self.pg.draw.line(
            self.pg.display.get_surface(),
            (0,0,255),
            (self.x_pos, self.y_pos),
            (self.x_pos + self.control_vector.x() * self.vector_len, self.y_pos + self.control_vector.y() * self.vector_len),
            width=3
        )
    
    def draw_rect(self):
        self.pg.draw.rect(self.pg.display.get_surface(), (255,0,0), pygame.Rect(self.x_pos - 10, self.y_pos - 10, 20,20), 5)

    def draw(self):
        scaled_image = self.pg.transform.scale(self.texture, (50,50))
        rotated_image = self.pg.transform.rotate(scaled_image, -self.control_vector.rotation - 90)
        new_rect = rotated_image.get_rect(center = self.texture.get_rect(center=(self.x_pos, self.y_pos)).center)

        self.pg.display.get_surface().blit(rotated_image, new_rect)

    def update_movement(self, dt):
        if self.is_accelerating:
            self.control_vector.set_magnitude(self.control_max_speed)
            self.movement_vector = self.movement_vector.displacement(self.control_vector, dt, self.mass)
            if self.movement_vector.magnitude >= self.max_speed:
                self.movement_vector.set_magnitude(self.max_speed)

        else:
            self.control_vector.set_magnitude(0)
            self.movement_vector = self.movement_vector.displacement(Vector(self.movement_vector.magnitude / self.deceleration, self.movement_vector.rotation + 180), dt, self.mass)
            if self.movement_vector.magnitude <= 0.1:
                self.movement_vector.set_magnitude(0)

        
        print(self.movement_vector.magnitude)

    def print_diagnostics(self):
        print(f'{self.control_vector.rotation} {self.control_vector.magnitude}')

    def update_rotation(self, dt):
        if self.is_rotating == True:
            self.control_vector.rotate(self.rotation_speed * self.rotation_dir * dt)

    def update(self, dt):
        self.update_movement(dt)
        self.update_rotation(dt)

        self.x_pos += self.movement_vector.x()
        self.y_pos += self.movement_vector.y()

        #self.print_diagnostics()
        self.draw_vects()
        #self.draw_rect()
        self.draw()