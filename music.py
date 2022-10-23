import pygame
import os

class Music():
    def __init__(self):
        self.level = 1
        self.level_complete = False
    # Déclanchement musique
        self.is_music_playing = True
        self.sound_on = pygame.image.load('images/sound2.png').convert_alpha()
        self.sound_off = pygame.image.load('images/mute2.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - -1, 10))
        pygame.mixer.music.load('sounds/opening.mp3')
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play()

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 10:
                        self.level = 1
                    self.generate_level(self.level)


WINDOW_WIDTH = 1160
WINDOW_HEIGHT = 760