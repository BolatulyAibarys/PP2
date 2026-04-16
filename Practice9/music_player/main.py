import pygame
from player import MusicPlayer


pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")

player = MusicPlayer()
player.play()

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SPACE — пауза
            if event.key == pygame.K_SPACE:
                player.toggle_pause()

            # → следующий
            if event.key == pygame.K_RIGHT:
                player.next_track()

            # ← предыдущий
            if event.key == pygame.K_LEFT:
                player.previous_track()

    pygame.display.update()

pygame.quit()