import pygame
from ball import Ball


def main():
    pygame.init()

    WIDTH = 500
    HEIGHT = 500
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")

    clock = pygame.time.Clock()

    ball = Ball(
        x=WIDTH // 2,
        y=HEIGHT // 2,
        radius=25,
        color=RED,
        screen_width=WIDTH,
        screen_height=HEIGHT,
        step=20
    )

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move_up()
                elif event.key == pygame.K_DOWN:
                    ball.move_down()
                elif event.key == pygame.K_LEFT:
                    ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    ball.move_right()

        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()