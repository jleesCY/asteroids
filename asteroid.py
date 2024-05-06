from vector import Vector
import random

class Asteroid:
    pg = None
    vector = None
    texture = None
    rect = None
    mask = None

    x_pos = 100
    y_pos = 100

    # ------- fine-tune
    large_rect_wh = 100
    medium_rect_wh = 50
    small_rect_wh = 25

    small_speed = (0.5, 3)
    medium_speed = (0.3, 2.5)
    large_speed = (0.1, 2)

    rand_angle_width = 60
    # ----------------

    rect_w = 0
    rect_h = 0

    size = 0

    def __init__(self, x, y, size, angle, pg):
        self.pg = pg
        self.x_pos = x
        self.y_pos = y
        self.size = size
        match size:
            case 1:
                self.vector = Vector(random.uniform(self.small_speed[0], self.small_speed[1]), angle)
                self.texture = self.pg.transform.smoothscale(pg.image.load("assets/small_asteroid_1.svg"), (self.small_rect_wh, self.small_rect_wh))
                self.rect = pg.Rect(self.x_pos - (self.small_rect_wh / 2), self.y_pos - (self.small_rect_wh / 2), self.small_rect_wh, self.small_rect_wh)
                self.rect_w = self.small_rect_wh
                self.rect_h = self.small_rect_wh
            case 2:
                self.vector = Vector(random.uniform(self.medium_speed[0], self.medium_speed[1]), angle)
                self.texture = self.pg.transform.smoothscale(pg.image.load("assets/medium_asteroid_1.svg"), (self.medium_rect_wh, self.medium_rect_wh))
                self.rect = pg.Rect(self.x_pos - (self.medium_rect_wh / 2), self.y_pos - (self.medium_rect_wh / 2), self.medium_rect_wh, self.medium_rect_wh)
                self.rect_w = self.medium_rect_wh
                self.rect_h = self.medium_rect_wh
            case 3:
                self.vector = Vector(random.uniform(self.large_speed[0], self.large_speed[1]), angle)
                self.texture = self.pg.transform.smoothscale(pg.image.load("assets/large_asteroid_1.svg"), (self.large_rect_wh, self.large_rect_wh))
                self.rect = pg.Rect(self.x_pos - (self.large_rect_wh / 2), self.y_pos - (self.large_rect_wh / 2), self.large_rect_wh, self.large_rect_wh)
                self.rect_w = self.large_rect_wh
                self.rect_h = self.large_rect_wh
        self.mask = pg.mask.from_surface(self.texture)
    
    def update_rect(self):
        self.rect.center = (self.x_pos, self.y_pos)

    def draw(self):
        new_rect = self.texture.get_rect(center = self.texture.get_rect(center=(self.x_pos, self.y_pos)).center)
        self.pg.display.get_surface().blit(self.texture, new_rect)

    def fix_out_of_bounds(self):
        screen = self.pg.display.get_surface()

        arr = [
            (self.rect.x + self.rect_w),        # left
            screen.get_width() - self.rect.x,   # right
            (self.rect.y + self.rect_h),        # top
            screen.get_height() - self.rect.y]  # bottom
        idx = next((i for i, x in enumerate(arr) if x == min(arr)), None) if any(x < 0 for x in arr) else -1

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
            
    def explode(self):
        if self.size == 3:
            return [
                Asteroid(self.x_pos, self.y_pos, 2, self.rand_angle(), self.pg),
                Asteroid(self.x_pos, self.y_pos, 2, self.rand_angle(), self.pg),
            ]
        elif self.size == 2:
            return [
                Asteroid(self.x_pos, self.y_pos, 1, self.rand_angle(), self.pg),
                Asteroid(self.x_pos, self.y_pos, 1, self.rand_angle(), self.pg),
            ]
        else:
            return []
    
    def rand_angle(self):
        return random.randint(self.vector.rotation - self.rand_angle_width, self.vector.rotation + self.rand_angle_width)
            

    def update(self, dt, tps):

        self.x_pos += self.vector.x() * dt * tps
        self.y_pos += self.vector.y() * dt * tps

        self.update_rect()

        self.x_pos, self.y_pos = self.fix_out_of_bounds()
        
        self.draw()