import json
import os
import random
import pygame

from config import (
    WIDTH,
    HEIGHT,
    CELL_SIZE,
    FPS_START,
    LEVEL_UP_EVERY,
    WHITE,
    BLACK,
    GREEN,
    DARK_GREEN,
    ORANGE,
    YELLOW,
    RED,
    DARK_RED,
    BLUE,
    PURPLE,
    GRAY,
    LIGHT_GRAY,
)

try:
    from db import init_db, save_result, get_top_scores, get_personal_best
except Exception as e:
    print("Database module error:", e)

    def init_db():
        pass

    def save_result(username, score, level_reached):
        pass

    def get_top_scores(limit=10):
        return []

    def get_personal_best(username):
        return 0


HUD_HEIGHT = 40
SETTINGS_FILE = "settings.json"


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = (200, 200, 200)
        else:
            color = LIGHT_GRAY

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2

        screen.blit(text_surface, (text_x, text_y))

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Advanced Snake")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("times new roman", 22)
        self.big_font = pygame.font.SysFont("times new roman", 44)
        self.small_font = pygame.font.SysFont("times new roman", 18)

        init_db()

        self.settings = self.load_settings()

        self.load_sounds()

        self.state = "menu"
        self.running = True

        self.username = ""
        self.menu_message = ""

        self.leaderboard_rows = []

        self.create_buttons()
        self.reset_game()

    def create_buttons(self):
        self.play_button = Button(220, 150, 160, 40, "Play")
        self.leaderboard_button = Button(220, 205, 160, 40, "Leaderboard")
        self.settings_button = Button(220, 260, 160, 40, "Settings")
        self.quit_button = Button(220, 315, 160, 40, "Quit")

        self.retry_button = Button(190, 250, 100, 40, "Retry")
        self.menu_button = Button(310, 250, 120, 40, "Main Menu")

        self.back_button = Button(230, 340, 140, 35, "Back")

        self.grid_button = Button(200, 150, 200, 35, "Toggle Grid")
        self.sound_button = Button(200, 200, 200, 35, "Toggle Sound")
        self.color_button = Button(200, 250, 200, 35, "Change Color")
        self.save_settings_button = Button(200, 310, 200, 35, "Save & Back")

    def load_settings(self):
        default_settings = {
            "snake_color": [50, 200, 50],
            "grid": False,
            "sound": True,
        }

        if not os.path.exists(SETTINGS_FILE):
            return default_settings

        try:
            with open(SETTINGS_FILE, "r") as file:
                data = json.load(file)

            for key in default_settings:
                if key not in data:
                    data[key] = default_settings[key]

            return data

        except Exception:
            return default_settings

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def load_sounds(self):
        self.sfx_lib = {}

        try:
            pygame.mixer.init()
        except Exception as e:
            print("Mixer init error:", e)

        try:
            pygame.mixer.music.load("assets/music.mp3")
            pygame.mixer.music.set_volume(0.3)

            if self.settings["sound"]:
                pygame.mixer.music.play(-1)
        except Exception as e:
            print("Music load error:", e)


    def load_sfx(self, path):
        try:
            sfx = self.sfx_lib.get(path)

            if sfx is None:
                sfx = pygame.mixer.Sound(path)
                self.sfx_lib[path] = sfx

            return sfx

        except Exception as e:
            print("Sound load error:", e)
            return None


    def play_sfx(self, path):
        if not self.settings["sound"]:
            return

        sfx = self.load_sfx(path)

        if sfx is not None:
            sfx.play()


    def reset_game(self):
        self.segments = [
            [50, 80],
            [60, 80],
            [70, 80],
            [80, 80],
        ]

        self.direction = "r"
        self.next_direction = "r"
        self.score = 0
        self.foods_eaten = 0
        self.level = 1
        self.speed = FPS_START

        self.game_over_saved = False

        self.obstacles = []

        self.active_powerup = None
        self.active_powerup_until = 0
        self.shield_active = False

        self.powerup = None
        self.poison_food = None

        self.next_powerup_spawn_time = pygame.time.get_ticks() + random.randint(4000, 8000)

        self.food = self.generate_food()
        self.poison_food = self.generate_empty_cell(extra=[self.food["pos"]])

        self.personal_best = 0
        if self.username.strip() != "":
            self.personal_best = get_personal_best(self.username.strip())

        self.last_move_time = pygame.time.get_ticks()

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
            if event.key == pygame.K_RETURN:
                self.start_game()

            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]

            else:
                if len(self.username) < 15:
                    if event.unicode.isalnum() or event.unicode in "_-":
                        self.username += event.unicode

        if self.play_button.clicked(event):
            self.start_game()

        elif self.leaderboard_button.clicked(event):
            self.leaderboard_rows = get_top_scores(10)
            self.state = "leaderboard"

        elif self.settings_button.clicked(event):
            self.state = "settings"

        elif self.quit_button.clicked(event):
            self.running = False

    def start_game(self):
        self.username = self.username.strip()

        if self.username == "":
            self.menu_message = "Enter username first"
            return

        self.menu_message = ""
        self.reset_game()
        self.state = "playing"

    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.state = "menu"

            elif event.key == pygame.K_UP and self.direction != "d":
                self.next_direction = "u"

            elif event.key == pygame.K_DOWN and self.direction != "u":
                self.next_direction = "d"

            elif event.key == pygame.K_LEFT and self.direction != "r":
                self.next_direction = "l"

            elif event.key == pygame.K_RIGHT and self.direction != "l":
                self.next_direction = "r"

    def handle_game_over_event(self, event):
        if self.retry_button.clicked(event):
            self.reset_game()
            self.state = "playing"

        elif self.menu_button.clicked(event):
            self.state = "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
                self.state = "playing"

            elif event.key == pygame.K_m:
                self.state = "menu"

    def handle_leaderboard_event(self, event):
        if self.back_button.clicked(event):
            self.state = "menu"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = "menu"

    def handle_settings_event(self, event):
        if self.grid_button.clicked(event):
            self.settings["grid"] = not self.settings["grid"]

        elif self.sound_button.clicked(event):
            self.settings["sound"] = not self.settings["sound"]

            if self.settings["sound"]:
                try:
                    pygame.mixer.music.play(-1)
                except:
                    pass
            else:
                try:
                    pygame.mixer.music.stop()
                except:
                    pass

        elif self.color_button.clicked(event):
            self.change_snake_color()

        elif self.save_settings_button.clicked(event):
            self.save_settings()
            self.state = "menu"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = "menu"

    def change_snake_color(self):
        colors = [
            [50, 200, 50],
            [220, 40, 40],
            [40, 100, 220],
            [150, 60, 200],
            [240, 200, 0],
        ]

        current_color = self.settings["snake_color"]

        if current_color in colors:
            index = colors.index(current_color)
            index = (index + 1) % len(colors)
            self.settings["snake_color"] = colors[index]
        else:
            self.settings["snake_color"] = colors[0]

    def update_game(self):
        now = pygame.time.get_ticks()

        self.update_timers(now)

        move_delay = 1000 // self.get_current_speed()

        if now - self.last_move_time >= move_delay:
            self.move_snake()
            self.last_move_time = now

    def update_timers(self, now):
        if now >= self.food["expires_at"]:
            self.food = self.generate_food()

        if self.powerup is not None:
            if now >= self.powerup["expires_at"]:
                self.powerup = None
                self.next_powerup_spawn_time = now + random.randint(4000, 8000)

        if self.powerup is None and now >= self.next_powerup_spawn_time:
            self.spawn_powerup()
            self.next_powerup_spawn_time = now + random.randint(9000, 14000)

        if self.active_powerup in ("speed", "slow"):
            if now >= self.active_powerup_until:
                self.active_powerup = None
                self.active_powerup_until = 0

    def get_current_speed(self):
        if self.active_powerup == "speed":
            return self.speed + 4

        if self.active_powerup == "slow":
            return max(2, self.speed - 3)

        return self.speed

    def move_snake(self):
        self.direction = self.next_direction

        head = self.segments[-1]
        new_head = [head[0], head[1]]

        if self.direction == "r":
            new_head[0] += CELL_SIZE
        elif self.direction == "l":
            new_head[0] -= CELL_SIZE
        elif self.direction == "u":
            new_head[1] -= CELL_SIZE
        elif self.direction == "d":
            new_head[1] += CELL_SIZE

        new_head = self.check_border_collision(new_head)

        if new_head is None:
            return

        if new_head in self.obstacles:
            if self.shield_active:
                self.shield_active = False
                self.obstacles.remove(new_head)
            else:
                self.end_game()
                return

        if new_head in self.segments[:-1]:
            if self.shield_active:
                self.shield_active = False
            else:
                self.end_game()
                return

        ate_food = new_head == self.food["pos"]
        ate_poison = self.poison_food is not None and new_head == self.poison_food
        ate_powerup = self.powerup is not None and new_head == self.powerup["pos"]

        self.segments.append(new_head)

        if not ate_food:
            self.segments.pop(0)

        if ate_food:
            self.score += self.food["points"]
            self.foods_eaten += 1

            self.play_sfx("assets/fruit.mp3")


            self.food = self.generate_food()

            if self.foods_eaten % LEVEL_UP_EVERY == 0:
                self.level_up()

        if ate_poison:
            self.play_sfx("assets/hit.mp3")
            self.shorten_snake(2)

            if len(self.segments) <= 1:
                self.end_game()
                return

            self.poison_food = self.generate_empty_cell(extra=[self.food["pos"]])

        if ate_powerup:
            self.play_sfx("assets/p_up.mp3")
            self.activate_powerup(self.powerup["type"])
            self.powerup = None
            self.next_powerup_spawn_time = pygame.time.get_ticks() + random.randint(6000, 10000)

    def check_border_collision(self, new_head):
        x, y = new_head

        hit_border = (
            x < 0
            or x >= WIDTH
            or y < HUD_HEIGHT
            or y >= HEIGHT
        )

        if not hit_border:
            return new_head

        if not self.shield_active:
            self.end_game()
            return None

        self.shield_active = False

        if x < 0:
            x = WIDTH - CELL_SIZE
        elif x >= WIDTH:
            x = 0

        if y < HUD_HEIGHT:
            y = HEIGHT - CELL_SIZE
        elif y >= HEIGHT:
            y = HUD_HEIGHT

        return [x, y]

    def shorten_snake(self, amount):
        for i in range(amount):
            if len(self.segments) > 0:
                self.segments.pop(0)

    def level_up(self):
        self.level += 1
        self.speed += 1

        if self.level >= 3:
            self.obstacles = self.generate_obstacles()

    def end_game(self):
        if not self.game_over_saved:
            save_result(self.username, self.score, self.level)
            self.game_over_saved = True

        self.personal_best = max(self.personal_best, self.score)
        self.state = "game_over"

    def generate_food(self):
        food_type = random.choices(
            ["normal", "bonus", "gold"],
            weights=[70, 25, 5],
            k=1
        )[0]

        if food_type == "normal":
            points = 1
            color = ORANGE
            lifetime = 9000

        elif food_type == "bonus":
            points = 3
            color = YELLOW
            lifetime = 7000

        else:
            points = 5
            color = PURPLE
            lifetime = 5000

        position = self.generate_empty_cell()

        return {
            "type": food_type,
            "pos": position,
            "points": points,
            "color": color,
            "expires_at": pygame.time.get_ticks() + lifetime,
        }

    def generate_empty_cell(self, extra=None):
        if extra is None:
            extra = []

        blocked = []

        for segment in self.segments:
            blocked.append(segment)

        for obstacle in self.obstacles:
            blocked.append(obstacle)

        for item in extra:
            if item is not None:
                blocked.append(item)

        if self.powerup is not None:
            blocked.append(self.powerup["pos"])

        if hasattr(self, "poison_food") and self.poison_food is not None:
            blocked.append(self.poison_food)

        for attempt in range(1000):
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(HUD_HEIGHT, HEIGHT, CELL_SIZE)

            position = [x, y]

            if position not in blocked:
                return position

        return [100, 100]

    def generate_obstacles(self):
        obstacles = []

        head = self.segments[-1]

        count = min(8 + self.level * 2, 35)

        for i in range(count):
            for attempt in range(200):
                x = random.randrange(0, WIDTH, CELL_SIZE)
                y = random.randrange(HUD_HEIGHT, HEIGHT, CELL_SIZE)

                position = [x, y]

                too_close_to_head = (
                    abs(position[0] - head[0]) <= 30
                    and abs(position[1] - head[1]) <= 30
                )

                if (
                    position not in self.segments
                    and position not in obstacles
                    and position != self.food["pos"]
                    and position != self.poison_food
                    and not too_close_to_head
                ):
                    obstacles.append(position)
                    break

        return obstacles

    def spawn_powerup(self):
        powerup_type = random.choice(["speed", "slow", "shield"])

        if powerup_type == "speed":
            color = BLUE
        elif powerup_type == "slow":
            color = PURPLE
        else:
            color = DARK_GREEN

        position = self.generate_empty_cell(extra=[self.food["pos"], self.poison_food])

        self.powerup = {
            "type": powerup_type,
            "pos": position,
            "color": color,
            "expires_at": pygame.time.get_ticks() + 8000,
        }

    def activate_powerup(self, powerup_type):
        now = pygame.time.get_ticks()

        if powerup_type == "speed":
            self.active_powerup = "speed"
            self.active_powerup_until = now + 5000

        elif powerup_type == "slow":
            self.active_powerup = "slow"
            self.active_powerup_until = now + 5000

        elif powerup_type == "shield":
            self.active_powerup = "shield"
            self.shield_active = True

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

        title = self.big_font.render("Advanced Snake", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 55))

        label = self.font.render("Enter username:", True, BLACK)
        self.screen.blit(label, (210, 105))

        input_rect = pygame.Rect(210, 125, 180, 28)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 2)

        username_text = self.font.render(self.username, True, BLACK)
        self.screen.blit(username_text, (input_rect.x + 5, input_rect.y + 2))

        if self.menu_message:
            msg = self.small_font.render(self.menu_message, True, RED)
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 365))

        self.play_button.draw(self.screen, self.font)
        self.leaderboard_button.draw(self.screen, self.font)
        self.settings_button.draw(self.screen, self.font)
        self.quit_button.draw(self.screen, self.font)

    def draw_game(self):
        self.screen.fill(WHITE)

        self.draw_hud()

        if self.settings["grid"]:
            self.draw_grid()

        for obstacle in self.obstacles:
            pygame.draw.rect(
                self.screen,
                GRAY,
                pygame.Rect(obstacle[0], obstacle[1], CELL_SIZE - 1, CELL_SIZE - 1)
            )

        pygame.draw.rect(
            self.screen,
            self.food["color"],
            pygame.Rect(self.food["pos"][0], self.food["pos"][1], CELL_SIZE - 1, CELL_SIZE - 1)
        )

        if self.poison_food is not None:
            pygame.draw.rect(
                self.screen,
                DARK_RED,
                pygame.Rect(self.poison_food[0], self.poison_food[1], CELL_SIZE - 1, CELL_SIZE - 1)
            )

        if self.powerup is not None:
            pygame.draw.rect(
                self.screen,
                self.powerup["color"],
                pygame.Rect(self.powerup["pos"][0], self.powerup["pos"][1], CELL_SIZE - 1, CELL_SIZE - 1)
            )

            letter = self.get_powerup_letter(self.powerup["type"])
            letter_surface = self.small_font.render(letter, True, WHITE)
            self.screen.blit(letter_surface, (self.powerup["pos"][0] + 1, self.powerup["pos"][1] - 3))

        snake_color = tuple(self.settings["snake_color"])

        for index, segment in enumerate(self.segments):
            if index == len(self.segments) - 1:
                color = DARK_GREEN
            else:
                color = snake_color

            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(segment[0], segment[1], CELL_SIZE - 1, CELL_SIZE - 1)
            )

    def get_powerup_letter(self, powerup_type):
        if powerup_type == "speed":
            return "B"

        if powerup_type == "slow":
            return "S"

        return "H"

    def draw_hud(self):
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, 0, WIDTH, HUD_HEIGHT))
        pygame.draw.line(self.screen, BLACK, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)

        text = (
            "Score: " + str(self.score)
            + "   Level: " + str(self.level)
            + "   Best: " + str(self.personal_best)
            + "   Speed: " + str(self.get_current_speed())
        )

        hud_text = self.small_font.render(text, True, BLACK)
        self.screen.blit(hud_text, (10, 8))

        effect_text = ""

        if self.active_powerup == "speed":
            effect_text = "Speed boost"

        elif self.active_powerup == "slow":
            effect_text = "Slow motion"

        elif self.shield_active:
            effect_text = "Shield active"

        if effect_text:
            effect_surface = self.small_font.render(effect_text, True, BLUE)
            self.screen.blit(effect_surface, (430, 8))

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (x, HUD_HEIGHT), (x, HEIGHT))

        for y in range(HUD_HEIGHT, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (0, y), (WIDTH, y))

    def draw_game_over(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("GAME OVER", True, RED)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        score_text = self.font.render("Final score: " + str(self.score), True, BLACK)
        level_text = self.font.render("Level reached: " + str(self.level), True, BLACK)
        best_text = self.font.render("Personal best: " + str(self.personal_best), True, BLACK)

        self.screen.blit(score_text, (220, 150))
        self.screen.blit(level_text, (220, 180))
        self.screen.blit(best_text, (220, 210))

        self.retry_button.draw(self.screen, self.font)
        self.menu_button.draw(self.screen, self.font)

        hint = self.small_font.render("R - retry, M - main menu", True, GRAY)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 310))

    def draw_leaderboard(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("Leaderboard", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        headers = self.font.render("Rank   Username        Score   Level   Date", True, BLACK)
        self.screen.blit(headers, (70, 95))

        y = 130

        if len(self.leaderboard_rows) == 0:
            empty = self.font.render("No results yet or database is not connected.", True, RED)
            self.screen.blit(empty, (100, 160))

        else:
            for index, row in enumerate(self.leaderboard_rows):
                username, score, level_reached, played_at = row

                date_text = str(played_at).split(".")[0]

                line = (
                    str(index + 1) + ".      "
                    + str(username)[:12].ljust(12)
                    + "   "
                    + str(score).ljust(5)
                    + "   "
                    + str(level_reached).ljust(5)
                    + "   "
                    + date_text[:10]
                )

                line_surface = self.small_font.render(line, True, BLACK)
                self.screen.blit(line_surface, (70, y))
                y += 25

        self.back_button.draw(self.screen, self.font)

    def draw_settings(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("Settings", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 45))

        grid_text = "Grid: ON" if self.settings["grid"] else "Grid: OFF"
        sound_text = "Sound: ON" if self.settings["sound"] else "Sound: OFF"

        grid_surface = self.font.render(grid_text, True, BLACK)
        sound_surface = self.font.render(sound_text, True, BLACK)
        color_surface = self.font.render("Snake color:", True, BLACK)

        self.screen.blit(grid_surface, (80, 155))
        self.screen.blit(sound_surface, (80, 205))
        self.screen.blit(color_surface, (80, 255))

        pygame.draw.rect(
            self.screen,
            tuple(self.settings["snake_color"]),
            pygame.Rect(420, 252, 35, 25)
        )
        pygame.draw.rect(
            self.screen,
            BLACK,
            pygame.Rect(420, 252, 35, 25),
            2
        )

        self.grid_button.draw(self.screen, self.font)
        self.sound_button.draw(self.screen, self.font)
        self.color_button.draw(self.screen, self.font)
        self.save_settings_button.draw(self.screen, self.font)