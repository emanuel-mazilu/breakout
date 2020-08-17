import sys
import pygame
from pygame.locals import QUIT

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_SIZE = (640, 1024)
DISPLAY = pygame.display.set_mode(SCREEN_SIZE)
X_RES, Y_RES = SCREEN_SIZE

BRICK_ROWS = 12
BRICK_COLUMNS = 9
PADDING = 3
total_bricks = BRICK_ROWS * BRICK_COLUMNS

VELOCITY = 20
SPEED = 30
bricks = []


class Brick:
    BRICK_WIDTH = 50
    BRICK_HEIGHT = 25

    def __init__(self, pos_x, pos_y, color=BLUE):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.hit_box = pygame.rect.Rect(self.pos_x, self.pos_y, Brick.BRICK_WIDTH, Brick.BRICK_HEIGHT)

    def draw(self, display=DISPLAY):
        self.hit_box = pygame.rect.Rect(self.pos_x, self.pos_y, Brick.BRICK_WIDTH, Brick.BRICK_HEIGHT)
        pygame.draw.rect(display, self.color, self.hit_box)


class Paddle(Brick):
    PADDLE_SIZE = (200, 12)
    BRICK_WIDTH, BRICK_HEIGHT = PADDLE_SIZE

    def __init__(self, **kwarg):
        self.pos_y = Y_RES - 24
        self.pos_x = 300
        super().__init__(self.pos_x, self.pos_y, **kwarg)
        self.hit_box = pygame.rect.Rect(self.pos_x, self.pos_y, Paddle.BRICK_WIDTH, Paddle.BRICK_HEIGHT)

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if self.pos_x > 0:
                self.pos_x -= VELOCITY
        if key[pygame.K_RIGHT]:
            if self.pos_x < X_RES - Paddle.BRICK_WIDTH:
                self.pos_x += VELOCITY

    def draw(self, display=DISPLAY):
        self.movement()
        self.hit_box = pygame.rect.Rect(self.pos_x, self.pos_y, Paddle.BRICK_WIDTH, Paddle.BRICK_HEIGHT)
        pygame.draw.rect(display, self.color, self.hit_box)


class Ball:
    def __init__(self, display=DISPLAY, color=BLACK):
        self.display = display
        self.color = color
        self.pos_x, self.pos_y = DISPLAY.get_rect().center
        self.direction_x = 1
        self.direction_y = 1
        self.radius = 10
        self.hit_box = pygame.Rect(self.pos_x-10, self.pos_y - 10, 20, 20)

    def movement(self):
        if self.pos_x < 0 + self.radius or self.pos_x > X_RES - self.radius:
            self.direction_x = -self.direction_x
        if self.pos_y < 0 + self.radius or self.pos_y > Y_RES - self.radius:
            self.direction_y = -self.direction_y
        self.pos_y += SPEED * self.direction_y
        self.pos_x += SPEED * self.direction_x

    def collision(self):
        if self.hit_box.colliderect(paddle.hit_box):
            self.direction_y = -ball.direction_y
        if 300 > self.hit_box.top:
            for brick in bricks:
                if self.hit_box.colliderect(brick.hit_box) and brick.color != WHITE:
                    brick.color = WHITE
                    self.direction_y = -self.direction_y

    def draw(self):
        self.movement()
        self.hit_box = pygame.Rect(self.pos_x-10, self.pos_y - 10, 20, 20)
        pygame.draw.rect(self.display, RED, self.hit_box, 2)
        pygame.draw.circle(self.display, self.color, [self.pos_x, self.pos_y], self.radius)
        self.collision()


def make_bricks():
    for i in range(0, BRICK_ROWS):
        for j in range(0, BRICK_COLUMNS):
            if j < 3:
                color = RED
            elif 3 <= j < 6:
                color = GREEN
            else:
                color = BLUE
            bricks.append(
                Brick(i * Brick.BRICK_WIDTH + i * PADDING + PADDING, j * Brick.BRICK_HEIGHT + j * PADDING + PADDING,
                      color=color))


def draw_bricks():
    for brick in bricks:
        brick.draw()


def win_check():
    test = 0
    for brick in bricks:
        if brick.color == WHITE:
            test += 1
    if test == total_bricks:
        pygame.quit()
        sys.exit()


pygame.init()
make_bricks()
paddle = Paddle(color=BLACK)
ball = Ball()
while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(WHITE)
    draw_bricks()
    ball.draw()
    paddle.draw()
    pygame.display.update()
    win_check()
