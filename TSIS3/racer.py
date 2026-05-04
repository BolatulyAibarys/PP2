import os
import random
import pygame

from pygame.locals import *

from ui import Button
from persistence import (
    load_settings,
    save_settings,
    load_leaderboard,
    add_score
)


WIDTH = 300
HEIGHT = 600

LANES = [47, 150, 253]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (180, 30, 30)
GREEN = (40, 180, 70)
BLUE = (40, 100, 220)
YELLOW = (240, 210, 40)
GRAY = (90, 90, 90)
DARK_GRAY = (50, 50, 50)
BROWN = (120, 70, 20)
PURPLE = (150, 70, 200)
ORANGE = (230, 140, 20)

ASSETS = "assets"


def load_image(path, size, fallback_color):
    try:
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image
    except Exception:
        image = pygame.Surface(size, pygame.SRCALPHA)
        image.fill(fallback_color)
        return image


def tint_image(image, color):
    tinted = image.copy()
    overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
    overlay.fill(color)
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted


class player_car(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()

        path = os.path.join(ASSETS, "player_car.png")
        base_image = load_image(path, (WIDTH // 4, HEIGHT // 4), GREEN)

        car_color = settings["car_color"]

        if car_color == "red":
            self.image = tint_image(base_image, (255, 100, 100, 255))
        elif car_color == "blue":
            self.image = tint_image(base_image, (100, 130, 255, 255))
        elif car_color == "purple":
            self.image = tint_image(base_image, (190, 120, 255, 255))
        else:
            self.image = base_image

        self.rect = self.image.get_rect()
        self.rect.center = (47, 525)

    def move(self):
        button = pygame.key.get_pressed()

        if button[K_a] or button[K_LEFT]:
            self.rect.centerx -= 5

        elif button[K_d] or button[K_RIGHT]:
            self.rect.centerx += 5

        if self.rect.centerx < 47:
            self.rect.centerx = 47

        if self.rect.centerx > 253:
            self.rect.centerx = 253


class red_car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        path = os.path.join(ASSETS, "enemy_car.png")
        self.image = load_image(path, (WIDTH // 4, HEIGHT // 4), RED)

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.centery = random.randint(-500, -100)

    def move(self, speed):
        self.rect.centery += speed

        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.centerx = random.choice(LANES)
        self.rect.centery = random.randint(-700, -100)


class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.coin_types = [
            {
                "name": "bronze",
                "value": 5,
                "path": os.path.join(ASSETS, "coin_bronze.png"),
                "color": BROWN
            },
            {
                "name": "silver",
                "value": 10,
                "path": os.path.join(ASSETS, "coin_silver.png"),
                "color": GRAY
            },
            {
                "name": "gold",
                "value": 20,
                "path": os.path.join(ASSETS, "coin_gold.png"),
                "color": YELLOW
            }
        ]

        self.image = None
        self.rect = None
        self.value = 5
        self.reset()

    def reset(self):
        coin_type = random.choices(
            self.coin_types,
            weights=[60, 30, 10],
            k=1
        )[0]

        self.value = coin_type["value"]

        self.image = load_image(
            coin_type["path"],
            (28, 28),
            coin_type["color"]
        )

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.centery = random.randint(-600, -50)

    def move(self, speed):
        self.rect.centery += speed

        if self.rect.top > HEIGHT:
            self.reset()


class background:
    def __init__(self):
        path = os.path.join(ASSETS, "road.png")

        self.image = load_image(
            path,
            (WIDTH, HEIGHT // 2),
            DARK_GRAY
        )

        rect1 = self.image.get_rect()
        rect2 = self.image.get_rect()
        rect3 = self.image.get_rect()

        rect1.centery = HEIGHT // 4
        rect2.centery = HEIGHT // 4 + HEIGHT // 2
        rect3.centery = HEIGHT // 4 + HEIGHT

        self.rectangles = [rect1, rect2, rect3]

    def draw(self, screen):
        for rectangle in self.rectangles:
            screen.blit(self.image, rectangle)

    def move(self, speed):
        for rectangle in self.rectangles:
            rectangle.centery += speed

            if rectangle.top >= HEIGHT:
                rectangle.centery = -HEIGHT // 4


class RoadObstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.kind = random.choice(["barrier", "oil", "pothole"])

        self.image = pygame.Surface((55, 35), pygame.SRCALPHA)

        if self.kind == "barrier":
            self.image.fill(ORANGE)
        elif self.kind == "oil":
            self.image.fill(BLACK)
        else:
            self.image.fill(BROWN)

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.centery = random.randint(-900, -100)

    def move(self, speed):
        self.rect.centery += speed

        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.kind = random.choice(["barrier", "oil", "pothole"])

        if self.kind == "barrier":
            self.image.fill(ORANGE)
        elif self.kind == "oil":
            self.image.fill(BLACK)
        else:
            self.image.fill(BROWN)

        self.rect.centerx = random.choice(LANES)
        self.rect.centery = random.randint(-1000, -100)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.power_type = None
        self.spawn_time = 0

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.reset()

    def reset(self):
        self.power_type = random.choice(["nitro", "shield", "repair"])
        self.image.fill((0, 0, 0, 0))

        if self.power_type == "nitro":
            color = BLUE
            letter = "N"
        elif self.power_type == "shield":
            color = PURPLE
            letter = "S"
        else:
            color = GREEN
            letter = "R"

        pygame.draw.circle(self.image, color, (15, 15), 15)

        font = pygame.font.SysFont("arial", 18)
        text = font.render(letter, True, WHITE)
        self.image.blit(text, (15 - text.get_width() // 2, 15 - text.get_height() // 2))

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.centery = random.randint(-1200, -300)

        self.spawn_time = pygame.time.get_ticks()

    def move(self, speed):
        self.rect.centery += speed

        now = pygame.time.get_ticks()

        if self.rect.top > HEIGHT or now - self.spawn_time > 8000:
            self.reset()


class RacerGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Advanced Racer")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("times new roman", 20)
        self.small_font = pygame.font.SysFont("times new roman", 16)
        self.big_font = pygame.font.SysFont("times new roman", 38)

        self.settings = load_settings()

        self.state = "menu"
        self.running = True

        self.username = ""
        self.menu_message = ""

        self.create_buttons()
        self.reset_game()

    def create_buttons(self):
        self.play_button = Button(75, 170, 150, 40, "Play")
        self.leaderboard_button = Button(75, 225, 150, 40, "Leaderboard")
        self.settings_button = Button(75, 280, 150, 40, "Settings")
        self.quit_button = Button(75, 335, 150, 40, "Quit")

        self.retry_button = Button(45, 350, 90, 35, "Retry")
        self.menu_button = Button(160, 350, 100, 35, "Menu")

        self.back_button = Button(85, 530, 130, 35, "Back")

        self.sound_button = Button(55, 190, 190, 35, "Toggle Sound")
        self.color_button = Button(55, 245, 190, 35, "Car Color")
        self.difficulty_button = Button(55, 300, 190, 35, "Difficulty")
        self.save_settings_button = Button(55, 355, 190, 35, "Save & Back")

    def reset_game(self):
        self.game_over_saved = False

        self.level = 1
        self.coin_score = 0
        self.coins_collected = 0
        self.distance = 0

        if self.settings["difficulty"] == "easy":
            self.enemy_speed = 2
            enemy_count = 1
            obstacle_count = 1
        elif self.settings["difficulty"] == "hard":
            self.enemy_speed = 6
            enemy_count = 1
            obstacle_count = 3
        else:
            self.enemy_speed = 4
            enemy_count = 1
            obstacle_count = 2

        self.road_speed = 3

        self.nitro_active = False
        self.nitro_until = 0
        self.shield_active = False

        self.repair_count = 0

        self.bcg = background()
        self.pc = player_car(self.settings)

        self.enemies = pygame.sprite.Group()
        for i in range(enemy_count):
            self.enemies.add(red_car())

        self.coins = pygame.sprite.Group()
        self.coins.add(coin())

        self.obstacles = pygame.sprite.Group()
        for i in range(obstacle_count):
            self.obstacles.add(RoadObstacle())

        self.powerups = pygame.sprite.Group()
        self.powerups.add(PowerUp())

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pc)

        for enemy in self.enemies:
            self.all_sprites.add(enemy)

        for item in self.coins:
            self.all_sprites.add(item)

        for obstacle in self.obstacles:
            self.all_sprites.add(obstacle)

        for powerup in self.powerups:
            self.all_sprites.add(powerup)

    def run(self):
        while self.running:
            self.handle_events()

            if self.state == "playing":
                self.update_game()

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "menu":
                self.handle_menu_event(event)

            elif self.state == "playing":
                self.handle_playing_event(event)

            elif self.state == "game_over":
                self.handle_game_over_event(event)

            elif self.state == "leaderboard":
                self.handle_leaderboard_event(event)

            elif self.state == "settings":
                self.handle_settings_event(event)

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_BACKSPACE:
                self.username = self.username[:-1]

            elif event.key == K_RETURN:
                self.start_game()

            else:
                if len(self.username) < 12:
                    if event.unicode.isalnum() or event.unicode in "_-":
                        self.username += event.unicode

        if self.play_button.clicked(event):
            self.start_game()

        elif self.leaderboard_button.clicked(event):
            self.state = "leaderboard"

        elif self.settings_button.clicked(event):
            self.state = "settings"

        elif self.quit_button.clicked(event):
            self.running = False

    def start_game(self):
        if self.username.strip() == "":
            self.menu_message = "Enter username first"
            return

        self.username = self.username.strip()
        self.menu_message = ""
        self.reset_game()
        self.state = "playing"

    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                self.state = "menu"

    def handle_game_over_event(self, event):
        if self.retry_button.clicked(event):
            self.reset_game()
            self.state = "playing"

        elif self.menu_button.clicked(event):
            self.state = "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == K_r:
                self.reset_game()
                self.state = "playing"

            elif event.key == K_m:
                self.state = "menu"

    def handle_leaderboard_event(self, event):
        if self.back_button.clicked(event):
            self.state = "menu"

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            self.state = "menu"

    def handle_settings_event(self, event):
        if self.sound_button.clicked(event):
            self.settings["sound"] = not self.settings["sound"]

        elif self.color_button.clicked(event):
            self.change_car_color()

        elif self.difficulty_button.clicked(event):
            self.change_difficulty()

        elif self.save_settings_button.clicked(event):
            save_settings(self.settings)
            self.state = "menu"

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            self.state = "menu"

    def change_car_color(self):
        colors = ["green", "red", "blue", "purple"]

        current = self.settings["car_color"]

        if current in colors:
            index = colors.index(current)
            self.settings["car_color"] = colors[(index + 1) % len(colors)]
        else:
            self.settings["car_color"] = "green"

    def change_difficulty(self):
        difficulties = ["easy", "normal", "hard"]

        current = self.settings["difficulty"]

        if current in difficulties:
            index = difficulties.index(current)
            self.settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
        else:
            self.settings["difficulty"] = "normal"

    def update_game(self):
        self.update_power_timers()

        current_speed = self.enemy_speed

        if self.nitro_active:
            current_speed += 2

        self.distance += current_speed // 2

        self.bcg.move(self.road_speed + current_speed // 5)

        self.pc.move()

        enemy_move_speed = current_speed
        coin_speed = max(3, current_speed // 2)
        obstacle_speed = max(3, current_speed // 2)
        powerup_speed = max(3, current_speed // 2)

        for enemy in self.enemies:
            enemy.move(enemy_move_speed)

        for item in self.coins:
            item.move(coin_speed)

        for obstacle in self.obstacles:
            obstacle.move(obstacle_speed)

        for powerup in self.powerups:
            powerup.move(powerup_speed)

        self.check_coin_collision()
        self.check_powerup_collision()
        self.check_obstacle_collision()
        self.check_enemy_collision()

        self.scale_difficulty()

    def update_power_timers(self):
        now = pygame.time.get_ticks()

        if self.nitro_active and now > self.nitro_until:
            self.nitro_active = False

    def check_coin_collision(self):
        collected_coin = pygame.sprite.spritecollideany(self.pc, self.coins)

        if collected_coin:
            self.coin_score += collected_coin.value
            self.coins_collected += 1
            collected_coin.reset()

            if self.settings["sound"]:
                self.play_sound("crash.wav")

    def check_powerup_collision(self):
        collected_powerup = pygame.sprite.spritecollideany(self.pc, self.powerups)

        if collected_powerup:
            self.activate_powerup(collected_powerup.power_type)
            collected_powerup.reset()

    def activate_powerup(self, power_type):
        now = pygame.time.get_ticks()

        if power_type == "nitro":
            self.nitro_active = True
            self.nitro_until = now + 4000

        elif power_type == "shield":
            self.shield_active = True

        elif power_type == "repair":
            self.repair_count += 1

            first_obstacle = None

            for obstacle in self.obstacles:
                first_obstacle = obstacle
                break

            if first_obstacle is not None:
                first_obstacle.reset()

    def check_obstacle_collision(self):
        hit_obstacle = pygame.sprite.spritecollideany(self.pc, self.obstacles)

        if hit_obstacle:
            if hit_obstacle.kind == "oil":
                self.pc.rect.centerx -= random.choice([-30, 30])
                hit_obstacle.reset()

            elif self.shield_active:
                self.shield_active = False
                hit_obstacle.reset()

            else:
                self.end_game()

    def check_enemy_collision(self):
        hit_enemy = pygame.sprite.spritecollideany(self.pc, self.enemies)

        if hit_enemy:
            if self.shield_active:
                self.shield_active = False
                hit_enemy.reset()

            elif self.repair_count > 0:
                self.repair_count -= 1
                hit_enemy.reset()

            else:
                self.end_game()

    def scale_difficulty(self):
        new_level = self.distance // 1000 + 1

        if new_level > self.level:
            self.level = new_level
            
            if self.level % 2 == 0:
                self.enemy_speed = min(self.enemy_speed + 1, 9)

            if self.level % 3 == 0 and len(self.obstacles) < 5:
                self.obstacles.add(RoadObstacle())

    def calculate_score(self):
        powerup_bonus = self.repair_count * 10

        score = self.coin_score + self.distance // 10 + powerup_bonus

        return score

    def end_game(self):
        if not self.game_over_saved:
            final_score = self.calculate_score()

            add_score(
                self.username,
                final_score,
                self.coins_collected,
                self.distance
            )

            self.game_over_saved = True

        self.state = "game_over"

    def play_sound(self, filename):
        try:
            path = os.path.join(ASSETS, filename)
            sound = pygame.mixer.Sound(path)
            sound.play()
        except Exception:
            pass

    def draw(self):
        if self.state == "menu":
            self.draw_menu()

        elif self.state == "playing":
            self.draw_game()

        elif self.state == "game_over":
            self.draw_game_over()

        elif self.state == "leaderboard":
            self.draw_leaderboard()

        elif self.state == "settings":
            self.draw_settings()

    def draw_menu(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("Advanced Racer", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

        label = self.font.render("Username:", True, BLACK)
        self.screen.blit(label, (60, 120))

        input_rect = pygame.Rect(150, 118, 90, 28)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 2)

        username_text = self.font.render(self.username, True, BLACK)
        self.screen.blit(username_text, (input_rect.x + 5, input_rect.y + 2))

        if self.menu_message:
            msg = self.small_font.render(self.menu_message, True, RED)
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 145))

        self.play_button.draw(self.screen, self.font)
        self.leaderboard_button.draw(self.screen, self.font)
        self.settings_button.draw(self.screen, self.font)
        self.quit_button.draw(self.screen, self.font)

    def draw_game(self):
        self.screen.fill(WHITE)

        self.bcg.draw(self.screen)

        for obstacle in self.obstacles:
            self.screen.blit(obstacle.image, obstacle.rect)

        for item in self.coins:
            self.screen.blit(item.image, item.rect)

        for powerup in self.powerups:
            self.screen.blit(powerup.image, powerup.rect)

        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect)

        self.screen.blit(self.pc.image, self.pc.rect)

        self.draw_hud()

    def draw_hud(self):
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, 90))

        score_text = self.small_font.render("Score: " + str(self.calculate_score()), True, BLACK)
        coins_text = self.small_font.render("Coins: " + str(self.coins_collected), True, BLACK)
        distance_text = self.small_font.render("Distance: " + str(self.distance), True, BLACK)
        level_text = self.small_font.render("Level: " + str(self.level), True, BLACK)

        self.screen.blit(score_text, (5, 5))
        self.screen.blit(coins_text, (5, 25))
        self.screen.blit(distance_text, (5, 45))
        self.screen.blit(level_text, (5, 65))

        effect = ""

        if self.nitro_active:
            remaining = max(0, (self.nitro_until - pygame.time.get_ticks()) // 1000)
            effect = "Nitro: " + str(remaining)

        elif self.shield_active:
            effect = "Shield"

        elif self.repair_count > 0:
            effect = "Repair: " + str(self.repair_count)

        if effect:
            effect_text = self.small_font.render(effect, True, BLUE)
            self.screen.blit(effect_text, (185, 5))

    def draw_game_over(self):
        self.screen.fill((125, 20, 20))

        final_score = self.calculate_score()

        title = self.big_font.render("GAME OVER", True, WHITE)
        score_text = self.font.render("Score: " + str(final_score), True, WHITE)
        coin_text = self.font.render("Coins: " + str(self.coins_collected), True, WHITE)
        distance_text = self.font.render("Distance: " + str(self.distance), True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        self.screen.blit(score_text, (90, 190))
        self.screen.blit(coin_text, (90, 220))
        self.screen.blit(distance_text, (90, 250))

        self.retry_button.draw(self.screen, self.font)
        self.menu_button.draw(self.screen, self.font)

    def draw_leaderboard(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("Leaderboard", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        leaderboard = load_leaderboard()

        y = 100

        if len(leaderboard) == 0:
            text = self.font.render("No scores yet", True, RED)
            self.screen.blit(text, (90, 150))

        else:
            for index, item in enumerate(leaderboard):
                line = (
                    str(index + 1)
                    + ". "
                    + item["username"][:7]
                    + " | "
                    + str(item["score"])
                    + " | "
                    + str(item["distance"])
                )

                text = self.small_font.render(line, True, BLACK)
                self.screen.blit(text, (35, y))
                y += 35

        self.back_button.draw(self.screen, self.font)

    def draw_settings(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("Settings", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        sound_text = "Sound: ON" if self.settings["sound"] else "Sound: OFF"
        color_text = "Car color: " + self.settings["car_color"]
        diff_text = "Difficulty: " + self.settings["difficulty"]

        self.screen.blit(self.small_font.render(sound_text, True, BLACK), (70, 150))
        self.screen.blit(self.small_font.render(color_text, True, BLACK), (70, 205))
        self.screen.blit(self.small_font.render(diff_text, True, BLACK), (70, 260))

        self.sound_button.draw(self.screen, self.font)
        self.color_button.draw(self.screen, self.font)
        self.difficulty_button.draw(self.screen, self.font)
        self.save_settings_button.draw(self.screen, self.font)