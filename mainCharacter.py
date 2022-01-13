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

        self.move_y = 0
        self.move_x = 0

        self.current_eat = 100
        self.target_eat = 150
        self.max_eat = 200
        self.eat_bar_length = 200
        self.eat_ratio = self.max_eat / self.eat_bar_length
        self.eat_change_speed = 2.5

        self.current_sleep = 10
        self.target_sleep = 500
        self.max_sleep = 500
        self.sleep_bar_length = 200
        self.sleep_ratio = self.max_sleep / self.sleep_bar_length
        self.sleep_change_speed = 1

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

    def start_moving(self, *args):
        EVENT = args[0]
        # tick = args[1]  # Program's time for smoother moving

        if EVENT.key == self.move_buttons[0][0]:
            self.move_y = self.v
        elif EVENT.key == self.move_buttons[0][1]:
            self.move_x = self.v
        elif EVENT.key == self.move_buttons[0][2]:
            self.move_y = - self.v
        elif EVENT.key == self.move_buttons[0][3]:
            self.move_x = - self.v

    def stop_moving(self, *args):
        EVENT = args[0]

        if EVENT.key == self.move_buttons[0][0] or EVENT.key == self.move_buttons[0][2]:
            self.move_y = 0
        elif EVENT.key == self.move_buttons[0][1] or EVENT.key == self.move_buttons[0][3]:
            self.move_x = 0

    def change_buttons(self):
        self.move_buttons = self.move_buttons[::-1]

    # Bogachev's method
    def get_fatigue(self, amount):
        if self.current_sleep > 0:
            self.current_sleep -= amount
        if self.current_sleep <= 0:
            self.current_sleep = 0

    # Bogachev's method
    def get_rest(self, amount):
        if self.current_sleep < self.max_sleep:
            self.current_sleep += amount
        if self.current_sleep >= self.max_sleep:
            self.current_sleep = self.max_sleep

    # Bogachev's method
    def basic_sleep(self, scale_screen):
        transition_width = 0
        transition_color = (0, 0, 255)

        if self.current_sleep < self.target_sleep:
            self.current_sleep += self.sleep_change_speed
            transition_width = int((self.target_sleep - self.current_sleep) / self.sleep_ratio)
            transition_color = (0, 255, 0)

        if self.current_sleep > self.target_sleep:
            self.current_sleep -= self.sleep_change_speed
            transition_width = int((self.target_sleep - self.current_sleep) / self.sleep_ratio)
            transition_color = (255, 255, 0)

        sleep_bar_rect = pygame.Rect(10, 10, self.current_sleep / self.sleep_ratio, 25)
        transition_bar_rect = pygame.Rect(sleep_bar_rect.right, 10, transition_width, 25)

        pygame.draw.rect(screen, (0, 0, 255), sleep_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.sleep_bar_length, 25), 4)

    # Bogachev's method
    def pro_eat(self, curr_scrn):
        transition_width = 0
        transition_color = (150, 75, 0)

        if self.current_eat < self.target_eat:
            self.current_eat += self.eat_change_speed
            transition_width = int((self.target_eat - self.current_eat) / self.eat_ratio)
            transition_color = (173, 135, 98)

        if self.current_eat > self.target_eat:
            self.current_eat -= self.eat_change_speed
            transition_width = int((self.target_eat - self.current_eat) / self.eat_ratio)
            transition_color = (101, 67, 33)

        eat_bar_rect = pygame.Rect(10, 45, self.current_eat / self.eat_ratio, 25)
        transition_bar_rect = pygame.Rect(eat_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(curr_scrn, (150, 75, 0), eat_bar_rect)
        pygame.draw.rect(curr_scrn, transition_color, transition_bar_rect)
        pygame.draw.rect(curr_scrn, (255, 255, 255), (10, 45, self.eat_bar_length, 25), 4)

    def get_starve(self, amount):
        if self.target_eat > 0:
            self.self.target_eat -= amount

        if self.target_eat <= 0:
            self.self.target_eat = 0

    def get_food(self, amount):
        if self.target_eat < self.max_eat:
            self.self.target_eat += amount

        if self.target_eat >= self.max_eat:
            self.self.target_eat = self.max_eat

    def update(self, *args):
        tick = args[0]

        current_display_screen = args[1]

        self.rect.y += self.move_y
        self.rect.x += self.move_x

        self.basic_sleep(current_display_screen)
        self.pro_eat(screen)

        self.get_fatigue(1)


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
    hero_character.pro_eat(screen)

    running = True  # Run variable
    move_on = False  # Some vars for the future


    while running:
        screen.fill((0, 0, 0))  # Updating the main screen

        all_sprites.update(clock.tick(), screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    hero_character.get_rest(50)
                else:
                    hero_character.start_moving(event, clock.tick())
            elif event.type == pygame.KEYUP:
                hero_character.stop_moving(event, clock.tick())

        all_sprites.draw(screen)

        clock.tick()
        pygame.display.flip()

    pygame.quit()
