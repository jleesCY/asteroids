from vector import Vector
import math
import pygame

class Ship:

    pg = None
    texture = None
    rect = None

    x_pos = 0
    y_pos = 0

    rect_w = 50
    rect_h = 50

    # movement
    rotation_dir = -1   # -1 is left, 1, is right
    is_rotating = False
    control_vector = None
    movement_vector = None
    curr_rotation_speed = 0
    is_accelerating = False

    # fine-tune ----------
    max_speed = 10
    control_max_speed = 2
    rotation_speed = 6
    deceleration = 2
    vector_change_padding = 5
    mass = 9
    # --------------------

    vector_len = 7


    def __init__(self, pg: pygame):
        self.pg = pg
        self.control_vector = Vector(0,0)
        self.movement_vector = Vector(0,0)
        self.control_vector.rotate(270)
        self.texture = self.pg.transform.scale(pg.image.load("assets/ship.png"), (self.rect_w, self.rect_h)) 
        self.x_pos = pg.display.get_surface().get_width() / 2
        self.y_pos = pg.display.get_surface().get_height() / 2
        self.rect = pygame.Rect(self.x_pos - 25, self.y_pos - 25, self.rect_w, self.rect_h)

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
            width=5
        )
    
    def draw_rect(self):
        self.pg.draw.rect(self.pg.display.get_surface(), (255,0,0), self.rect, 3)

    def draw(self):
        rotated_image = self.pg.transform.rotate(self.texture, -self.control_vector.rotation - 90)
        new_rect = rotated_image.get_rect(center = self.texture.get_rect(center=(self.x_pos, self.y_pos)).center)

        self.pg.display.get_surface().blit(rotated_image, new_rect)

    def update_movement(self, dt, tps):
        if self.is_accelerating:
            self.control_vector.set_magnitude(self.control_max_speed * dt * tps)
            self.movement_vector = self.movement_vector.displacement(self.control_vector, self.mass)
            if self.movement_vector.magnitude >= self.max_speed:
                self.movement_vector.set_magnitude(self.max_speed)

        else:
            self.control_vector.set_magnitude(0)
            self.movement_vector = self.movement_vector.displacement(Vector((self.movement_vector.magnitude / self.deceleration) * dt * tps, self.movement_vector.rotation + 180), self.mass)
            if self.movement_vector.magnitude <= 0.1:
                self.movement_vector.set_magnitude(0)

    def print_diagnostics(self):
        print(f'{self.control_vector.rotation} {self.control_vector.magnitude}')

    def update_rotation(self, dt, tps):
        if self.is_rotating == True:
            self.control_vector.rotate(self.rotation_speed * self.rotation_dir * dt * tps)

    def update_rect(self):
        self.rect.center = (self.x_pos, self.y_pos)

    def fix_out_of_bounds(self):
        screen = self.pg.display.get_surface()

        arr = [
            (self.rect.x + self.rect_w),        # left
            screen.get_width() - self.rect.x,   # right
            (self.rect.y + self.rect_h),        # top
            screen.get_height() - self.rect.y]  # bottom
        idx = next((i for i, x in enumerate(arr) if x == min(arr)), None) if any(x < 0 for x in arr) else -1

        print(arr)

        match idx:
            case -1:
                return (self.x_pos, self.y_pos)
            case 0:
                return (screen.get_width() + (self.rect_w / 2), screen.get_height() - arr[3] + (self.rect_w / 2))
            case 1:
                return (-(self.rect_w / 2), screen.get_height() - arr[3] + (self.rect_w / 2))
            case 2:
                return (screen.get_width() - arr[1] + (self.rect_w / 2), screen.get_height() + (self.rect_h / 2))
            case 3:
                return (screen.get_width() - arr[1] + (self.rect_w / 2), -(self.rect_h / 2))

    def update(self, dt, tps):
        self.update_movement(dt, tps)
        self.update_rotation(dt, tps)

        self.x_pos += self.movement_vector.x() * dt * tps
        self.y_pos += self.movement_vector.y() * dt * tps

        self.update_rect()
        self.x_pos, self.y_pos = self.fix_out_of_bounds()

        #self.print_diagnostics()
        #self.draw_vects()
        #self.draw_rect()
        self.draw()