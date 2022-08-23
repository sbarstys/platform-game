import pygame
import sys
from game import *

SURFACE_FILE_INDEX = 1
SPRITE_FILE_INDEX = 2

pygame.init()
clock = pygame.time.Clock()

#Game driver with main while loop to control events and movements
def main():
    surface_file = str(sys.argv[SURFACE_FILE_INDEX])
    sprite_file = str(sys.argv[SPRITE_FILE_INDEX])
    game = Game(surface_file, sprite_file)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game.check_enemy_collision()
        game.check_coin_collision()
        if not game.win_by_coin and not game.lose_by_enemy:
            key_pressed = pygame.key.get_pressed()
            game.move_enemies()
            game.handle_key_mov(key_pressed)
            game.handle_pos()
        game.draw_window()
        pygame.display.flip()
        clock.tick(Game.FPS)

if __name__ == '__main__':
    main()