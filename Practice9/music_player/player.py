import pygame
import os


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        music_folder = os.path.join(os.path.dirname(__file__), "music")

        self.playlist = [
            os.path.join(music_folder, "song1.mp3"),
            os.path.join(music_folder, "song2.mp3"),
            os.path.join(music_folder, "song3.mp3"),
        ]

        self.current_track = 0
        self.paused = False

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def toggle_pause(self):
        if self.paused:
            self.unpause()
        else:
            self.pause()

    def next_track(self):
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        self.current_track = (self.current_track - 1) % len(self.playlist)
        self.play()