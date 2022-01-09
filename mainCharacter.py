import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Image '{fullname}' not found")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


class MovingHero(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)

        self.image = load_image('obama.jpeg')  # Uploading image for our sprite (Don't pay attention for the name)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.current_sleep = 100
        self.max_sleep = 500
        self.sleep_bar_length = 200
        self.sleep_ratio = self.max_sleep / self.sleep_bar_length

        self.door_key = False

        self.v = 10  # hero's speed

        self.move_buttons = [
            [
                pygame.K_s,
                pygame.K_d,
                pygame.K_w,
                pygame.K_a
            ],
            [
                pygame.K_DOWN,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_LEFT
            ]
        ]

    def move(self, *args):
        EVENT = args[0]
        # tick = args[1]  # Program's time for smoother moving

        if EVENT.key == self.move_buttons[0][0]:
            self.rect.y += self.v
        elif EVENT.key == self.move_buttons[0][1]:
            self.rect.x += self.v
        elif EVENT.key == self.move_buttons[0][2]:
            self.rect.y -= self.v
        elif EVENT.key == self.move_buttons[0][3]:
            self.rect.x -= self.v

    def change_buttons(self):
        self.move_buttons = self.move_buttons[::-1]

    def get_fatigue(self, amount):
        if self.current_sleep > 0:
            self.current_sleep -= amount
        if self.current_sleep <= 0:
            self.current_sleep = 0

    def get_rest(self, amount):
        if self.current_sleep < self.max_sleep:
            self.current_sleep += amount
        if self.current_sleep >= self.max_sleep:
            self.current_sleep = self.max_sleep

    def basic_sleep(self, scale_screen):
        pygame.draw.rect(scale_screen, (0, 0, 255), (10, 10, self.current_sleep / self.sleep_ratio, 25))
        pygame.draw.rect(scale_screen, (255, 255, 255), (10, 10, self.sleep_bar_length, 25), 4)


if __name__ == '__main__':
    # Initialize garbage:
    pygame.init()

    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    screen.fill((255, 255, 255))

    hero_character = MovingHero(all_sprites)
    clock = pygame.time.Clock()

    # All groups appearance
    all_sprites.draw(screen)

    hero_character.basic_sleep(screen)

    running = True  # Run variable
    move_on = False  # Some vars for the future

    while running:
        all_sprites.update()

        all_sprites.draw(screen)

        hero_character.basic_sleep(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                hero_character.move(event, clock.tick())

        screen.fill((255, 255, 255))  # Updating the main screen

        pygame.display.flip()

    pygame.quit()
