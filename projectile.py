from vector import Vector
import math
class Projectile:

    pg = None
    vector = None
    texture = None
    rect = None
    mask = None

    x_pos = 0
    y_pos = 0

    rotation = 0
    distance = 0

    rect_w = 5
    rect_h = 5

    # fine-tune ----------
    speed = 13
    # --------------------

    vector_len = 10

    def __init__(self, x, y, angle, pg):
        self.x_pos = x
        self.y_pos = y
        self.rotation = angle
        self.pg = pg
        self.texture = self.pg.transform.smoothscale(pg.image.load("assets/projectile.svg"), (self.rect_w, self.rect_h))
        self.vector = Vector(self.speed, angle)
        self.rect = pg.Rect(self.x_pos - (self.rect_w / 2), self.y_pos - (self.rect_h / 2), self.rect_w, self.rect_h)
        self.mask = pg.mask.from_surface(self.texture)

    def draw(self):
        new_rect = self.texture.get_rect(center = self.texture.get_rect(center=(self.x_pos, self.y_pos)).center)
        self.pg.display.get_surface().blit(self.texture, new_rect)

    def draw_vects(self):
        self.pg.draw.line(
            self.pg.display.get_surface(),
            (0,255,0),
            (self.x_pos, self.y_pos),
            (self.x_pos + self.vector.x() * self.vector_len, self.y_pos + self.vector.y() * self.vector_len),
            width=3
        )

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

        old_x = self.x_pos
        old_y = self.y_pos

        self.x_pos += self.vector.x() * dt * tps
        self.y_pos += self.vector.y() * dt * tps

        self.distance += math.sqrt((self.x_pos - old_x)**2 + (self.y_pos - old_y)**2)

        self.update_rect()
        self.x_pos, self.y_pos = self.fix_out_of_bounds()

        self.draw()