import pygame
import pygame.mixer


class sounds:
    @staticmethod
    def init_music():
        pygame.mixer.music.load(filename="assets/Music/StartMenuMusic.mp3")
        pygame.mixer.music.set_volume(0.025)
        pygame.mixer.music.play(loops=5, fade_ms=40, start=0)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()

    @staticmethod
    def start_music():
        pygame.mixer.music.play(loops=5, fade_ms=40, start=0)

