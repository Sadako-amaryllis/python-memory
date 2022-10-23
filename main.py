import pygame
from game import Game
from music import Music

game = Game()
music = Music()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
    game.update(event_list)
pygame.quit()