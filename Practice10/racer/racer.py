import pygame
from pygame.locals import *
import random

pygame.init()

width = 300
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer")

running = True
game_over = False

level = 1
enemy_speed = 10
coin_score = 0


class player_car(pygame.sprite.Sprite):
    def __init__(self, path="mycar.jpg"):
        super().__init__()
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image, (width // 4, height // 4))
        self.rect = self.image.get_rect()
        self.rect.center = (47, 525)

    def move(self):
        button = pygame.key.get_pressed()

        if button[K_a]:
            self.rect.centerx -= 5
        elif button[K_d]:
            self.rect.centerx += 5

        # boundaries
        if self.rect.centerx < 47:
            self.rect.centerx = 47
        if self.rect.centerx > 253:
            self.rect.centerx = 253


class red_car(pygame.sprite.Sprite):
    def __init__(self, path="encar.jpg"):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path), (width // 4, height // 4))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(47, 253)
        self.rect.centery = -75
        self.score = 0

    def move(self, speed=10):
        self.rect.centery += speed

        if self.rect.centery > 675:
            self.rect.centery = -75
            self.rect.centerx = random.randint(47, 253)
            self.score += 10


class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(47, 253)
        self.rect.centery = random.randint(-500, -50)

    def move(self, speed=5):
        self.rect.centery += speed

        if self.rect.centery > height:
            self.rect.centery = random.randint(-500, -50)
            self.rect.centerx = random.randint(47, 253)


class background:
    def __init__(self, path="road.jpg"):
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image, (width, height // 2))

        rect1 = self.image.get_rect()
        rect2 = self.image.get_rect()
        rect3 = self.image.get_rect()

        rect2.centery += height // 2
        rect3.centery += height

        self.rectangles = []
        self.rectangles.append(rect1)
        self.rectangles.append(rect2)
        self.rectangles.append(rect3)

    def draw(self):
        for rectangle in self.rectangles:
            screen.blit(self.image, rectangle)

    def move(self):
        for rectangle in self.rectangles:
            if rectangle.centery > 750:
                rectangle.centery = -150
            rectangle.centery += 3


bcg = background()
pc = player_car()
enemy = red_car()
gold = coin()

cars = pygame.sprite.Group()
cars.add(pc)
cars.add(enemy)
cars.add(gold)

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(gold)

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # restart game
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == K_r:
                pc.rect.center = (47, 525)
                enemy.rect.centery = -75
                enemy.rect.centerx = random.randint(47, 253)
                enemy.score = 0
                coin_score = 0
                level = 1
                enemy_speed = 10
                gold.rect.centery = random.randint(-500, -50)
                gold.rect.centerx = random.randint(47, 253)
                game_over = False

    if not game_over:
        bcg.draw()
        bcg.move()

        pc.move()
        enemy.move(enemy_speed)
        gold.move(5)
# collect coin
        if pygame.sprite.spritecollideany(pc, coins):
            coin_score += 5
            gold.rect.centery = random.randint(-500, -50)
            gold.rect.centerx = random.randint(47, 253)

        # level and speed
        if enemy.score >= level * 50:
            level += 1
            enemy_speed += 2

        for car in cars:
            screen.blit(car.image, car.rect)

        font = pygame.font.SysFont("open dyslexic", 18)

        text = font.render("Score: " + str(enemy.score + coin_score), True, (0, 0, 0))
        level_text = font.render("Level: " + str(level), True, (0, 0, 0))

        screen.blit(text, (5, 5))
        screen.blit(level_text, (5, 30))

        # collision with enemy
        if pygame.sprite.spritecollideany(pc, enemies):
            game_over = True

    else:
        screen.fill((125, 20, 20))

        go_font = pygame.font.SysFont("times new roman", 18)

        game_over_text = go_font.render(
            "Game Over! Score: " + str(enemy.score + coin_score),
            True,
            (20, 200, 200)
        )

        restart_text = go_font.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        go_rect = game_over_text.get_rect()
        go_rect.center = (width // 2, height // 2)

        restart_rect = restart_text.get_rect()
        restart_rect.center = (width // 2, height // 2 + 30)

        screen.blit(game_over_text, go_rect)
        screen.blit(restart_text, restart_rect)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()