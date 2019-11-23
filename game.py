from random import randint
import pygame

pygame.init()

SCREEN_W = 288
SCREEN_H = 512

BIRD_IMAGE = pygame.image.load("assets/bird.png")
BIRD_STARTING_POSITION = (20, 130)
BIRD_THRUST = 3
BIRD_SPEED = 4
GRAVITY = 0.1

BACKGROUND_IMAGE = pygame.image.load("assets/background-day.png")

PIPES = (
    pygame.transform.flip(pygame.image.load("assets/pipe.png"), False, True),
    pygame.image.load("assets/pipe.png")
)

GAME_OVER_IMAGE = pygame.image.load("assets/gameover.png")
GAME_OVER_SIZE = GAME_OVER_IMAGE.get_size()
GAME_OVER_POSITION = (SCREEN_W / 2 - GAME_OVER_SIZE[0] / 2, SCREEN_H / 2 - GAME_OVER_SIZE[1] / 2)

BASE_IMAGE = pygame.image.load("assets/base.png")
BASE_Y = SCREEN_H - BASE_IMAGE.get_size()[1]


DEBUG = False


class Entity:
    def __init__(self, x, y, image, hitbox_relative_size=0):
        self.image = image
        self.size = image.get_size()
        self.hitbox_relative_size = hitbox_relative_size

        self.x = x
        self.y = y
        self.w = self.size[0]
        self.h = self.size[1]

        self.hitbox_x = self.x + hitbox_relative_size
        self.hitbox_y = self.y + hitbox_relative_size
        self.hitbox_w = self.w - hitbox_relative_size * 2
        self.hitbox_h = self.h - hitbox_relative_size * 2

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), (self.hitbox_x, self.hitbox_y, self.hitbox_w, self.hitbox_h))

    def update(self):
        self.hitbox_x = self.x + self.hitbox_relative_size
        self.hitbox_y = self.y + self.hitbox_relative_size

    def is_colliding(self, colliding_entity):
        return self.hitbox_x + self.hitbox_w >= colliding_entity.hitbox_x and \
            self.hitbox_x <= colliding_entity.hitbox_x + colliding_entity.hitbox_w and \
            self.hitbox_y + self.hitbox_h >= colliding_entity.hitbox_y and \
            self.hitbox_y <= colliding_entity.hitbox_y + colliding_entity.hitbox_h


class Bird(Entity):
    def __init__(self):
        super().__init__(BIRD_STARTING_POSITION[0], BIRD_STARTING_POSITION[1], BIRD_IMAGE, +5)
        self.fall_speed = 0
        self.alive = True

    def update(self):
        self.fall_speed += GRAVITY
        self.y += self.fall_speed
        super().update()

    def fly(self):
        self.fall_speed = - BIRD_THRUST

    def reset(self):
        self.alive = True
        self.fall_speed = 0
        self.y = BIRD_STARTING_POSITION[1]


class Pipe(Entity):
    def __init__(self, min_y, max_y, image):
        super().__init__(SCREEN_W, randint(min_y, max_y), image)
        self.min_y = min_y
        self.max_y = max_y
        self.speed = BIRD_SPEED

    def update(self):
        self.x -= self.speed
        if self.x <= -self.w:
            self.reset()

        super().update()

    def reset(self):
        self.x = SCREEN_W
        self.y = randint(self.min_y, self.max_y)


screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Spalla Bird")
clock = pygame.time.Clock()
running = True

bird = Bird()
pipe_top = Pipe(-140, -40, PIPES[0])
pipe_bottom = Pipe(300, 350, PIPES[1])
base = Entity(0, BASE_Y, BASE_IMAGE)

entities = (pipe_bottom, pipe_top, base, bird)

while running:
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    for entity in entities:
        entity.draw(screen)

    if not bird.alive:
        screen.blit(GAME_OVER_IMAGE, GAME_OVER_POSITION)
    else:
        for entity in entities:
            entity.update()

        if bird.is_colliding(pipe_top) or bird.is_colliding(pipe_bottom) or bird.is_colliding(base):
            bird.alive = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bird.alive:
                    bird.fly()
                else:
                    bird.reset()
                    pipe_top.reset()
                    pipe_bottom.reset()

    pygame.display.update()
    clock.tick(60)
