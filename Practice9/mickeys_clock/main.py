import pygame
from clock import MickeyClock


def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mickey's Clock Application")

    app_clock = pygame.time.Clock()
    mickey_clock = MickeyClock(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mickey_clock.draw()

        pygame.display.flip()
        app_clock.tick(1)  # обновление раз в секунду

    pygame.quit()


if __name__ == "__main__":
    main()