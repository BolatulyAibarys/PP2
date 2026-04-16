import pygame
import datetime
import os


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.width = 600
        self.height = 600
        self.center = (self.width // 2, self.height // 2)

        base_path = os.path.dirname(__file__)

        self.clock_image = pygame.image.load(
            os.path.join(base_path, "images", "clock.png")
        ).convert_alpha()

        self.hand_image = pygame.image.load(
            os.path.join(base_path, "images", "mickey_hand.png")
        ).convert_alpha()

        self.clock_image = pygame.transform.scale(self.clock_image, (600, 600))

        # одна и та же рука, но для минут и секунд сделаем разный размер
        self.minute_hand = pygame.transform.scale(self.hand_image, (140, 140))
        self.second_hand = pygame.transform.scale(self.hand_image, (180, 180))

    def rotate_image(self, image, angle, center):
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=center)
        return rotated_image, rotated_rect

    def draw(self):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = -minutes * 6
        second_angle = -seconds * 6

        self.screen.blit(self.clock_image, (0, 0))

        minute_rotated, minute_rect = self.rotate_image(
            self.minute_hand, minute_angle, self.center
        )
        second_rotated, second_rect = self.rotate_image(
            self.second_hand, second_angle, self.center
        )

        # сначала длинную, потом короткую или наоборот — не принципиально
        self.screen.blit(second_rotated, second_rect)
        self.screen.blit(minute_rotated, minute_rect)