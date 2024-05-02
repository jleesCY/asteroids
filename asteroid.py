from vector import Vector
class Asteroid:
    pg = None
    vector = None
    texture = None
    rect = None
    mask = None

    small_speed = 2
    medium_speed = 1.7
    large_speed = 1.2

    x_pos = 100
    y_pos = 100

    large_rect_wh = 100
    medium_rect_wh = 50
    small_rect_wh = 25

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
                self.vector = Vector(self.small_speed, angle)
                self.texture = self.pg.transform.smoothscale(pg.image.load("assets/small_asteroid_1.svg"), (self.small_rect_wh, self.small_rect_wh))
                self.rect = pg.Rect(self.x_pos - (self.small_rect_wh / 2), self.y_pos - (self.small_rect_wh / 2), self.small_rect_wh, self.small_rect_wh)
                self.rect_w = self.small_rect_wh
                self.rect_h = self.small_rect_wh
            case 2:
                self.vector = Vector(self.medium_speed, angle)
                self.texture = self.pg.transform.smoothscale(pg.image.load("assets/medium_asteroid_1.svg"), (self.medium_rect_wh, self.medium_rect_wh))
                self.rect = pg.Rect(self.x_pos - (self.medium_rect_wh / 2), self.y_pos - (self.medium_rect_wh / 2), self.medium_rect_wh, self.medium_rect_wh)
                self.rect_w = self.medium_rect_wh
                self.rect_h = self.medium_rect_wh
            case 3:
                self.vector = Vector(self.large_speed, angle)
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
                Asteroid(self.x_pos, self.y_pos, 2, 45, self.pg),
                Asteroid(self.x_pos, self.y_pos, 2, 135, self.pg),
                Asteroid(self.x_pos, self.y_pos, 2, 225, self.pg),
                Asteroid(self.x_pos, self.y_pos, 2, 315, self.pg)
            ]
        elif self.size == 2:
            return [
                Asteroid(self.x_pos, self.y_pos, 1, 45, self.pg),
                Asteroid(self.x_pos, self.y_pos, 1, 135, self.pg),
                Asteroid(self.x_pos, self.y_pos, 1, 225, self.pg),
                Asteroid(self.x_pos, self.y_pos, 1, 315, self.pg)
            ]
        else:
            return []
            

    def update(self, dt, tps):

        self.x_pos += self.vector.x() * dt * tps
        self.y_pos += self.vector.y() * dt * tps

        self.update_rect()

        self.x_pos, self.y_pos = self.fix_out_of_bounds()
        
        self.draw()