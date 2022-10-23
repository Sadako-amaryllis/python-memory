import pygame
import random
import os
from tile import Tile

class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False

        # image pokemon
        self.all_pokemons = [f for f in os.listdir('images/pokemon') if os.path.join('images/pokemon', f)]
        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.margin_left = 60
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        # retournement cartes
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # first level
        self.generate_level(self.level)

        # Déclanchement musique
        self.is_music_playing = True
        self.sound_on = pygame.image.load('images/sound2.png').convert_alpha()
        self.sound_off = pygame.image.load('images/mute2.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - -1, 10))
        pygame.mixer.music.load('sounds/opening.mp3')
        pygame.mixer.music.set_volume(.20)
        pygame.mixer.music.play()

    def update(self, event_list):
        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == 60:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []

    def generate_level(self, level):
        self.pokemons = self.select_random_pokemons(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.generate_tileset(self.pokemons)

    def generate_tileset(self, pokemons):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows
        self.tiles_group.empty()

        for i in range(len(pokemons)):
            x = (self.img_width + self.padding) * (i % self.cols)
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(pokemons[i], x, y)
            self.tiles_group.add(tile)

    def select_random_pokemons(self, level):
        pokemons = random.sample(self.all_pokemons, (self.level + self.level + 2))
        pokemons_copy = pokemons.copy()
        pokemons.extend(pokemons_copy)
        random.shuffle(pokemons)
        return pokemons

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

    def draw(self):
        # fonts
        title_font = pygame.font.Font('fonts/Pokemon-title.ttf.', 44)
        content_font = pygame.font.Font('fonts/Pokemon-title.ttf', 24)

        # text
        title_text = title_font.render('Pokemon memories', True, WHITE)
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Phase ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        info_text = content_font.render('Trouver les pokémons similaires', True, WHITE)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        if not self.level == 10:
            next_text = content_font.render('Phase terminée. Appuyez sur Espace pour la phase suivante!', True, WHITE)
        else:
            next_text = content_font.render('FVous avez terminé la game ! Appuyez sur espace pour recommencer', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            screen.blit(next_text, next_rect)

# Fenêtre Pygame
pygame.init()

WINDOW_WIDTH = 1160
WINDOW_HEIGHT = 760
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pokemon memories')

WHITE = (255, 255, 255)