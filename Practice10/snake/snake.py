import pygame
from pygame.locals import *
import random
pygame.init()
screen = pygame.display.set_mode((600, 400))
running = True
x = 50
y = 50

fruit_color = (200, 120, 0)
snake_color = (50, 200, 50)
segments = [[50, 50], [60, 50], [70, 50], [80, 50]]

dir = "r"
score = 0
level = 1
speed = 10

eaten = False
game_over = False

image_lib = {}

def load_image(path):
    loaded_image = image_lib.get(path)
    if loaded_image == None:
        loaded_image = pygame.image.load(path)
        image_lib[path] = loaded_image
    return loaded_image

sfx_lib = {}

def load_sfx(path):
    sfx = sfx_lib.get(path)
    if sfx == None:
        sfx = pygame.mixer.Sound(path)
        sfx_lib[path] = sfx
    return sfx

# Generate random fruit position
def generate_fruit():
    while True:
        fx = random.randrange(0, 600, 10)
        fy = random.randrange(0, 400, 10)

        fruit_rect = pygame.Rect(fx, fy, 9, 9)

        # fruit cannot be on snake or wall
        if [fx, fy] not in segments:
            return [fx, fy]

fruit = generate_fruit()

# music and sound, use only if files exist
try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play()
except:
    pass

clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            snake_color = (255, 0, 0)
            try:
                load_sfx("sound.mp3").play()
            except:
                pass

        # restart after game over
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                segments = [[50, 50], [60, 50], [70, 50], [80, 50]]
                dir = "r"
                score = 0
                level = 1
                speed = 3
                fruit = generate_fruit()
                game_over = False

    if not game_over:
        klava = pygame.key.get_pressed()

        if klava[K_UP] and dir != "d":
            dir = "u"
        elif klava[K_DOWN] and dir != "u":
            dir = "d"
        elif klava[K_LEFT] and dir != "r":
            dir = "l"
        elif klava[K_RIGHT] and dir != "l":
            dir = "r"

        x = segments[-1][0]
        y = segments[-1][1]

        if dir == "r":
            segments[-1][0] += 10
        if dir == "l":
            segments[-1][0] -= 10
        if dir == "u":
            segments[-1][1] -= 10
        if dir == "d":
            segments[-1][1] += 10

        head_rect = pygame.Rect(segments[-1][0], segments[-1][1], 9, 9)

        # check border collision
        if segments[-1][0] < 0 or segments[-1][0] >= 600 or segments[-1][1] < 0 or segments[-1][1] >= 400:
            game_over = True

        # check collision with snake body
        if segments[-1] in segments[:-1]:
            game_over = True

        if segments[-1][0] == fruit[0] and segments[-1][1] == fruit[1]:
            eaten = True
            score += 1
            fruit = generate_fruit()

            # Add levels after every 4 foods
            if score % 4 == 0:
                level += 1
                speed += 1
        else:
            eaten = False

        for i in range(0, len(segments) - 1):
            segments[i][0] = segments[i + 1][0]
            segments[i][1] = segments[i + 1][1]

        segments[len(segments) - 2][0] = x
        segments[len(segments) - 2][1] = y

        # if food is eaten, snake grows
        if eaten:
            segments.insert(0, [x, y])

    screen.fill((255, 255, 255))

    for segment in segments:
        pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0], segment[1], 9, 9))

    pygame.draw.rect(screen, fruit_color, pygame.Rect(fruit[0], fruit[1], 9, 9))

    font = pygame.font.SysFont("times new roman", 20)

    text = font.render("Score: " + str(score), True, (0, 0, 0))
    level_text = font.render("Level: " + str(level), True, (0, 0, 0))

    screen.blit(text, (10, 0))
    screen.blit(level_text, (10, 25))

    if game_over:
        over_text = font.render("GAME OVER! Press R to restart", True, (255, 0, 0))
        screen.blit(over_text, (170, 180))

    clock.tick(speed)
    pygame.display.flip()

pygame.quit()