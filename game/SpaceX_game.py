import pygame
import time
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 680, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceX Game")

# Load images
# Player
rocket01_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "SpaceShip.png")), (24, 111))
laser_img = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
# Obstacles
asteroid01_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Asteroid01.png")),
                                        (random.randrange(10, 120), random.randrange(60, 140)))
asteroid02_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Asteroid02.png")),
                                        (random.randrange(10, 120), random.randrange(60, 140)))
asteroid03_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Asteroid03.png")),
                                        (random.randrange(10, 120), random.randrange(60, 140)))
asteroid04_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Asteroid04.png")),
                                        (random.randrange(10, 120), random.randrange(60, 140)))
# Background
background_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Background.png")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y <= height and self.y >= 0

    def collision(self, obj):
        return collide(self, obj)


class Objects:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.falcon_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.falcon_img, (self.x, self.y))

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.falcon_img.get_width()

    def get_height(self):
        return self.falcon_img.get_height()


class Player(Objects):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.falcon_img = rocket01_img
        self.mask = pygame.mask.from_surface(self.falcon_img)
        self.max_health = health


class Asteroid(Objects):
    asteroid_types = {
                        "asteroid01": asteroid01_img,
                        "asteroid02": asteroid02_img,
                        "asteroid03": asteroid03_img,
                        "asteroid04": asteroid04_img

                     }

    def __init__(self, x, y, types, health=100):
        super().__init__(x, y, health)
        self.falcon_img = pygame.transform.rotate(self.asteroid_types[types], random.randrange(0, 360))
        self.mask = pygame.mask.from_surface(self.falcon_img)

    def move(self, vel):
        self.y += vel


def collide(object1, object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 1
    lives = 6
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    asteroids = []
    wave_length = 6
    asteroid_vel = 1

    player_vel = 3

    player = Player(300, 650)
    
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(background_img, (0, 0))
        # Draw text
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for asteroid in asteroids:
            asteroid.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("YOU LOST !!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(asteroids) == 0:
            level += 1
            wave_length += 3
            for i in range(wave_length):
                asteroid = Asteroid(random.randrange(50, WIDTH-100), random.randrange(-1500, -100),
                                     random.choice(["asteroid01", "asteroid02", "asteroid03", "asteroid04"]))
                asteroids.append(asteroid)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for asteroid in asteroids[:]:
            asteroid.move(asteroid_vel)
            if asteroid.y + asteroid.get_height() > HEIGHT:
                lives -= 1
                asteroids.remove(asteroid)


main()








